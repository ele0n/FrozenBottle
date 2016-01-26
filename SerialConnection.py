#!/usr/bin/python
import serial
import struct


class SerialConnection(object):
    def __init__(self, devicename, baudrate, rows, cols):
        self.DEVICE = devicename
        self.baud = baudrate
        self.ser = serial.Serial(self.DEVICE, self.baud)

        self.rows = rows
        self.cols = cols

        # odd lines are missing 1 bottle
        odd = (rows - rows % 2) / 2
        self.bottles = [(255, 255, 255)] * ((rows*cols)-odd)
        self.bottles_next = [(255, 255, 255)] * ((rows*cols)-odd)

    @property
    def index_count(self):
        return self.xy_to_i(self.cols-1, self.rows-1) + 1

    def i_to_xy(self, i):
        # compensate for odd lines missing 1 bottle
        for k in range(1, i, 2):
            if i >= self.cols-1+self.cols*k:
                i += 1

        x = i % self.cols
        y = i // self.cols

        return x, y

    def xy_to_i(self, x, y):
        i = y*self.cols + x

        # compensate for odd lines missing 1 bottle
        for k in range(1, i, 2):
            if i >= self.cols-1+self.cols*k:
                i -= 1

        return i

    def checksum(self, body):
        result = ord(body[0])
        for i in range(0, len(body)):
            if i > 0:
                result = result ^ ord(body[i])
        return struct.pack('B', result)

    def send_i(self, i, red, green, blue, commit=True):
        if commit:
            self.bottles[i] = (red, green, blue)
            self.bottles_next[i] = (red, green, blue)
        else:
            self.bottles_next[i] = (red, green, blue)
            return

        # write header
        self.ser.write('\xBA\xBE')

        # write body
        body = chr(i) + chr(red) + chr(green) + chr(blue)
        self.ser.write(body)

        # write checksum
        self.ser.write(self.checksum(body))

    def send_xy(self, x, y, red, green, blue, commit=True):
        i = y * 7 + (x-3) * (-1)**y + 3 - (y // 2)

        # virtual bubble
        if y % 2 != 0:
            if x == 6:
                return
            i -= 1

        self.send(i, red, green, blue, commit)

    def get_color_i(self, i):
        return self.bottles[i]

    def get_color_xy(self, x, y):
        i = self.xy_to_i(x, y)
        return self.get_color_i(i)

    def commit(self):
        for i, color in enumerate(self.bottles):
            if self.bottles[i] != self.bottles_next[i]:
                self.send_i(i, *color, commit=True)
