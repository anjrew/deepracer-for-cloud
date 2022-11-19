#!/bin/bash

usage(){
	echo "Usage: $0 [-f] [-w] [-p <model-prefix>] [-d <delimiter>]"
    echo ""
    echo "Command will set the current model to be the pre-trained model and increment a numerical suffix."
    echo "-p model  Sets the to-be name to be <model-prefix> rather than auto-incremeneting the previous model."
    echo "-d delim  Delimiter in model-name (e.g. '-' in 'test-model-1')"
    echo "-f        Force. Ask for no confirmations."
    echo "-w        Wipe the S3 prefix to ensure that two models are not mixed."
    echo "-n        Set this flag so not to increment with pretrained and instead just make a new model"
	exit 1
}

trap ctrl_c INT

function ctrl_c() {
        echo "Requested to stop."
        exit 1
}

OPT_DELIM='-'
IS_PRETRAINED=True

while getopts ":fwpn:d:" opt; do
case $opt in

f) OPT_FORCE="True"
;;
p) OPT_PREFIX="$OPTARG"
;;
w) OPT_WIPE="--delete"
;;
d) OPT_DELIM="$OPTARG"
;;
n) IS_PRETRAINED=False
;;
h) usage
;;
\?) echo "Invalid option -$OPTARG" >&2
usage
;;
esac
done

read -r -p "Do you want to retrain the last model? [y/N] " response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
then
    IS_PRETRAINED=True
else
    IS_PRETRAINED=False
fi

echo "Iterating model and using pretrained: $IS_PRETRAINED"

CONFIG_FILE=$DR_CONFIG
echo "Configuration file $CONFIG_FILE will be updated."

## Read in data
CURRENT_RUN_MODEL=$(grep -e "^DR_LOCAL_S3_MODEL_PREFIX" ${CONFIG_FILE} | awk '{split($0,a,"="); print a[2] }')
CURRENT_RUN_MODEL_NUM=$(echo "${CURRENT_RUN_MODEL}" | \
                    awk -v DELIM="${OPT_DELIM}" '{ n=split($0,a,DELIM); if (a[n] ~ /[0-9]*/) print a[n]; else print ""; }')
if [[ -z ${CURRENT_RUN_MODEL_NUM} ]];
then
    NEW_RUN_MODEL="${CURRENT_RUN_MODEL}${OPT_DELIM}1"
else
    NEW_RUN_MODEL_NUM=$(echo "${CURRENT_RUN_MODEL_NUM} + 1" | bc )
    NEW_RUN_MODEL=$(echo $CURRENT_RUN_MODEL | sed "s/${CURRENT_RUN_MODEL_NUM}\$/${NEW_RUN_MODEL_NUM}/")
fi
RED='\033[0;31m'
NC='\033[0m' # No Color
if [[ -n "${NEW_RUN_MODEL}" ]];
then
    echo "Incrementing model from ${CURRENT_RUN_MODEL} to ${NEW_RUN_MODEL}"
    if [[ -z "${OPT_FORCE}" ]]; 
    then
        read -r -p "Are you sure? [y/N]" response
        if [[ ! "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
        then
            echo "Aborting."
            exit 1
        fi
    fi
    sed -i.bak -re "s/(DR_LOCAL_S3_PRETRAINED_PREFIX=).*$/\1$CURRENT_RUN_MODEL/g; s/(DR_LOCAL_S3_PRETRAINED=).*$/\1$IS_PRETRAINED/g; ; s/(DR_LOCAL_S3_MODEL_PREFIX=).*$/\1$NEW_RUN_MODEL/g" "$CONFIG_FILE" && echo "Done."
else
    echo    "Error in determining new model. Aborting."
    exit 1
fi

if [[ -n "${OPT_WIPE}" ]];
then
    MODEL_DIR_S3=$(aws ${DR_LOCAL_PROFILE_ENDPOINT_URL} s3 ls s3://${DR_LOCAL_S3_BUCKET}/${NEW_RUN_MODEL} )
    if [[ -n "${MODEL_DIR_S3}" ]];
    then
        echo "The new model's S3 prefix s3://${DR_LOCAL_S3_BUCKET}/${NEW_RUN_MODEL} exists. Will wipe."
    fi
    if [[ -z "${OPT_FORCE}" ]]; 
    then
        read -r -p '$(echo "Are you sure? [y/N])"' response
        if [[ ! "$response" =~ ^([yY][eE][sS]|[yY])$ ]]
        then
            echo "Aborting."
            exit 1
        fi
    fi
    aws ${DR_LOCAL_PROFILE_ENDPOINT_URL} s3 rm s3://${DR_LOCAL_S3_BUCKET}/${NEW_RUN_MODEL} --recursive
fi

