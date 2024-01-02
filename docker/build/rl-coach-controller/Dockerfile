FROM awsdeepracercommunity/deepracer-rlcoach:5.1.0


COPY ./multi_agent_coach /deepracer/markov/multi_agent_coach
COPY ./training_worker.py /deepracer/bundle/markov/training_worker.py
COPY ./sagemaker_graph_manager.py /deepracer/bundle/markov/sagemaker_graph_manager.py


# This is not used. It is used in the ROBOMAKER container
# COPY ./rollout_agent_ctrl.py /deepracer/markov/agent_ctrl/rollout_agent_ctrl.py 

