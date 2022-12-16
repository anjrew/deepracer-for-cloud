import streamlit as st

import pandas as pd

from deepracer.logs import \
    DeepRacerLog
from deepracer.logs import (DeepRacerLog, S3FileHandler)


# @st.cache
def load_logs(bucket:str, prefix:str, endpoint:str, profile="minio"):
    """Load telemetry logs from S3 bucket"""
    fh = S3FileHandler(bucket=bucket, prefix=prefix,
                    profile=profile, s3_endpoint_url=endpoint)

    log = DeepRacerLog(filehandler=fh)

    log.load()
    
    return log

@st.cache
def load_meta_data(bucket:str, prefix:str, endpoint:str, profile="minio") -> dict:
    """Load telemetry logs from S3 bucket"""
   

    logs = load_logs(bucket, prefix, endpoint, profile)
    
    return {
        'action_space': logs.action_space(),
        'hyperparameters': logs.hyperparameters(),
        'agent_and_network': logs.agent_and_network()
    }