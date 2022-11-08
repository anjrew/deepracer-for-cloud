from typing import Dict, List
from xmlrpc.client import Boolean


def check_sensor_property(test: List) -> Boolean:
    """Checks the sesor property of a model metadata file

    Args:
        test (List(str)): The list of sensor values to check

    Returns:
        Boolean: True if it is valid and false if it is not
    """

    cameras = ["FRONT_FACING_CAMERA", "STEREO_CAMERAS"]
    options = ["LIDAR"] + cameras
    are_valid_sensors = all([
        any([o == s for o in options]) for s in test
    ])

    cameras_found = [x in test for x in cameras]
    only_one_camera = cameras_found.count(True) == 1
    return are_valid_sensors and only_one_camera


def check_neural_network_property(test: str) -> Boolean:
    """Check for valid neural network values

    Args:
        test (str): The neural network value to test

    Returns:
        Boolean: True if it is valid and False if it is not
    """
    net_options = ["DEEP_CONVOLUTIONAL_NETWORK",
                   "DEEP_CONVOLUTIONAL_NETWORK_SHALLOW", "DEEP_CONVOLUTIONAL_NETWORK_DEEP"]
    return test in net_options


def check_valid_action_space_property(val: str, action_space) -> Boolean:
    """Checks if for a valid action space label and if it matches the object shape

    Args:
        val (str): The label for the action space
        obj (Dict): The object shape for details of the action space

    Returns:
        Boolean: True if the action space parameters are valid and compatible
    """
    val_is_valid = val == 'continuous' or val == 'discrete'
    label = ''
    try:
        label = get_action_space_label(action_space)
    except:
        pass
    return val_is_valid and val == label


def get_action_space_label(action_space):
    """Gets a type label for an action space

    Args:
        action_space (Dict): The action space object

    Raises:
        Exception: If an invalid action space is provided

    Returns:
        str: The action space label
    """
    types = (float, int)
    try:
        speed_high_valid = isinstance(action_space['speed']['high'], types)
        speed_low_valid = isinstance(action_space['speed']['low'], types)
        angle_high_valid = isinstance(
            action_space['steering_angle']['high'], types)
        angle_low_valid = isinstance(
            action_space['steering_angle']['low'], types)
        if speed_high_valid \
                and speed_low_valid \
                and angle_high_valid \
                and angle_low_valid:
            return 'continuous'
        else:
            raise Exception('Invalid continuous action space')
    except:
        try:
            if isinstance(action_space, list) \
                and all([
                    isinstance(a, dict) and
                    isinstance(a['steering_angle'], types) and
                    isinstance(a['speed'], types)
                    for a in action_space]):
                return 'discrete'
        except:
            raise Exception(
                "Invalid action space provided. Could not give 'continuous' or 'discrete' label")


def no_multiple_same_action(action_space: list):
    """Checks weather there are actions that are the same in the action space

    Args:
        action_space (list): The action space to check

    Returns:
        bool: If no repeat actions where found
    """

    for x, action in enumerate(action_space):
        for y, action_compare in enumerate(action_space):
            if x != y:
                if action['speed'] == action_compare['speed'] and action['steering_angle'] == action_compare['steering_angle']:
                    raise Exception(f"Multiple of the same action was found with SPEED: {action['speed']} STEERING: {action['steering_angle']}")
                
    return True
