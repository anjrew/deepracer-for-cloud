import streamlit as st
import pandas as pd
import numpy as np
import os
import argparse
import boto3

from deepracer.logs import metrics
from navigation import NavOptions

# parser = argparse.ArgumentParser(description='Run the DeepRacer analysis streamlit app')

# parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                     help='an integer for the accumulator')

# parser.add_argument("-m", "--models-path-", dest="models_path",  metavar='M',
#                     help="The path to where the models are stored in the system", type=str ,default=None)

# args = vars(parser.parse_args())

BUCKET_NAME=os.getenv('DR_LOCAL_S3_BUCKET', 'bucket')
model_prefix=os.getenv('DR_LOCAL_S3_MODEL_PREFIX')

# S3_ENDPOINT=os.getenv('DR_MINIO_URL', 'http://minio:9000') 
S3_ENDPOINT='http://localhost:9000'

DIR = os.path.dirname(os.path.abspath(__file__))

session = boto3.session.Session(profile_name='minio')  # type: ignore
s3_client = session.resource("s3", endpoint_url=S3_ENDPOINT)
bucket = s3_client.Bucket(BUCKET_NAME)  # type: ignore


model_folders = {}
all_objects = bucket.objects.all()
for object in all_objects:
    print(object.key)
    path_parts = object.key.split('/')
    if len(path_parts) > 1:
        model_name = path_parts[0]
        if model_name != 'custom_files':
            print('Got model_name', model_name)
            model_folders[model_name] = model_folders



# ===== UI ======

nav =  st.sidebar.radio(
    "Choose view",
    [e.value for e in NavOptions]
)



st.title('DeepRacer Analysis')


model_prefix = st.selectbox(
    'Model name',
    model_folders.keys())


st.button('Refresh 🔄')


try:
    # tm = metrics.TrainingMetrics(BUCKET, model_name=PREFIX, profile='minio', s3_endpoint_url=ENDPOINT)
    tm = metrics.TrainingMetrics(BUCKET_NAME, model_name=model_prefix, profile='minio', s3_endpoint_url=S3_ENDPOINT)  # type: ignore

    summary_df = tm.getSummary(method='mean', summary_index=['r-i','master_iteration'])

    fig = tm.plotProgress()


    st.pyplot(fig)
    
except Exception as e:
    st.error(f'Failed to load model {model_prefix}')
