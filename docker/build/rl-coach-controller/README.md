# RL Coach Controller

A Custom RL Coach controller that can be used to train RL Coach agents but with a input for a game controller

## Build

From within the folder containing the Dockerfile build the robomaker container
```bash
    docker build -t anjrew-deepracer-rl-coach:latest -f ./Dockerfile .
```

## Save the image
```bash
docker save anjrew-deepracer-rl-coach:<TAG> -o anjrew-deepracer-rl-coach-<TAG>.tar
```