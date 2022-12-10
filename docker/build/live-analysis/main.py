import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import argparse
import boto3
from file_loaders import load_logs, load_meta_data
from s3_functions import list_bucket_s3
# import metrics_page as mp

from deepracer.logs import metrics
from navigation import NavOptions

# parser = argparse.ArgumentParser(description='Run the DeepRacer analysis streamlit app')

# parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                     help='an integer for the accumulator')

# parser.add_argument("-m", "--models-path-", dest="models_path",  metavar='M',
#                     help="The path to where the models are stored in the system", type=str ,default=None)

# args = vars(parser.parse_args())

BUCKET_NAME=os.getenv('DR_LOCAL_S3_BUCKET', 'bucket')

# S3_ENDPOINT=os.getenv('DR_MINIO_URL', 'http://minio:9000') 
S3_ENDPOINT='http://localhost:9000'

DIR = os.path.dirname(os.path.abspath(__file__))

model_folders = list_bucket_s3(BUCKET_NAME, S3_ENDPOINT)
                 
                 
# ===== UI ======

navigation =  st.sidebar.radio(
    "Choose view",
    [e.value for e in NavOptions]
)

st.title('DeepRacer Analysis')

model_prefix = st.selectbox(
    'Choose Model',
    model_folders)

st.button('Refresh 🔄')

st.markdown("***")

st.header(navigation)

if model_prefix is not None:
    
    if navigation == NavOptions.METRICS.value:
        try:
            tm = metrics.TrainingMetrics(BUCKET_NAME, model_name=model_prefix, profile='minio', s3_endpoint_url=S3_ENDPOINT)  # type: ignore

            mplt_col1, mplt_col2 = st.columns(2)
            
            method = mplt_col1.selectbox(
                'Choose Method',
                ['mean','median','min','max'])
            
            rolling_average = mplt_col2.number_input(label='Moving average (Iterations)',value=2)
            
            fig = tm.plotProgress(method=method, rolling_average=rolling_average)  # type: ignore

            st.pyplot(fig)
            
            summary_df = tm.getSummary(method=method, summary_index=['r-i','master_iteration'])  # type: ignore
            
            st.dataframe(summary_df.head(10))
            
        except Exception as e:
            st.error(f'Failed to load model {model_prefix}')

    elif navigation == NavOptions.HYPER_PARAMETERS.value:
        logs = load_meta_data(BUCKET_NAME, model_prefix, S3_ENDPOINT)
        st.json(logs['hyperparameters'])


    elif navigation == NavOptions.AGENT_AND_NETWORK.value:
        logs = load_meta_data(BUCKET_NAME, model_prefix, S3_ENDPOINT)
        st.json(logs['agent_and_network'])

        
    elif navigation == NavOptions.ACTION_SPACE.value:
        try:
            logs = load_meta_data(BUCKET_NAME, model_prefix, S3_ENDPOINT)
            action_space = logs['action_space']
            st.json(action_space)
            
            if isinstance(action_space, list):
                print('Creating action space graph')
                x = []
                y = []
                for ang in action_space:
                    x.append(ang['steering_angle'])
                    y.append(ang['speed'])  
                
                fig, ax = plt.subplots()

                ax.set_xlabel('Steering Angle')     # type: ignore
                ax.set_ylabel('Speed')              # type: ignore
                ax.scatter(x, y)
                st.pyplot(fig)
            else:
                fig, ax = plt.subplots()
                speed=action_space['speed']
                steering_angle= action_space['steering_angle']

                ax.set_xlabel('Steering Angle')     # type: ignore
                ax.set_ylabel('Speed')              # type: ignore
                
                st.pyplot(fig)
        except Exception as e:
            print("Error: Failed to load action space", e)
            st.error(f'Failed to load action space')

