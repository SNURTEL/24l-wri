#!/usr/bin/env bash

IP_ADDR=192.168.18.87
BASE_SPEED=20
P=0.5
BACKWARDS_FACTOR=0.9
SLOW_SPEED=15

echo "Upload script"
scp line_follower.py robot@$IP_ADDR:.
echo "Running..."
ssh -t robot@$IP_ADDR "python3 line_follower.py $BASE_SPEED $P $BACKWARDS_FACTOR $SLOW_SPEED" | tee robot.log
