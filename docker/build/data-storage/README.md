## BUILD

From within the folder containing the Dockerfile
"""bash
    docker build -t deep-racer-data-storage:latest -f Dockerfile.data-storage .
"""


## RUN
Example of running the data-storage

<!-- """bash
    docker run \
    --rm \
    -v ${PWD}/scripts/local_console/local_console.py:/app/script.py \
    --name data-storage \
    deep-racer-data-storage:latest \
    python /app/script.py
""" -->

## Dump Database 

Run in command line:
- pg_dump aws_deep_racer > ./db_creator.sql