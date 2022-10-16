from argparse import ArgumentParser
from functools import reduce
import numpy as np
import generate_discete_action_space_functions as fn
import matplotlib.pyplot as plt
import json



class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


parser = ArgumentParser()
parser.add_argument("-i", "--input", dest="input",
                    help="The path of the input file to be converted", metavar="file_path")
parser.add_argument("-o", "--output", dest="output",
                    help="The output path destination of the new file",  metavar="file_path")
parser.add_argument("-v", "--view", dest="view", action="store_true",
                    help="Show the action space in a graph")

args = vars(parser.parse_args())

# Opening JSON file
input_file = open(args['input'])
# input_file = open('./config/discreate-action-space-config.json')
# # returns JSON object as
# # a dictionary
meta_data = json.load(input_file)

action_space = meta_data['action_space']
speed = action_space['speed']
speed_step = speed['step']
steering_angle = action_space['steering_angle']
steering_step = steering_angle['step']
full_speed_angle = steering_angle['full_speed_angle']
top_speed = speed['high']
bottom_speed = speed['low']
left = steering_angle['high']
right = steering_angle['low']


left_range = fn.get_full_range(
    full_speed_angle, abs(left), abs(left)/steering_step)[1:]

right_range = fn.get_full_range(
    full_speed_angle, abs(right), abs(right)/steering_step)[1:]

speed_range: np.array = fn.get_full_range(
    bottom_speed, top_speed, (top_speed-bottom_speed) / speed_step)

full_speed_angle_range = fn.get_full_range(
    0, full_speed_angle, full_speed_angle - min(len(left_range), len(right_range)))
 

corner_speed_range = speed_range[:-1]
actions = [
    fn.create_full_speed_angle_actions(full_speed_angle_range, speed_range),
    # Create all speeds for angle of 0deg
    fn.create_direction_actions(left_range, corner_speed_range, True),
    # Create left actions
    fn.create_direction_actions(right_range, corner_speed_range, False)
    # Create right actions
]

actions = reduce(lambda x, y: x + y, actions)

meta_data['action_space_type'] = 'discrete'
meta_data['action_space'] = list(actions)

# if True == True:
if args['view'] == True:
    print('Creating action space graph')
    x = []
    y = []
    for ang in actions:
        x.append(int(ang['steering_angle']))
        y.append(int(ang['speed']))
    plt.scatter(x, y)
    plt.show()

output_path = args['output']
with open(output_path, 'w') as input_file:
    json.dump(meta_data, input_file, indent=2, cls=NpEncoder)
    print("New json file created at ", output_path)
