#!/bin/bash

echo "Commiting custom log analysis image"
echo "Give a commit message:"
read commit_message
CURRENT_CONTAINER_HASH=$(docker ps | grep loganalysis | head -c 12)

echo "Run following scripts"
COMMIT_SCRIPT="docker commit -a $DR_USER_NAME -m \"$commit_message\" $CURRENT_CONTAINER_HASH $DR_ANALYSIS_IMAGE:$DR_ANALYSIS_IMAGE_TAG"
echo $COMMIT_SCRIPT
eval $COMMIT_SCRIPT
SAVE_SCRIPT="docker save -o "$DR_DIR$DR_ANALYSIS_BACKUP_PATH" $DR_ANALYSIS_IMAGE:$DR_ANALYSIS_IMAGE_TAG"
echo $SAVE_SCRIPT
eval $SAVE_SCRIPT




