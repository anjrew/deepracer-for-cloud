## BUILD

From within the folder containing the Dockerfile
```bash
    docker build -t anjrew-deepracer-robomaker-simulator:latest -f ./Dockerfile .
```

## Save the image
```bash
docker save anjrew-deepracer-robomaker-simulator:<TAG> -o anjrew-deepracer-robomaker-simulator-<TAG>.tar
```

## Usage

Set the docker environment variable of the container IGNORE_ACTION to 'True'

