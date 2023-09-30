# Robo Container
## Build

From within the folder containing the Dockerfile build the robomaker container
```bash
    docker build -t anjrew-deepracer-robomaker-simulator:latest -f ./Dockerfile.robomaker .
```

## Save the image
```bash
docker save anjrew-deepracer-robomaker-simulator:<TAG> -o anjrew-deepracer-robomaker-simulator-<TAG>.tar
```

## Usage

Set the docker environment variable of the container IGNORE_ACTION to 'True'

## ROS Topics

speed_topics [
    '/racecar/left_rear_wheel_velocity_controller/command', 
    '/racecar/right_rear_wheel_velocity_controller/command',
    '/racecar/left_front_wheel_velocity_controller/command', 
    '/racecar/right_front_wheel_velocity_controller/command'
]

steering_topics [
    '/racecar/left_steering_hinge_position_controller/command', 
    '/racecar/right_steering_hinge_position_controller/command'
]

# Gaming container

## Build
```bash
    docker build -t anjrew-deepracer-robomaker-controller:latest -f ./Dockerfile.controller .
```

# Robomaker container
```bash
    docker build -t anjrew-deepracer-robomaker-simulator:latest -f ./Dockerfile.robomaker .
```
## Build

## Get the IP of the  RoboContainer
```bash
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' robo_container_id

```
or

```bash
#!/bin/bash

# Replace 'your_image_name' with the desired Docker image name
image_name="anjrew-deepracer-robomaker-simulator:latest"

# Get the container ID associated with the image name
container_id=$(docker ps -q -f ancestor=$image_name)

# Use the container ID to get the IP address
container_ip=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $container_id)

# Print the container IP address
echo "Container IP Address: $container_ip"

```

### run
```docker run -e ROS_MASTER_URI=http://<robo_ip>:11311 --rm --privileged -it --net sagemaker-local anjrew-deepracer-robomaker-controller:latest```

docker run -e ROS_MASTER_URI=http://10.0.1.20:11311 --rm --privileged -it --net sagemaker-local anjrew-deepracer-robomaker-controller:latest


### Do it with the new Docker compose file
```bash
docker-compose -f $DR_DIR/docker/docker-compose-training.yml -f $DR_DIR/docker/build/robo-simulator/docker-compose-robo-simulator.yml up
```