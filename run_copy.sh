#!/usr/bin/env bash

IP_ADDR=192.168.18.87
BASE_SPEED=20
P=0.65
BACKWARDS_FACTOR=0.8
SLOW_SPEED=10

# LF 1

BASE_SPEED=12
P=0.5
BACKWARDS_FACTOR=0.9
SLOW_SPEED=9

# LF 2

BASE_SPEED=20
P=0.5
BACKWARDS_FACTOR=1.2
SLOW_SPEED=20

echo "Upload script"
scp line_follower_copy.py robot@$IP_ADDR:.
echo "Running..."
ssh -t robot@$IP_ADDR "python3 line_follower_copy.py $BASE_SPEED $P $BACKWARDS_FACTOR $SLOW_SPEED" | tee robot.log
