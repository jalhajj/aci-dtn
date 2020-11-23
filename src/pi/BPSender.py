#! /usr/bin/python3
from datetime import datetime
from threading import Thread
import time
import sounddevice as sd
import numpy as np
import json
import os
# Import module
import pyion
from pyion import BpCustodyEnum, BpPriorityEnum, BpReportsEnum

# =================================================================
# === Define global variables
# =================================================================

# ION node number
node_nbr = 1

# Originating and destination endpoints
orig_eid = 'ipn:150.1'
dest_eid = 'ipn:149.1'
rept_eid = 'ipn:150.2'

# Define endpoint properties
ept_props = {
    'TTL':          3600,   # [sec]
    'custody':      BpCustodyEnum.SOURCE_CUSTODY_REQUIRED,
    'priority':     BpPriorityEnum.BP_EXPEDITED_PRIORITY,
    'report_eid':   rept_eid,
    'report_flags': BpReportsEnum.BP_RECEIVED_RPT
    #'report_flags': BpReportsEnum.BP_RECEIVED_RPT | BpReportsEnum.BP_CUSTODY_RPT,
}

# Create a proxy to ION
proxy = pyion.get_bp_proxy(node_nbr)

# Attach to ION
proxy.bp_attach()

# =================================================================
# === Acquire reports
# =================================================================

# Open endpoint to get reports
rpt_eid = proxy.bp_open(rept_eid)

def print_reports():
    while True:
        try:
            data = rpt_eid.bp_receive()
            print(data.decode())
        except InterruptedError:
            break

# Start monitoring thread
th = Thread(target=print_reports, daemon=True)
th.start()

# =================================================================
# === MAIN
# =================================================================

# Open a endpoint and set its properties. Then send file
with proxy.bp_open(orig_eid, **ept_props) as eid:
    while True:
        sample = sd.rec(int(duration*freq),samplerate=freq, channels=1)
        sd.wait()
        now = time.time() # datetime.datetime.now()
        influx_now = time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime(time.time()))
        # now =time.mktime(datetime.datetime.now().timetuple())
        level = float(np.average(np.abs(sample)))
        maxlevel = float(np.max(np.abs(sample)))
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

        eid.bp_send(dest_eid, data)
