#!/usr/bin/env python

import RPi.GPIO as GPIO, time, os

PIN = 18
DEBUG = 1
GPIO.setmode(GPIO.BCM)


def RCtime(RCpin):
  reading = 0
  GPIO.setup(RCpin, GPIO.OUT)
  GPIO.output(RCpin, GPIO.LOW)
  time.sleep(0.1)

  GPIO.setup(RCpin, GPIO.IN)
  while GPIO.input(RCpin) == GPIO.LOW:
    reading += 1
  return reading


i = 0
while True:
  print "%d: %d" %(i, RCtime(PIN))
  i += 1
