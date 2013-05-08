/*
 * Oscilloscope Arduino firmware
 *
 * This file is part of Oscilloscope.
 *
 * Copyright 2013 Michal Belica <devel@beli.sk>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see http://www.gnu.org/licenses/.
 */

int ledPin = 13;

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
}

void send_data(unsigned int samples, unsigned int interval) {
  word av;
  for( int i = 0; i < samples; ++i ) {
    digitalWrite(ledPin, bitRead(i, 0));
    av = word(analogRead(0));
    Serial.write(lowByte(av));
    Serial.write(highByte(av));
    if( interval > 0 ) {
      delay(interval-1);
    }
  }
  digitalWrite(ledPin, LOW);
}

unsigned int serial_read_word() {
  byte al = Serial.read();
  byte ah = Serial.read();
  return word(ah, al);
}

// the loop routine runs over and over again forever:
void loop() {
  unsigned long t1, t2, dt;
  byte b, csum, mycsum;
  word samples, interval;
  
  if( (b = Serial.read()) != -1 ) {
    if( b == 'P' ) {
      digitalWrite(ledPin, HIGH);
      Serial.write('p');
      delay(10);
      digitalWrite(ledPin, LOW);
    } else if( b == 'A' ) {
      samples = serial_read_word();
      interval = serial_read_word();
      csum = Serial.read();
      mycsum = (samples + interval) & 0xff;
      if( csum ==  mycsum) {
        Serial.write('A');
        t1 = millis();
        send_data(samples, interval);
        t2 = millis();
        dt = t2 - t1;
        Serial.write((const unsigned char *)&dt, 4);
      } else {
        Serial.write('E');
        Serial.write(mycsum);
      }
    }
  }
  delay(50);
}

