import argparse
import os
import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError, OperationalError
import time


parser = argparse.ArgumentParser()

parser.add_argument("-s", "--system-env-path", dest="system_env_path",
                    help="The path location for the file with system environment variables", metavar="system_env_path", default=f'./system.env')

parser.add_argument("-r", "--run-env-path", dest="run_env_path",
                    help="The path location for the file with run environment variables", metavar="run_env_path", default=f'./run.env')

parser.add_argument("-u", "--user", dest="db_username",
                    help="The username for the database", metavar="db_username", default='postgres')

parser.add_argument("-pw", "--password", dest="db_password",
                    help="The password for the database", metavar="db_password", default='password')

parser.add_argument("-p", "--port", dest="db_port",
                    help="The port of the db", metavar="db_port", default=5432)

parser.add_argument("-n", "--name", dest="db_name",
                    help="The name of the db", metavar="db_name", default='deep-racer-logs')


args = vars(parser.parse_args())

pg = None
Session = None

max_attempts = 10  # Maximum number of connection attempts
sleep_seconds = 5  # Time to wait between each attempt

for attempt in range(max_attempts):
    try:
        pg = create_engine(f"postgresql://{args['db_username']}:{args['db_password']}@postgresdb:{args['db_port']}/{args['db_name']}", echo=True)
        pg.connect()
        Session = sessionmaker(bind=pg)
        print("Database connection successful.")
        break
    except OperationalError:
        print(f"Database connection failed. Retrying in {sleep_seconds} seconds ({attempt+1}/{max_attempts})...")
        time.sleep(sleep_seconds)
else:
    print("Max connection attempts reached. Exiting.")
    exit(1)


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
    env_vars = {} # or dict {}session
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


# Function to execute SQL file
def execute_sql_file(engine, sql_file_path):
    with open(sql_file_path, 'r') as f:
        sql_commands = f.read().split(';')
        for command in sql_commands:
            if command.strip():
                try:
                    engine.execute(command)
                except SQLAlchemyError as e:
                    print(f"An error occurred while executing SQL command: {e}")
    
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

print('----------- Run Vars --------------')
for key, value in run_vars.items():
    print(f'{key} = {value}')
    
print('----------- System Vars --------------')
for key, value in system_vars.items():
    print(f'{key} = {value}')
      
custom_files_folder = f'./custom_files/'

with open(f'{custom_files_folder}/hyperparameters.json', 'r') as f:
    hyperparameters = json.load(f)
    print('----------- Adding hyper params to table --------------', hyperparameters)

    columns = ', '.join(hyperparameters.keys())
    placeholders = ', '.join([f':{key}' for key in hyperparameters.keys()])
    query = f"INSERT INTO hyperparameters ({columns}) VALUES ({placeholders}) ON CONFLICT DO NOTHING;"

    with Session() as session:
            result = session.execute(text(query), hyperparameters)       
            session.commit()


with open(f'{custom_files_folder}/model_metadata.json', 'r') as f:
    print('----------- Adding model meta data to table --------------')
    model_metadata = json.load(f)

with open(f'{custom_files_folder}/reward_function.py', 'r') as f:
    print('----------- Adding reward function to the table --------------')
    lines = f.readlines()
