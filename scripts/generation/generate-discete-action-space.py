from functools import reduce
import json
from argparse import ArgumentParser, Namespace
import numpy as np

parser = ArgumentParser()
parser.add_argument("-i", "--input", dest="input",
                    help="The path of the input file to be converted", metavar="file_path")
parser.add_argument("-o", "--output", dest="output",
                    help="The output path destination of the new file",  metavar="file_path")

args = vars(parser.parse_args())

# Opening JSON file
f = open(args['input'])

# # returns JSON object as
# # a dictionary
meta_data = json.load(f)

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

actions = []

left_range = range(0, left, steering_step)
right_range = range(0, right, steering_step)
speed_range = range(bottom_speed, top_speed, speed_step)


def get_angles_top_speed(prev: dict, ang, speeds: list(int)) -> dict:
    prev.update(
        {ang: min(enumerate(speeds), key=lambda index, _: abs(i-index))})
    return prev


for i, angle in enumerate(left_range):
    if angle < full_speed_angle:
        for speed in speed_range:
            actions.append({
                "steering_angle": angle,
                "speed": speed
            },)
    else:
        remaining_ang_amount = i - (len(left_range) - 1)
        remaining_angles = left_range[remaining_ang_amount:]
        speed_list = list(speed_range)
        # angles_top_speed_map = [{'angle': ang, 'top_speed': min(enumerate(
        #     speed_list), key=lambda index, _: abs(i-index))} for i, ang in enumerate(remaining_angles)]

        angles_top_speed_map = reduce(
            lambda prev, next: get_angles_top_speed(prev, next, speed_list))

        for steer_angle in remaining_angles:
            speed_range_x = range(
                bottom_speed, angles_top_speed_map[steer_angle], speed_step)
            for speed in speed_range_x:
                actions.append({
                    "steering_angle": steer_angle,
                    "speed": speed
                },)

meta_data['action_space_type'] = 'discrete'
meta_data['action_space'] = action_space

with open('new_file.json', 'w') as f:
    json.dump(meta_data, f, indent=2)
    print("New json file is created from data.json file")
# # Iterating through the json
# # list
# for i in data['emp_details']:
#     print(i)

# # Closing file
# f.close()
