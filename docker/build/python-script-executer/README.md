## BUILD

From within the folder containing the Dockerfile
"""bash
    docker build -t deep-racer-executer:latest -f Dockerfile.python-script-executer .
"""


## RUN
Example of running the executer

"""bash
    docker run \
    --rm \
    -v ${PWD}/scripts/local_console/local_console.py:/app/script.py \
    --name executer \
    deep-racer-executer:latest \
    python /app/script.py
"""

