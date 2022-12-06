import streamlit as st
import pandas as pd
import numpy as np
from deepracer.logs import metrics
import os


BUCKET="bucket"
PREFIX=os.getenv('DR_LOCAL_S3_MODEL_PREFIX')

assert PREFIX is not None, 'No model name was found'

tm = metrics.TrainingMetrics(BUCKET, model_name=PREFIX, profile='minio', s3_endpoint_url='http://minio:9000')

summary=tm.getSummary(method='mean', summary_index=['r-i','master_iteration'])


st.title('Testing if this is working')
