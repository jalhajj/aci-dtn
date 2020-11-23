#!/usr/bin/python3 -u
#!/usr/bin/python3 -u
# -u is for unbuffered io

# Install instructions:
#  apt install python3-pip libportaudio2
# pip3 install sounddevice
# pip3 install numpy
# pip3 install influxdb

from influxdb import InfluxDBClient
import sys
import os
import time
import datetime
import socket


host="acivm.pultar.org"
# host="localhost"
port=8087
buffered = []

for line in sys.stdin:
    try:
        # connect
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))

        # send current line
        s.send(line.encode())
    except:
        buffered.append(line)
        print("Could not send current line. Adding to buffer")
    try:
        for bline in buffered:
            s.send(bline.encode())
            buffered.remove(bline)
        s.close()

    except:
        print("Error sending lines from buffer.")

    if (len(buffered)>0):
        print(str(len(buffered))+" items in buffer")
        print(buffered)
