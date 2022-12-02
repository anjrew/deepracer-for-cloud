## BUILD

From withing the folder containing the Dockerfile
"""bash
    docker build -t deep-racer-live-analysis:latest -f ${PWD}/Dockerfile.live-analysis .
"""


## RUN
Example of running the executer

"""bash
    docker run \
    --rm \
    -v ${PWD}/scripts/local_console/local_console.py:/app/script.py \
    --name executer \
    deep-racer-live-analysis:latest
"""

