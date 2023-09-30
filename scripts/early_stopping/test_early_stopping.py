import pytest
import pandas as pd
from deepracer.logs import metrics
from deepracer.logs import AnalysisUtils as au
from deepracer.logs import DeepRacerLog
from deepracer.logs import S3FileHandler
from early_stopping import *



def test_get_fastest_lap():
    data = {'time': [120, 100, 110],
            'master_iteration': [1, 2, 3]}
    complete_laps = pd.DataFrame(data)
    assert get_fastest_lap(complete_laps) == 100

def test_check_fastest_lap_improved():
    data = {'time': [120, 100, 110],
            'master_iteration': [1, 2, 3]}
    complete_laps = pd.DataFrame(data)
    current_fastest_s = 110
    check_result = check_fastest_lap_improved(complete_laps, current_fastest_s)
    
    assert check_result.has_improved == True
    assert check_result.best_result == 100

    complete_laps = pd.DataFrame({'time': [10, 5, 15, 20, 25], 'master_iteration': [0, 1, 2, 3, 4], 'progress': [100, 100, 100, 100, 100]})
    current_fastest_s = 15
    check_result = check_fastest_lap_improved(complete_laps, current_fastest_s)
    assert check_result.has_improved == True
    assert check_result.best_result == 5

    current_fastest_s = 2
    check_result = check_fastest_lap_improved(complete_laps, current_fastest_s)
    assert check_result.has_improved == False
    assert check_result.best_result == 2

def test_check_consistency_improved():
    time_complete_rolling_av = pd.Series([100, 110, 120])
    current_best_consistency = 10
    check_result = check_consistency_improved(time_complete_rolling_av, current_best_consistency)
    assert check_result.has_improved == False
    assert check_result.best_result == 10
    
    time_complete_rolling_av = pd.Series([10, 5, 15, 20, 25])
    current_best_consistency = 8
    check_result = check_consistency_improved(time_complete_rolling_av, current_best_consistency)
    assert check_result.has_improved == True
    assert math.isclose(check_result.best_result, 7.90, rel_tol=1e-2, abs_tol=1e-2)

    time_complete_rolling_av = pd.Series([10, 20, 30, 40, 50])
    current_best_consistency = 14
    check_result = check_consistency_improved(time_complete_rolling_av, current_best_consistency)
    assert check_result.has_improved == False
    assert check_result.best_result == 14


def test_check_completion_rate_improved():
    completion_rates = pd.Series([50, 70, 90])
    new_best_completion = 60
    check_result = check_completion_rate_improved(completion_rates, new_best_completion)
    assert check_result.has_improved == False
    assert check_result.best_result == 90
    
    completion_rates = pd.Series([50, 75, 25, 90])
    new_best_completion = 80
    check_result = check_completion_rate_improved(completion_rates, new_best_completion)
    assert check_result.has_improved == False

    completion_rates = pd.Series([50, 75, 25, 90])
    new_best_completion = 90
    check_result = check_completion_rate_improved(completion_rates, new_best_completion)
    assert check_result.has_improved == False
    
    completion_rates = pd.Series([50, 75, 25, 90])
    new_best_completion = 95
    check_result = check_completion_rate_improved(completion_rates, new_best_completion)
    assert check_result.has_improved == True

def test_check_reward_improved():
    reward_ds = pd.Series([1000, 1200, 1100])
    current_max_reward = 1100
    check_result = check_reward_improved(reward_ds, current_max_reward)
    assert check_result.has_improved == True
    assert check_result.best_result == 1200

    reward_ds = pd.Series([10, 20, 30, 40, 50])
    current_max_reward = 25
    check_result = check_reward_improved(reward_ds, current_max_reward)
    assert check_result.has_improved == True
    assert check_result.best_result == 50


    reward_ds = pd.Series([10, 20, 30, 40, 50])
    current_max_reward = 50
    check_result = check_reward_improved(reward_ds, current_max_reward)
    assert check_result.has_improved == False
    assert check_result.best_result == 50

