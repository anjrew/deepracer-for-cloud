FROM awsdeepracercommunity/deepracer-rlcoach:5.1.0

# Install required Python packages
RUN pip install --no-cache-dir \
        pygame

COPY ./env_utils.py /deepracer/common/env_utils.py

COPY ./rollout_agent_ctrl.py /deepracer/markov/agent_ctrl/rollout_agent_ctrl.py 

