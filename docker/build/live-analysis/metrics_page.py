import streamlit as st 

# def render(st, BUCKET_NAME: str, S3_ENDPOINT: str, model_prefix: str):
def render(BUCKET_NAME: str, S3_ENDPOINT: str, model_prefix: str):
    """
    Render the model
    :param model_prefix: str
    """
    print(BUCKET_NAME, S3_ENDPOINT, model_prefix)
    try:
        tm = metrics.TrainingMetrics(BUCKET_NAME, model_name=model_prefix, profile='minio', s3_endpoint_url=S3_ENDPOINT)  # type: ignore

        fig = tm.plotProgress()

        st.pyplot(fig)
        
        summary_df = tm.getSummary(method='mean', summary_index=['r-i','master_iteration'])
        summary_df.head(10)
        
    except Exception as e:
        st.error(f'Failed to load model {model_prefix}')
