import logging
import time
from enum import Enum
from typing import List, Union
import pandas as pd
import math

from deepracer.logs import metrics
from deepracer.logs import AnalysisUtils as au
from deepracer.logs import DeepRacerLog
from deepracer.logs import S3FileHandler


class MonitorOption(Enum):
    FASTEST_LAP = 'fastest_lap'
    CONSISTENCY = 'consistency'
    COMPLETION_RATE = 'completion_rate'
    TRAIN_REWARD= 'train_reward'
    EVALUATION_REWARD = 'evaluation_reward'
    
    def is_valid(self):
        return self in MonitorOption

class AggregationMethod(Enum):
    MEAN = 'mean'
    MODE = 'mode'
    MEDIAN = 'median'
    
    def is_valid(self):
        return self in AggregationMethod
    
class ImprovementCheck:
    def __init__(self,
        has_improved: bool,
        best_result: Union[float, int]
    ):
        self.has_improved = has_improved
        self.best_result = best_result     
            

class CurrentBestResults:
    def __init__(self):
        self.lap_time_s = math.inf
        self.consistency_deviation = math.inf
        self.completion_rate = -math.inf
        self.train_reward = -math.inf
        self.eval_reward = -math.inf
        self.patience = 0

    def update_fastest_lap(self, new_fastest_lap_s: float):
        self.lap_time_s = new_fastest_lap_s

    def update_best_consistency_deviation(self, new_best_consistency_deviation: float):
        self.patience = new_best_consistency_deviation
        
    def update_best_completion_rate(self, new_best_completion_rate: float):
        self.completion_rate = new_best_completion_rate

    def update_best_train_reward(self, new_max_reward: float):
        self.train_reward = new_max_reward

    def update_best_eval_reward(self, new_max_reward: float):
        self.train_reward = new_max_reward

class EarlyStoppingArgs:
    # Constants
    # S3
    BUCKET: str
    PREFIX: str
    
    # Data args
    AG_METHOD: AggregationMethod
    REFRESH_TIME_S:int
    ROLLING_AVERAGE: int
    MAX_PATIENCE:int
    MIN_DELTA = int
    MONITOR_OPTIONS: List[MonitorOption]
    
    def __init__(self, 
        bucket:str, 
        prefix:str, 
        ag_method: AggregationMethod,
        refresh_time_s:int,
        rolling_average: int,
        max_patience:int,
        min_delta:int,
        monitor_options: List[MonitorOption]
        ):
        self.BUCKET = bucket
        self.PREFIX = prefix
        self.AG_METHOD = ag_method
        self.REFRESH_TIME_S = refresh_time_s
        self.ROLLING_AVERAGE = rolling_average
        self.MAX_PATIENCE = max_patience
        self.MIN_DELTA = min_delta
        self.MONITOR_OPTIONS = monitor_options


# Variables
current_best_results=CurrentBestResults()


def check_stats(
        options: EarlyStoppingArgs,
        current_best: CurrentBestResults,
    ) -> CurrentBestResults: 
    try:

        fh = S3FileHandler(bucket=options.BUCKET, prefix=options.PREFIX,
                   profile="minio", s3_endpoint_url="http://localhost:9000")
        tm = metrics.TrainingMetrics(options.BUCKET, model_name=options.PREFIX, profile='minio', s3_endpoint_url='http://localhost:9000')

        log = DeepRacerLog(filehandler=fh)
      
        log.load(force=True)

        df = log.dataframe()
      
        train=tm.getTraining()

        summary_df=tm.getSummary(method=str(options.AG_METHOD), summary_index=['r-i','master_iteration'])
        
        train_completion = summary_df['train_completion']
        eval_completion = summary_df['eval_completion']
        average_completion = summary_df[['train_completion','eval_completion']].mean(axis='columns')
        train_reward = summary_df['train_reward']
        eval_reward = summary_df['eval_reward']

        summary_df['train_reward_completion'] = (train_completion / 100) * train_reward
        summary_df['eval_reward_completion'] = (eval_completion / 100) * eval_reward
        
        simulation_agg = au.simulation_agg(df, secondgroup="unique_episode")
        complete_laps = simulation_agg[simulation_agg['progress']==100]
        time_complete_rolling_av = complete_laps['time'].rolling(options.ROLLING_AVERAGE).mean()
        
        
        model_improved=False
        improvements=[]
        monitor_options=options.MONITOR_OPTIONS
        
        ## Check for improvement
        if MonitorOption.FASTEST_LAP in monitor_options:
            model_improved = check_fastest_lap_improved(complete_laps, current_best.lap_time_s)
            improvements.append(MonitorOption.FASTEST_LAP )
            
        if MonitorOption.CONSISTENCY in monitor_options:
            model_improved = check_consistency_improved(time_complete_rolling_av, current_best.consistency_deviation)
            improvements.append(MonitorOption.CONSISTENCY)

        if MonitorOption.COMPLETION_RATE in monitor_options:
            model_improved = check_completion_rate_improved(average_completion, current_best.completion_rate)
            improvements.append(MonitorOption.COMPLETION_RATE)
        
        if MonitorOption.TRAIN_REWARD in monitor_options:
            model_improved = check_reward_improved(train_reward, current_best.train_reward)
            improvements.append(MonitorOption.TRAIN_REWARD)
        
        if MonitorOption.EVALUATION_REWARD in monitor_options:
            model_improved = check_reward_improved(eval_reward, current_best.train_reward)
            improvements.append(MonitorOption.TRAIN_REWARD)
            
        if model_improved:
            patience = options.MAX_PATIENCE
            logging.info(f'No improvement. Patience remaining: {patience}')
        else:    
            if current_best.patience > 0:
                current_best.patience -= 1
                logging.info(f'No improvement. Patience remaining: {current_best.patience }')
            else:
                logging.info('Patience expired. Stopping training')
                ## Stop the training docker container by exiting the container with a non-zero exit code
                exit(1)
                
        return current_best_results

    except Exception as e:
      logging.error('Logs not found. Trying again after {0} seconds'.format(options.REFRESH_TIME_S))
      logging.error('The exception was: ', e)
      
      return current_best_results




def check_fastest_lap_improved(complete_laps: pd.DataFrame, current_fastest_s: float ) -> ImprovementCheck:
    fastest_lap = get_fastest_lap(complete_laps)
    has_improved = fastest_lap < current_fastest_s
    metric="Fastest lap"
    log_improvement(has_improved, metric)
    return ImprovementCheck(has_improved, min(fastest_lap, current_fastest_s))

def log_improvement(has_improved:bool, metric: str):
    message=f'{metric} did {"" if has_improved else "not "}improve'
    logging.info(message)


def get_fastest_lap(complete_laps: pd.DataFrame) -> float:
    fastest_lap = complete_laps['time'].min()
    fastest_lap_iteration = complete_laps['master_iteration'].loc[complete_laps['time'].idxmin()]
    logging.info(f'Fastest lap: {fastest_lap} seconds at iteration {fastest_lap_iteration}')
    return fastest_lap
        

def check_consistency_improved(complete_times: pd.Series, current_best_consistency: float) -> ImprovementCheck:
    """Check if the consistency of the model has improved by comparing the standard deviation of the time to complete a lap"""
    standard_deviation = complete_times.std()
    logging.info(f'STD: {standard_deviation}, Mean: {complete_times.mean()}, Current best STD: {current_best_consistency}')
    has_improved = standard_deviation < current_best_consistency
    log_improvement(has_improved, 'Consistency')
    return ImprovementCheck(has_improved, min(standard_deviation, current_best_consistency))
    
    
def check_completion_rate_improved(average_completion: pd.Series, new_best_completion: float) -> ImprovementCheck:
    """Check if the completion rate of the model has improved by comparing the average completion rate of the training or evaluation runs"""
    current_best_completion = average_completion.max()
    logging.info(f'Current: {current_best_completion}%, New best completion rate: {new_best_completion}%')
    has_improved = new_best_completion > current_best_completion
    log_improvement(has_improved, 'Completion rate')
    return ImprovementCheck(has_improved, max(new_best_completion, current_best_completion))
 
    
def check_reward_improved(reward_ds: pd.Series, current_max_reward:float) -> ImprovementCheck:
    max_reward= reward_ds.max()
    has_improved = max_reward > current_max_reward
    log_improvement(has_improved, 'Reward')
    return ImprovementCheck(has_improved, max(max_reward, current_max_reward))
    
    
if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()

    ## Add parser arguments
    parser.add_argument('--min-check', type=int, default=1, help='Number of time in minutes to wait before checking for improvement')
    parser.add_argument('--patience', type=int, default=10, help='Number of checks to wait for improvement before stopping training')
    parser.add_argument('--min-delta', type=float, default=0.0, help='Minimum change in monitored value to qualify as improvement')
    parser.add_argument('--monitor', 
                        type=str, nargs='+', 
                        default=[MonitorOption.FASTEST_LAP, MonitorOption.CONSISTENCY,], 
                        help=f'Quantity to be monitored. Options: {[option.value for option in MonitorOption]}'
    )

    ## Storage
    parser.add_argument("-b", "--bucket", dest="bucket",
                        help="The name of the MinIO bucket",  type=str ,default="bucket")

    parser.add_argument("-p", "--prefix", dest="prefix",
                        help="The name of the prefix where the model is stored in the MinIO bucket (The model name)",  type=str ,default="rl-deepracer-sagemaker")

    # Data transformation
    parser.add_argument("-m", "--method", dest="method",
                        help="Statistical value to be calculated. Examples are 'mean', 'median','min' & 'max'. Default: 'mean'.",  type=str ,default="mean")
    parser.add_argument("-rav", "--rolling-average", dest="rolling_average",
                        help="The rolling average to use for the graph",  type=int)

    # Logging
    parser.add_argument('--log-level', type=lambda l:logging.getLevelName(l), default='INFO', help='Logging level')
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    args = vars(parser.parse_args())


    
    program_args=EarlyStoppingArgs(
        bucket=args.get('bucket', 'bucket'),
        prefix=args.get('prefix', 'rl-deepracer-sagemaker'),
        ag_method=AggregationMethod(args.get('method')),
        refresh_time_s=args.get('min_check', 0) * 60,
        rolling_average=args.get('rolling_average', 0),
        max_patience=args.get('patience', 10),
        min_delta=args.get('min_delta', 0),
        monitor_options=args.get('monitor',[])
    )
    
    while True:
        best_results=check_stats(program_args, current_best_results)
        current_best_results=best_results
        time.sleep(program_args.REFRESH_TIME_S)