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
# Import module
import pyion
freq=48000
duration=60
client = InfluxDBClient('acivm.pultar.org','8086','root','root','aciprojectdb')

# =================================================================
# === Define global variables
# =================================================================

# ION node number
node_nbr = 149

# Endpoint to listen to
EID = 'ipn:149.1'

# =================================================================
# === MAIN
# =================================================================

# Create a proxy to ION's BP
proxy = pyion.get_bp_proxy(node_nbr)

# Attach to ION
proxy.bp_attach()

# Open a proxy to receive data
with proxy.bp_open(EID) as eid:
    # You are now ready to received
    print('{} ready to receive'.format(eid))

    nbnd, nbytes, elapsed = 0, 0, 0

    # Receive
    while eid.is_open:
        try:
            # This is a blocking call
            data = eid.bp_receive()

            try:
                data = json.loads(line)
                now = time.time() # datetime.datetime.now()
                fields = data["fields"]
                fields["time_received"] = now
                print(json.dumps(data))
              	client.write_points([data])
            except UnicodeDecodeError:
                print(data)
        except InterruptedError:
            break
