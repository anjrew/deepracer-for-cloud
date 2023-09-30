## Prerequisites

- Make sure the environment is activated and setup

## BUILD

From within the folder containing the Dockerfile
"""bash
    docker build -t deep-racer-data-storage:latest -f Dockerfile.data-storage .
"""


## RUN
Example of running the data-storage from the ROOT of the project

'''bash
    docker run \
    --rm \
    --name data-storage \
    deep-racer-data-storage:latest
''' 

## Dump Database 

Run in command line:
- pg_dump aws_deep_racer > ./db_creator.sql