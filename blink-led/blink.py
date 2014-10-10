#!/usr/bin/env python
"""Blink an LED!

"""
import RPi.GPIO as GPIO
import time

PIN = 7

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN, GPIO.OUT)  # GPIO.OUT or GPIO.IN
while True:
    GPIO.output(PIN, True)  # turn on pin
    time.sleep(5, False)

    GPIO.output(PIN, False)  # turn off pin
    time.sleep(5)
