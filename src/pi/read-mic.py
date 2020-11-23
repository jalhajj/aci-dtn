#!/usr/bin/python3 -u
# u is for ubuffered io


# Install instructions:
#  apt install python3-pip libportaudio2
# pip3 install sounddevice
# pip3 install numpy
# pip3 install influxdb

import sounddevice as sd
import numpy as np
import json
import os
import time
import datetime

freq=48000
duration=30

while True:
    sample = sd.rec(int(duration*freq),samplerate=freq, channels=1)
    sd.wait()
    now = time.time() # datetime.datetime.now()
    influx_now = time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime(time.time()))
    # now =time.mktime(datetime.datetime.now().timetuple())
    

    level = float(np.average(np.abs(sample)))
    maxlevel = float(np.max(np.abs(sample)))
    
    # print(level*100)

    data =  {
        "measurement": "microphone",
        "time": influx_now,
        "tags": {
            "host": os.uname()[1],
            "duration": duration
            },
        "fields": {
            "level": level,
            "level_max": maxlevel,
            "duration": duration,
            "time_recorded": now
            }
        }
    
    # datajson =  json.dumps(data)
    print(json.dumps(data))
    
    
