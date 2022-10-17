import random
from faker import Faker
import numpy as np
from argparse import ArgumentParser
import sys
import os


parser = ArgumentParser()

parser.add_argument("-f", "--file", dest="file",
                    help="The path to the reward file for testing", type=str, metavar="file_path", default='/home/aj/aws-deep-racer/deepracer-for-cloud/custom_files')

parser.add_argument("-t", "--tests", dest="tests",
                    help="The number of tests to carry out", type=int, default=3)

args = vars(parser.parse_args())

reward_file_path = args['file']

reward_file_directory = os.path.dirname(reward_file_path)

sys.path.insert(1, reward_file_directory)

from reward_function import reward_function

tests = args['tests']

fake = Faker()

def create_random_params() -> dict:
    return {
        "all_wheels_on_track": True,                                         # flag to indicate if the agent is on the track
        "x": random.uniform(0, 75.5),                                                               # agent's x-coordinate in meters
        "y": random.uniform(0, 75.5),                                                               # agent's y-coordinate in meters
        "closest_objects": [random.randint(0, 9), random.randint(0, 9)],                            # zero-based indices of the two closest objects to the agent's current position of (x, y).
        "closest_waypoints": [random.randint(0, 9), random.randint(0, 9)],                          # indices of the two nearest waypoints.
        "distance_from_center": random.uniform(0, 75.5),                                            # distance in meters from the track center 
        "is_crashed": bool(random.getrandbits(1)),                                                  # Boolean flag to indicate whether the agent has crashed.
        "is_left_of_center": bool(random.getrandbits(1)),                                           # Flag to indicate if the agent is on the left side to the track center or not. 
        "is_offtrack": bool(random.getrandbits(1)),                                                 # Boolean flag to indicate whether the agent has gone off track.
        "is_reversed": bool(random.getrandbits(1)),                                                 # flag to indicate if the agent is driving clockwise (True) or counter clockwise (False).
        "heading": random.uniform(0, 360),                                                          # agent's yaw in degrees
        "objects_distance": np.random.uniform(0, 360),                                              # list of the objects' distances in meters between 0 and track_length in relation to the starting line.
        "objects_heading": np.random.uniform(0, 360),                                               # list of the objects' headings in degrees between -180 and 180.
        "objects_left_of_center": [bool(random.getrandbits(1)), ] * 5,                              # list of Boolean flags indicating whether elements' objects are left of the center (True) or not (False).
        "objects_location": [( random.uniform(0, 75.5),  random.uniform(0, 75.5)),],                # list of object locations [(x,y), ...].
        "objects_speed": [ random.uniform(0, 75.5), ],                                              # list of the objects' speeds in meters per second.
        "progress":  random.uniform(0, 100),                                                        # percentage of track completed
        "speed":  random.uniform(0, 5),                                                             # agent's speed in meters per second (m/s)
        "steering_angle": random.uniform(-45, 45),                                                  # agent's steering angle in degrees
        "steps": random.randint(0, 2000),                                                           # number steps completed
        "track_length": random.uniform(12, 100),                                                    # track length in meters.
        "track_width": random.uniform(5, 10),                                                       # width of the track
        "waypoints": [(random.uniform(5, 10), random.uniform(5, 10)), ] * 100                       # list of (x,y) as milestones along the track center
    }
 

results = []   
    
for test in range(0, tests):
    params = create_random_params()
    results.append({
        'params': params,
        'reward': reward_function(params)
    })

print(f'\nThe reward results are\n',)

for result in results:
    print('\nA reward was given:', result['reward'])
    for key, value in result['params'].items():
        if key != 'waypoints':
            print(f'{key}:', value)