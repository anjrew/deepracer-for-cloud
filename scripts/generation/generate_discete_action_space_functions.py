import numpy as np
import math


def create_actions_for_speeds(speed_range: np.array, angle: float) -> list:
    actions = []
    for speed in speed_range:
        actions.append({
            "steering_angle": angle,
            "speed": speed
        },)
    return actions


def create_direction_actions(steering_range: np.array, speed_range: np.array, full_speed_angle: int, speed_step: float) -> list:
    
    if 0 in steering_range: 
        raise Exception('A steering range of "0" should not be used in the "create_direction_actions" to make actions')

    bottom_speed = speed_range[0]

    actions = []
    for angle in steering_range:
        if angle <= full_speed_angle:
            actions.extend(create_actions_for_speeds(speed_range, angle))
        else:
            remaining_angles = find_remaining_angles(
                steering_range, full_speed_angle)

            amount_of_speeds = len(speed_range)
            angles_top_speed_index_map = get_top_speed_index_map(remaining_angles, amount_of_speeds)

            for steer_angle in remaining_angles:
                speed_range_remaining = np.arange(
                    bottom_speed, angles_top_speed_index_map[steer_angle], speed_step)

                actions.extend(create_actions_for_speeds(
                    speed_range_remaining, steer_angle))

    return actions


def get_top_speed_index_map(remaining_angles:np.array, amount_of_speeds: int) -> dict:
    angles_top_speed_index_map = {}

    amount_of_remaining_angles = len(remaining_angles)
    speed_index_step = amount_of_speeds/amount_of_remaining_angles

    for index, ang in enumerate(remaining_angles):

        angles_top_speed_index_map.update(
            {ang: math.ceil(index * speed_index_step)})


def find_remaining_angles(steering_range: np.array, full_speed_angle: float) -> np.array:
    idx = find_nearest_idx(steering_range, full_speed_angle)
    return steering_range[idx:]


def find_nearest(array, value):
    idx = find_nearest_idx(array, value)
    return array[idx]


def find_nearest_idx(array, value) -> int:
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx
