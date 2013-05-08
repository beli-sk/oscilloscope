#!/usr/bin/python
# vim: ai:ts=4:sw=4:sts=4:et:fileencoding=utf-8
#
# This file is part of Oscilloscope
#
# Copyright 2013 Michal Belica <devel@beli.sk>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.
#

import serial
import sys
import struct
import select
import time
from optparse import OptionParser

def read_packet(ser, samples):
    p = ser.read(samples*2+4)
    if len(p) < samples*2+4:
        print "short read:", len(p)
        return (None, None)
    data = []
    for i in range(0, samples):
        word = p[i*2] + p[i*2+1]
        data.append(struct.unpack('<H', word)[0])
    i = samples*2;
    dword = p[i] + p[i+1] + p[i+2] + p[i+3]
    t = struct.unpack('<I', dword)[0]
    return (data, t)

def to_pct(n):
    return float(n) / 1023.0 * 100.0

def serial_ping(ser):
    for i in range(3):
        ser.write('P')
        c = None
        rl, wl, xl = select.select([ser], [], [], 1)
        if rl:
            c = ser.read(1)
        if c == 'p':
            sys.stderr.write('Serial ping OK\n')
            break
    else:
        sys.stderr.write( 'Serial ping failed\n')
        ser.close()
        sys.exit(1)

def write_packet(ser, samples, interval):
    ser.write('A' + struct.pack('<HH', samples, interval))
    csum = (samples + interval) & 0xff
    ser.write(struct.pack('<B', csum))
    c = ser.read(1)
    if c == 'E':
        rcsum = ser.read(1)
        sys.stderr.write('Packet check sum error: %d vs. %d' % (csum, rcsum))
    elif c != 'A':
        sys.stderr.write('Bad response received')

def draw_bar(pct):
    width = 40
    sys.stdout.write('\r%6.2f [' % pct)
    full = int(round(pct / 100 * width))
    empty = width - full
    for i in range(full):
        sys.stdout.write('#')
    for i in range(empty):
        sys.stdout.write(' ')
    sys.stdout.write(']')

def multi_probe(ser, samples, interval):
    ser.flushInput()
    write_packet(ser, samples, interval)
    sys.stderr.write("Reading...\n")
    data, tt = read_packet(ser, samples)
    real_interval = float(tt) / float(samples);
    real_time = float(0)
    for n in data:
        sys.stdout.write('%g\t%g\n' % (real_time, to_pct(n)))
        real_time += real_interval
    sys.stderr.write('Total time: %d ms\n' % tt)

def realtime_probe(ser, interval):
    ser.timeout = 1
    while True:
        write_packet(ser, 1, 1)
        data, tt = read_packet(ser, 1)
        if data is not None and tt is not None:
            draw_bar(to_pct(data[0]))
            sys.stdout.flush()
            time.sleep(float(interval)/1000)

parser = OptionParser()
parser.add_option("-d", "--device", dest="device",
        help="read from serial port DEVICE (required)", metavar="DEVICE")
parser.add_option("-s", "--speed", dest="speed", type="int", default=115200,
        help="serial port baud rate (default: 115200)", metavar="BAUD")
parser.add_option("-n", "--samples", dest="samples", type="int", default=100,
        help="number of samples 1-65535 (ignored in realtime) (default: 100)", metavar="SAMPLES")
parser.add_option("-i", "--interval", dest="interval", type="int", default=100,
        help="sampling interval 0-65535 (default: 100)", metavar="SECONDS")
parser.add_option("-r", "--realtime", dest="realtime", action="store_true", default=False,
        help="show sampled values in realtime")
(options, args) = parser.parse_args()

# check for required options
for opt in ['device']:
    if opt not in options.__dict__ or options.__dict__[opt] is None:
        parser.error("parameter --%s is required" % opt)

ser = serial.Serial(options.device, options.speed)
ser.flushInput()
ser.flushOutput()
serial_ping(ser)
if options.realtime:
    realtime_probe(ser, options.interval)
else:
    multi_probe(ser, options.samples, options.interval)
ser.close()

