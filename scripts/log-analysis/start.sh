#!/usr/bin/env bash

docker run --rm -d -p "$DR_ANALYSIS_PORT:8888" \
-v `pwd`/../../data/logs:/workspace/logs \
-v `pwd`/../../docker/volumes/.aws:/root/.aws \
-v `pwd`/../../data/analysis:/workspace/analysis \
-v `pwd`/../../data/minio:/workspace/minio \
--shm-size=9.90gb \ 
--name loganalysis \
--network sagemaker-local \
 $DR_ANALYSIS_IMAGE:$DR_ANALYSIS_IMAGE_TAG

docker logs -f loganalysis