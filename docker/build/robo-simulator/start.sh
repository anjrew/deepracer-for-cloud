#!/bin/bash

echo $1
echo $2
echo $3
# Run the existing command in the background
./run.sh $2 &

# Run your additional command in the background
python controller.py &

# Wait for both processes to complete
wait
