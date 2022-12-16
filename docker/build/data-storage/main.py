import pandas as pd
import numpy as np
import argparse
import os
import json
from sqlalchemy import create_engine



DIR = os.getenv('DR_DIR',os.path.dirname(os.path.realpath(__file__) + '/../../../..'))


parser = argparse.ArgumentParser()

parser.add_argument("-s", "--system-env-path", dest="system_env_path",
                    help="The path location for the file with system environment variables", metavar="system_env_path", default=f'{DIR}/system.env')

parser.add_argument("-r", "--run-env-path", dest="run_env_path",
                    help="The path location for the file with run environment variables", metavar="run_env_path", default=f'{DIR}/run.env')

parser.add_argument("-u", "--user", dest="db_username",
                    help="The username for the database", metavar="db_username", default='admin')

parser.add_argument("-pw", "--password", dest="db_password",
                    help="The password for the database", metavar="db_password", default='admin')

parser.add_argument("-p", "--port", dest="db_port",
                    help="The port of the db", metavar="db_port", default=5432)

parser.add_argument("-n", "--name", dest="db_name",
                    help="The name of the db", metavar="db_name", default=5432)


args = vars(parser.parse_args())

pg = create_engine(f"postgresql://{args['db_username']}:{args['db_password']}@postgresdb:{args['db_port']}/{args['db_name']}", echo=True)


run_env_path=args['system_env_path']
system_env_path=args['run_env_path']

def parse_value(val: str):
    """Maps a string value to the best matching type of value

    Args:
        val (str): The original string value

    Returns:
        str|int|float|boolean: The best matching type of value
    """
    val = val.replace('\'','')
    if val == 'True':
        return True
    elif val == 'False':
        return False
    elif val.isnumeric():
        num = float(val)
        return int(num) if num.is_integer() else val
    else:
        return val
    
def get_env_file_data(abs_path: str):
    env_vars = {} # or dict {}
    with open(abs_path) as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            # if 'export' not in line:
            #     continue
            # Remove leading `export `, if you have those
            # then, split name / value pair
            # key, value = line.replace('export ', '', 1).strip().split('=', 1)
            key, value = line.strip().split('=', 1)
            # os.environ[key] = value  # Load to local environ
            # env_vars[key] = value # Save to a dict, initialized env_vars = {}
            env_vars[key.lower().replace('dr_', '')] = parse_value(value) # Save to a list
    return env_vars

    
run_vars = get_env_file_data(run_env_path)

system_vars = get_env_file_data(system_env_path)

keys_of_interest = set([
    'gui_enable'
    'sagemaker_image'
    'robomaker_image'
    'coach_image',
    'workers',
    'docker_style',
    'host_x',
    'local_s3_image',
    'run_id',
    'world_name',
    'race_type',
    'enable_domain_randomization',
    'eval_opp_s3_model_prefix',
    'train_change_start_position',
    'train_alternate_driving_direction',
    'train_start_position_offset',
    'train_round_robin_advance_dist',
    'train_multi_config',
    'local_s3_model_prefix',
    'local_s3_pretrained',
    'local_s3_pretrained_prefix',
    'local_s3_pretrained_checkpoint',
    'oa_number_of_obstacles',
    'oa_min_distance_between_obstacles',
    'oa_randomize_obstacle_locations',
    'oa_is_obstacle_bot_car',
    'oa_object_positions',
    'h2b_is_lane_change',
    'h2b_lower_lane_change_time',
    'h2b_upper_lane_change_time',
    'h2b_lane_change_distance',
    'h2b_number_of_bot_cars',
    'h2b_min_distance_between_bot_cars',
    'h2b_randomize_bot_car_locations',
    'h2b_bot_car_speed',
    'h2b_bot_car_penalty'
])

    
for key, value in run_vars.items():
    print(f'{key} = {value}')
    
for key, value in system_vars.items():
    print(f'{key} = {value}')
      
custom_files_folder = f'{DIR}/custom_files/'

with open(f'{custom_files_folder}/hyperparameters.json', 'r') as f:
  hyperparameters = json.load(f)
  query = """INSERT INTO hyperparameters 
            (id, text, compound_score, pos_score, neg_score, neu_score, cleaned_text, username, user_id)
            VALUES 
            (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;"""

#   pg.execute(query, (tweet_id, text, compound, pos, neg, neu, cleaned_text,user_info['username'], user_info['id'])) 
    
with open(f'{custom_files_folder}/model_metadata.json', 'r') as f:
  model_metadata = json.load(f)

with open(f'{custom_files_folder}/reward_function.py', 'r') as f:
    lines = f.readlines()
    
# Output: {'name': 'Bob', 'languages': ['English', 'French']}
# print(data)
