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
    -e DR_LOCAL_S3_MODEL_PREFIX=$DR_LOCAL_S3_MODEL_PREFIX \
    -e DR_LOCAL_S3_BUCKET=$DR_LOCAL_S3_BUCKET \
    -e DR_MINIO_URL=$DR_MINIO_URL \
    --name live-analysis \
    --network=sagemaker-local \
    deep-racer-live-analysis:latest
"""

