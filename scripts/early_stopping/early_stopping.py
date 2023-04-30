import logging
import time
from enum import Enum
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

class CurrentBestResults:
    def __init__(self):
        self.fastest_lap_s = math.inf
        self.best_consistency_deviation = math.inf
        self.best_completion_rate = -math.inf
        self.max_reward = -math.inf

    def update_fastest_lap(self, new_fastest_lap_s: float):
        self.fastest_lap_s = new_fastest_lap_s

    def update_best_consistency_deviation(self, new_best_consistency_deviation: float):
        self.best_consistency_deviation = new_best_consistency_deviation

    def update_best_completion_rate(self, new_best_completion_rate: float):
        self.best_completion_rate = new_best_completion_rate

    def update_max_reward(self, new_max_reward: float):
        self.max_reward = new_max_reward

# Variables
current_best_results=CurrentBestResults()


def check_stats(monitor: MonitorOption, summary_df: pd.DataFrame, current_best: float): 
    global patience, MIN_DELTA, current_fastest_lap_s
    try:

        fh = S3FileHandler(bucket=BUCKET, prefix=PREFIX,
                   profile="minio", s3_endpoint_url="http://localhost:9000")
        tm = metrics.TrainingMetrics(BUCKET, model_name=PREFIX, profile='minio', s3_endpoint_url='http://localhost:9000')

        log = DeepRacerLog(filehandler=fh)
      
        log.load(force=True)

        df = log.dataframe()
      
        train=tm.getTraining()

        summary_df=tm.getSummary(method=AG_METHOD, summary_index=['r-i','master_iteration'])
        
        train_completion = summary_df['train_completion']
        eval_completion = summary_df['eval_completion']
        average_completion = summary_df[['train_completion','eval_completion']].mean(axis='columns')
        train_reward = summary_df['train_reward']
        eval_reward = summary_df['eval_reward']

        summary_df['train_reward_completion'] = (train_completion / 100) * train_reward
        summary_df['eval_reward_completion'] = (eval_completion / 100) * eval_reward
        
        simulation_agg = au.simulation_agg(df, secondgroup="unique_episode")
        complete_laps = simulation_agg[simulation_agg['progress']==100]
        time_complete_rolling_av = complete_laps['time'].rolling(ROLLING_AVERAGE).mean()
        
        
        model_improved=False
        improvements=[]
        
        ## Check for improvement
        if MonitorOption.FASTEST_LAP in MONITOR:
            model_improved = check_fastest_lap_improved(complete_laps, current_fastest_lap_s)
            improvements.append(MonitorOption.FASTEST_LAP )
            
        if MonitorOption.CONSISTENCY in MONITOR:
            model_improved = check_consistency_improved(time_complete_rolling_av, MIN_DELTA)
            improvements.append(MonitorOption.CONSISTENCY)

        if MonitorOption.COMPLETION_RATE in MONITOR:
            model_improved = check_completion_rate_improved(average_completion, MIN_DELTA)
            improvements.append(MonitorOption.COMPLETION_RATE)
        
        if MonitorOption.TRAIN_REWARD in MONITOR:
            model_improved = check_reward_improved(summary_df, MIN_DELTA)
            improvements.append(MonitorOption.TRAIN_REWARD)
            
        if model_improved:
            patience = MAX_PATIENCE
            logging.info(f'No improvement. Patience remaining: {patience}')
        else:    
            if patience > 0:
                patience -= 1
                logging.info(f'No improvement. Patience remaining: {patience}')
            else:
                logging.info('Patience expired. Stopping training')
                ## Stop the training docker container by exiting the container with a non-zero exit code
                exit(1)

    except Exception as e:
      logging.error('Logs not found. Trying again after {0} seconds'.format(REFRESH_TIME_S))
      logging.error('The exception was: ', e)




def check_fastest_lap_improved(complete_laps: pd.DataFrame, current_fastest_s: float ) -> bool:
        fastest_lap = get_fastest_lap(complete_laps)
        if fastest_lap < current_fastest_s:
            current_fastest_s = fastest_lap
            logging.info('Fastest lap improved')
            return True
        else:
            logging.info('Fastest lap did not improve')
            return False


def get_fastest_lap(complete_laps: pd.DataFrame) -> float:
    fastest_lap = complete_laps['time'].min()
    fastest_lap_iteration = complete_laps['master_iteration'].loc[complete_laps['time'].idxmin()]
    logging.info(f'Fastest lap: {fastest_lap} seconds at iteration {fastest_lap_iteration}')
    return fastest_lap
        

def check_consistency_improved(complete_times: pd.Series, current_best_consistency: int) -> bool:
    """Check if the consistency of the model has improved by comparing the standard deviation of the time to complete a lap"""
    consistency = complete_times.std()
    logging.info(f'Consistency: {consistency}')
    if consistency < current_best_consistency:
        logging.info('Consistency improved')
        return True
    else:
        logging.info('Consistency did not improve')
        return False
    
    
def check_completion_rate_improved(average_completion: pd.Series, current_best_completion: int) -> bool:
    """Check if the completion rate of the model has improved by comparing the average completion rate of the training or evaluation runs"""
    completion_rate = average_completion.max()
    logging.info(f'Completion rate: {completion_rate}')
    if completion_rate > current_best_completion:
        logging.info('Completion rate improved')
        return True
    else:
        logging.info('Completion rate did not improve')
        return False
 
    
def check_reward_improved(reward_ds: pd.Series, current_max_reward:float) -> bool:
    max_reward= reward_ds.max()
    if max_reward > current_max_reward:
        logging.info('Reward improved')
        return True
    else:
        logging.info('Reward did not improve')
        return False
    
    
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

    # Constants
    BUCKET=args['bucket']
    PREFIX=args['prefix']
    AG_METHOD = args.get('method')
    REFRESH_TIME_S = args.get('min_check', 0) * 60
    ROLLING_AVERAGE = args.get('rolling_average')
    MAX_PATIENCE = args.get('patience',0)
    MIN_DELTA = args.get('min_delta', 0)
    MONITOR = args.get('monitor',[])
    while True:
        check_stats()
        time.sleep(REFRESH_TIME_S)