FROM awsdeepracercommunity/deepracer-rlcoach:5.1.0-cpu-avx2

# Install required Python packages
RUN pip install --no-cache-dir \
        pygame

COPY ./start.sh /start.sh

COPY ./rollout_agent_ctrl.py /opt/install/sagemaker_rl_agent/lib/python3.6/site-packages/markov/agent_ctrl/rollout_agent_ctrl.py

# Copy the controller script
COPY ./controller.py controller.py


