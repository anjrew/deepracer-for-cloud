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
    -v ${PWD}/:/app/files \
    --name live-analysis \
    --network=sagemaker-local \
    deep-racer-live-analysis:latest
"""

