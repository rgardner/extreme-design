#!/usr/bin/env bash

PIN="$1"

echo "$PIN" > /sys/class/gpio/export
cd /sys/class/gpio/gpio"$PIN"

echo "Setting direction to out."
echo "out" >direction

echo "Viewing current state of GPIO $PIN"
cat value

echo "Setting the state of GPIO $PIN to high (relay on)"
echo 1 > value

sleep 10

echo "Setting the state of GPIO $PIN to low (relay off)"
echo 0 >value

echo "Removing pin $PIN from the control of the Kernel driver"
echo "$PIN" > /sys/class/gpio/unexport
