#!/usr/bin/env bash
echo "Starting log analysis container..."

docker run --rm -d -p "8888:8888" \
-v $DR_DIR/data/logs:/workspace/logs \
-v $DR_DIR/docker/volumes/.aws:/root/.aws \
-v $DR_DIR/data/analysis:/workspace/analysis \
-v $DR_DIR/data/minio:/workspace/minio \
--name loganalysis \
--network sagemaker-local \
--shm-size 9.90gb $DR_ANALYSIS_IMAGE:$DR_ANALYSIS_IMAGE_TAG

docker logs -f loganalysis

