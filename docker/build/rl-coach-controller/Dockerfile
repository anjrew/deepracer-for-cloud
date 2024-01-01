FROM awsdeepracercommunity/deepracer-rlcoach:5.1.0

# Install required Python packages
RUN pip install --no-cache-dir \
        pygame debugpy

COPY ./env_utils.py /deepracer/common/env_utils.py
COPY ./multi_agent_coach /deepracer/markov/multi_agent_coach
COPY ./training_worker.py /deepracer/bundle/markov/training_worker.py
COPY ./sagemaker_graph_manager.py /deepracer/bundle/markov/sagemaker_graph_manager.py


# This is not used. It is used in the ROBOMAKER container
# COPY ./rollout_agent_ctrl.py /deepracer/markov/agent_ctrl/rollout_agent_ctrl.py 

