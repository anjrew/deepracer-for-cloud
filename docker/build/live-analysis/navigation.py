from enum import Enum

class NavOptions(Enum):
    """ Different options for the navigation"""
    METRICS = 'Metrics'
    REWARD_HEATMAP = 'Reward heatmap'
    TRAINING_ANALYSIS = 'Training Analysis'
    ACTION_SPACE = 'Action Space'
    VISUAL_ANALYSIS = 'Visual Analysis'
    