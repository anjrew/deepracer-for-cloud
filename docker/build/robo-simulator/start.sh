#!/bin/bash

# Run the existing command in the background
./run.sh $1 &

# Run your additional command in the background
python3 python controller.py &

# Wait for both processes to complete
wait
