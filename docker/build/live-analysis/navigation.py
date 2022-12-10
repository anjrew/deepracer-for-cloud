from enum import Enum

class NavOptions(Enum):
    """ Different options for the navigation"""
    METRICS = 'Metrics'
    HYPER_PARAMETERS = 'Hyper Parameters'
    REWARD_HEATMAP = 'Reward heatmap'
    TRAINING_ANALYSIS = 'Training Analysis'
    ACTION_SPACE = 'Action Space'
    TRACK_ANALYSIS = 'Track Analysis'
    VISUAL_ANALYSIS = 'Visual Analysis'
    AGENT_AND_NETWORK = 'Agent and Network'
    