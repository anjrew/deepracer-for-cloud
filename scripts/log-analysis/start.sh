#!/usr/bin/env bash

docker run --rm -d -p "8888:8888" \
-v `pwd`/../../data/logs:/workspace/logs \
-v `pwd`/../../docker/volumes/.aws:/root/.aws \
-v `pwd`/../../data/analysis:/workspace/analysis \
-v `pwd`/../../data/minio:/workspace/minio \
--name loganalysis \
--network sagemaker-local \
 $DR_ANALYSIS_IMAGE:$DR_ANALYSIS_IMAGE_TAG

docker logs -f loganalysis