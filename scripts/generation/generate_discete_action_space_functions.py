from functools import reduce
from xmlrpc.client import Boolean
import numpy as np
import math


def create_full_speed_angle_actions(full_speed_angle_range: np.array, speed_range: np.array,) -> list:
    return reduce(lambda x, y: x + y, [
        create_actions_for_speeds(speed_range, angle) for angle in full_speed_angle_range
    ]) + reduce(lambda x, y: x + y, [
        create_actions_for_speeds(speed_range, -angle) for angle in full_speed_angle_range
    ])


def create_actions_for_speeds(speed_range: np.array, angle: float, is_left=True) -> list:
    actions = []
    for speed in speed_range:
        actions.append({
            "steering_angle": angle if is_left else -angle,
            "speed": speed
        },)
    return actions


def create_direction_actions(steering_range: np.array, speed_range: np.array, is_left: Boolean) -> list:

    if 0 in steering_range:
        raise Exception(
            'A steering range of "0" should not be used in the "create_direction_actions" to make actions')

    actions = []

    angles_top_speed_index_map = get_top_speed_index_map(
        steering_range, len(speed_range))

    for steer_angle in steering_range:
        steer_angle_speed_index = angles_top_speed_index_map[steer_angle]
        speed_range_remaining = speed_range[:steer_angle_speed_index+1]

        actions.extend(create_actions_for_speeds(
            speed_range_remaining, steer_angle, is_left))

    return actions


def get_top_speed_index_map(remaining_angles: np.array, amount_of_speeds: int) -> dict:
    """Gets a a map with steering angle and max speed index from another array

    Args:
        remaining_angles (np.array): The angles to map to the speed indexes
        amount_of_speeds (int): Amount of speed indexes that need to be referenced to

    Returns:
        dict: With each key with the angle and the corresponding index reference
    of a speed list
    """
    angles_top_speed_index_map = {}

    amount_of_remaining_angles = len(remaining_angles)
    speed_index_step = amount_of_speeds/amount_of_remaining_angles

    for index, ang in enumerate(np.sort(remaining_angles)):
        angles_top_speed_index_map.update(
            {
                ang: math.floor((len(remaining_angles) - index)
                                * speed_index_step)
            })
    return angles_top_speed_index_map


def find_remaining_angles(steering_range: np.array, full_speed_angle: float) -> np.array:
    return steering_range[steering_range > full_speed_angle]


def find_nearest(array, value):
    idx = find_nearest_idx(array, value)
    return array[idx]


def find_nearest_idx(array, value) -> int:
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx


def get_full_range(start: float, stop: float, step: float) -> np.array:
    return np.arange(start, stop + step, step)

# def show_action_space
