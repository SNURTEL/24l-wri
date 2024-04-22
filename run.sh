#!/usr/bin/env bash

echo "Upload script"
scp line_follower.py robot@$1:.
echo "Running..."
ssh -t robot@$1 "python3 line_follower.py $2" | tee robot.log