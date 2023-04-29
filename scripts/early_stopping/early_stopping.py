import logging
import time
from enum import Enum
import pandas as pd
import math
from argparse import ArgumentParser

import matplotlib.pyplot as plt

from deepracer.logs import metrics
from deepracer.logs import AnalysisUtils as au
from deepracer.logs import DeepRacerLog
from deepracer.logs import S3FileHandler


class MonitorOption(Enum):
    FASTEST_LAP = 'fastest_lap'
    CONSISTENCY = 'consistency'

parser = ArgumentParser()

## Add parser arguments
parser.add_argument('--min-check', type=int, default=1, help='Number of time in minutes to wait before checking for improvement')
parser.add_argument('--patience', type=int, default=10, help='Number of checks to wait for improvement before stopping training')
parser.add_argument('--min-delta', type=float, default=0.0, help='Minimum change in monitored value to qualify as improvement')
parser.add_argument('--monitor', type=str, nargs='+', default=[MonitorOption.FASTEST_LAP, MonitorOption.CONSISTENCY,], help='Quantity to be monitored')

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

# Variables
patience:int = MAX_PATIENCE
current_fastest_lap=math.inf

def check_stats(): 
    global patience, MIN_DELTA, current_fastest_lap
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
        
        ## Check for fastest lap
        if MonitorOption.FASTEST_LAP in MONITOR:
            model_improved = check_fastest_lap_improved(complete_laps, current_fastest_lap)
            
        if MonitorOption.CONSISTENCY in MONITOR:
            model_improved = check_consistency_improved(time_complete_rolling_av, MIN_DELTA)
                
            
        if model_improved:
            patience = MAX_PATIENCE
        else:    
            if patience > 0:
                patience -= 1
                logging.info(f'Patience remaining: {patience}')
            else:
                logging.info('Patience expired. Stopping training')
                ## Stop the training docker container by exiting the container with a non-zero exit code
                exit(1)

    except Exception as e:
      logging.error('Logs not found. Trying again after {0} seconds'.format(REFRESH_TIME_S))
      logging.error('The exception was: ', e)




def check_fastest_lap_improved(complete_laps: pd.DataFrame, current_fastest) -> bool:
        fastest_lap = complete_laps['time'].min()
        fastest_lap_iteration = complete_laps['master_iteration'].loc[complete_laps['time'].idxmin()]
        logging.info(f'Fastest lap: {fastest_lap} seconds at iteration {fastest_lap_iteration}')
        if fastest_lap < current_fastest:
            current_fastest = fastest_lap
            logging.info('Fastest lap improved')
            return True
        else:
            logging.info('Fastest lap did not improve')
            return False
        

def check_consistency_improved(time_complete_rolling_av: pd.DataFrame, min_delta: float) -> bool:
    consistency = time_complete_rolling_av.std()
    logging.info(f'Consistency: {consistency}')
    if consistency < min_delta:
        logging.info('Consistency improved')
        return True
    else:
        logging.info('Consistency did not improve')
        return False