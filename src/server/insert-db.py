#!/usr/bin/python3 -u
# -u is for unbuffered io

# Install instructions:
#  apt install python3-pip libportaudio2
# pip3 install sounddevice
# pip3 install numpy
# pip3 install influxdb

from influxdb import InfluxDBClient
import sys
import json
import os
import time
import datetime

freq=48000
duration=60

client = InfluxDBClient('acivm.pultar.org','8086','root','root','aciprojectdb')

for line in sys.stdin:
    data = json.loads(line)
    
    now = time.time() # datetime.datetime.now()

    # print(data)
    # print(data["fields"])
    fields = data["fields"]
    fields["time_received"] = now

    print(json.dumps(data))
    client.write_points([data])
    
    
