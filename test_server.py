#!/usr/bin/env python3

import logging
from networktables import NetworkTables
import time

logging.basicConfig(level=logging.DEBUG)

NetworkTables.initialize()
sd = NetworkTables.getTable("SmartDashboard")

i = 0
while True:    
    sd.putNumber('frc-grapher-timestamp', i)
    sd.putNumber('Drive Gyro', i)
    sd.putNumber('Robot X Pose', i**2)
    sd.putNumber('Robot Y Pose', i**3)
    sd.putNumber('Other Data', i**1.5)
    time.sleep(1)
    i += 1