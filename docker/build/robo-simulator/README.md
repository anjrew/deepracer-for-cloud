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

### run
```docker run --rm --privileged -it anjrew-deepracer-robomaker-controller:latest```
