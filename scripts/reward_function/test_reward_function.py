import random
import numpy as np
from argparse import ArgumentParser
import argparse
import matplotlib.pyplot as plt
import sys
import os


parser = ArgumentParser(
    description='''
        Run Tests on the given reward function
        
        Examples: 
        - Test steering angle reward: > dr-test-reward-function -p steering_angle -v 45 -sh
        - Test distance from center reward: > dr-test-reward-function -p distance_from_center -v 50 -tw 100 -sh
        - Test progress reward: > dr-test-reward-function -p progress -v 100 -sh
        - Test speed reward: > dr-test-reward-function -p speed -v 5 -sh
    ''',
)

parser.add_argument("-f", "--file", dest="file",
                    help="The path to the reward file for testing", type=str, metavar="file_path", default='/home/aj/aws-deep-racer/deepracer-for-cloud/custom_files')

parser.add_argument("-t", "--tests", dest="tests",
                    help="The number of tests to carry out", type=int, default=3)

parser.add_argument("-v", "--value", dest="value",
                    help="The value of the parameter to test", type=int, default=0)

parser.add_argument("-p", "--param", dest="param",
                    help="The numeric parameter to test", type=str, default=None)

parser.add_argument("-r", "--random-seed", dest="random_seed",
                    help="The random seed for the random parameters", type=int, default=1)

parser.add_argument("-sh", "--show",
                    help="View the result in the graph", dest='show', action='store_true')

parser.add_argument("-tw", "--track-width",
                    help="Set the width of the track", dest='track_width', type=int, default=1)
 
 


args = vars(parser.parse_args())

reward_file_path = args['file']

value = args['value']
param = args['param']
show = args.get('show')
track_width = args.get('track_width')
print(args)

random.seed(args['random_seed'])

reward_file_directory = os.path.dirname(reward_file_path).replace('\'', '')

# sys.path.insert(1, reward_file_directory)
sys.path.insert(0, reward_file_directory)


from reward_function import reward_function

tests = args['tests']


def create_random_params() -> dict:
    
    track_width = random.uniform(5, 10)
    distance_from_center = random.uniform(0, track_width/2)
    
    
    return {
        # flag to indicate if the agent is on the track
        "all_wheels_on_track": True,
        # agent's x-coordinate in meters
        "x": random.uniform(0, 75.5),
        # agent's y-coordinate in meters
        "y": random.uniform(0, 75.5),
        # zero-based indices of the two closest objects to the agent's current position of (x, y).
        "closest_objects": [random.randint(0, 9), random.randint(0, 9)],
        # indices of the two nearest waypoints.
        "closest_waypoints": [random.randint(0, 9), random.randint(0, 9)],
        # distance in meters from the track center
        "distance_from_center": distance_from_center,
        # Boolean flag to indicate whether the agent has crashed.
        "is_crashed": bool(random.getrandbits(1)),
        # Flag to indicate if the agent is on the left side to the track center or not.
        "is_left_of_center": bool(random.getrandbits(1)),
        # Boolean flag to indicate whether the agent has gone off track.
        "is_offtrack": bool(random.getrandbits(1)),
        # flag to indicate if the agent is driving clockwise (True) or counter clockwise (False).
        "is_reversed": bool(random.getrandbits(1)),
        # agent's yaw in degrees
        "heading": random.uniform(0, 360),
        # list of the objects' distances in meters between 0 and track_length in relation to the starting line.
        "objects_distance": np.random.uniform(0, 360),
        # list of the objects' headings in degrees between -180 and 180.
        "objects_heading": np.random.uniform(0, 360),
        # list of Boolean flags indicating whether elements' objects are left of the center (True) or not (False).
        "objects_left_of_center": [bool(random.getrandbits(1)), ] * 5,
        # list of object locations [(x,y), ...].
        "objects_location": [(random.uniform(0, 75.5),  random.uniform(0, 75.5)), ],
        # list of the objects' speeds in meters per second.
        "objects_speed": [random.uniform(0, 75.5), ],
        # percentage of track completed
        "progress":  random.uniform(0, 100),
        # agent's speed in meters per second (m/s)
        "speed":  random.uniform(0, 5),
        # agent's steering angle in degrees
        "steering_angle": random.uniform(-45, 45),
        # number steps completed
        "steps": random.randint(0, 2000),
        # track length in meters.
        "track_length": random.uniform(12, 100),
        # width of the track
        "track_width": track_width,
        # list of (x,y) as milestones along the track center
        "waypoints": [(random.uniform(5, 10), random.uniform(5, 10)), ] * 100
    }


results = []

params = create_random_params()
if track_width is not None:
    params['track_width'] = track_width



if param is None:
    print('Testing Random Parameters')
    for test in range(0, tests):
        results.append({
            'params': params,
            'reward': reward_function(params)
        })

else:
    print(f'Testing "{param}" up to:', value)
    for val in range(0, value, 1):
        params[param] = val
        results.append({
            param: val,
            'reward': reward_function(params)
        })


print(f'\nThe reward results are\n',)

for result in results:
    for key, value in result.items():
        if key != 'params':
            print(f'{key}:', value)

if show is True:
    plt.title(f'{param} vs Reward')
    plt.plot(list(map(lambda x: x['reward'] ,results)))
    plt.xlabel(param)
    plt.ylabel('Reward')
    plt.show()