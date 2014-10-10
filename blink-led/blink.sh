#!/usr/bin/env bash
PIN="$1"

sudo su
echo "$PIN" > /sys/class/gpio/export
cd /sys/class/gpio/gpio"$PIN"

echo "Setting direction to out."
echo "out" >direction

echo "Setting pin high."
echo 1 >value

echo "Sleep for 5 seconds."
sleep 5

echo "Setting pin low."
echo 0 >value

echo "$PIN" > /sys/class/gpio/unexport
