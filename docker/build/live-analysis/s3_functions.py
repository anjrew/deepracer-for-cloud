import boto3
import streamlit as st

@st.cache
def list_bucket_s3(BUCKET_NAME: str, S3_ENDPOINT: str) -> 'list[str]':
    """Returns a list of model names

    Args:
        BUCKET_NAME (str): The name of the bucket
        S3_ENDPOINT (str): The endpoint of the bucket
    """
    session = boto3.session.Session(profile_name='minio')  # type: ignore
    s3_client = session.resource("s3", endpoint_url=S3_ENDPOINT)
    bucket = s3_client.Bucket(BUCKET_NAME)  # type: ignore

    model_folders = { }
    
    for object in bucket.objects.all():
        path_parts = object.key.split('/')
        if len(path_parts) > 1:
            model_name = path_parts[0]
            if model_name != 'custom_files':
                model_folders[model_name] = None
    
    return list(model_folders.keys()) # type: ignore)


