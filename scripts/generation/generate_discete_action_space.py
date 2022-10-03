from argparse import ArgumentParser
from functools import reduce
import numpy as np
import generate_discete_action_space_functions as fn
import json
import math


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

args = vars(parser.parse_args())

# Opening JSON file
input_file = open(args['input'])
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


left_range = np.arange(0, left, steering_step)[1:]
right_range = np.arange(0, right, steering_step)[1:]
speed_range = np.arange(bottom_speed, top_speed, speed_step)

actions = [
    # Create all speeds for angle of 0deg
    fn.create_actions_for_speeds(speed_range, 0),
    # Create left actions
    fn.create_direction_actions(left_range, speed_range, full_speed_angle, speed_step, True),
    # Create right actions
    fn.create_direction_actions(right_range, speed_range, full_speed_angle, speed_step, False)  
]

actions = reduce(lambda x, y: x + y ,actions)


def create_full_speed_actions(speed_range: np.array, angle: float) -> list:
    actions = []
    for speed in speed_range:
        actions.append({
            "steering_angle": angle,
            "speed": speed
        },)
    return actions


def create_direction_actions(steering_range: np.array, speed_range: np.array) -> list:
    actions = []
    for i, angle in enumerate(steering_range):
        if angle <= full_speed_angle:
            actions.extend(create_full_speed_actions(speed_range, angle))
        else:
            remaining_ang_amount = i - (len(steering_range) - 1)
            remaining_angles = steering_range[remaining_ang_amount:]
            speed_list = list(speed_range)
            # angles_top_speed_map = [{'angle': ang, 'top_speed': min(enumerate(
            #     speed_list), key=lambda index, _: abs(i-index))} for i, ang in enumerate(remaining_angles)]

            angles_top_speed_index_map = {}

            amount_of_remaining_angles = len(remaining_angles)
            amount_of_speeds = len(speed_list)
            speed_index_step = amount_of_speeds/amount_of_remaining_angles

            for index, ang in enumerate(remaining_angles):

                angles_top_speed_index_map.update(
                    {ang: math.ceil(index * speed_index_step)})

            for steer_angle in remaining_angles:
                speed_range_x = np.arange(
                    bottom_speed, angles_top_speed_index_map[steer_angle], speed_step)

                actions.extend(create_full_speed_actions(
                    speed_range_x, steer_angle))


meta_data['action_space_type'] = 'discrete'
meta_data['action_space'] = list(actions)

output_path = args['output']
with open(output_path, 'w') as input_file:
    json.dump(meta_data, input_file, indent=2, cls=NpEncoder)
    print("New json file created at ", output_path)
