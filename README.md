Oscilloscope
============

Tool for analyzing voltage levels over time using
[Arduino](http://www.arduino.cc) on USB serial port.

Consists of command line tool written in [Python](http://www.python.org) and
code for Arduino.

Project
-------

[Oscilloscope project](https://github.com/beli-sk/oscilloscope) is hosted on Github.

Requirements
------------

### hardware

 * Arduino Duemilanove w/ ATmega328 or compatible platform
 * USB cable
 * PC

### software

 * Python 2 (tested with 2.7)
 * [PySerial module](http://pyserial.sourceforge.net/)
 * (optional) [gnuplot](http://gnuplot.info/)

Usage
-----

**Warning**: Never exceed maximal input voltage of your Arduino's input pins
which could be either 3.3V or 5V. Always make sure the voltage you are
measuring is not above the allowed voltage on the analog input pins! Also
make sure the two circuits (Arduino and the measured circuit) have a common
ground.

 * connect Arduino to PC with serial cable
 * (only first time) flash the sketch from _Oscilloscope_ directory
 * connect probed signal to analog pin 0 on Arduino
 * run oscilloscope.py with command line arguments (use -h for help), e.g.:

        ./oscilloscope.py -d /dev/ttyUSB0

 * *or* run `gnuplot_scope.sh` with the same arguments to pipe the data
   directly to gnuplot

License
-------

Copyright 2013 Michal Belica < *devel* at *beli* *sk* >

```
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see http://www.gnu.org/licenses/ .
```

You find a copy of the GNU General Public License in file LICENSE distributed
with the software.

