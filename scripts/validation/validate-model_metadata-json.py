import json
from argparse import ArgumentParser, Namespace
from typing import Dict, List
from xmlrpc.client import Boolean

parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="file",
                    help="The file to check if it is valid", metavar="file_path")


args = vars(parser.parse_args())

# Opening JSON file
f = open(args['file'])

# # returns JSON object as
# # a dictionary
data = json.load(f)


def check_sensor_property(test: List(str)) -> Boolean:
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

    only_one_camera = all(x in cameras for x in cameras)

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


def check_valid_action_space_property(val: str, obj: Dict) -> Boolean:
    """Checks if for a valid action space label and if it matches the object shape

    Args:
        val (str): The label for the action space
        obj (Dict): The object shape for details of the action space

    Returns:
        Boolean: True if the action space parameters are valid and compatible
    """
    val_is_valid = val == 'continuous' or val == 'discrete'
    label = get_action_space_label(obj)
    return val_is_valid and label == label


def get_action_space_label(action_space: Dict) -> str:
    """Gets a type label for an action space

    Args:
        action_space (Dict): The action space object

    Raises:
        Exception: If an invalid action space is provided

    Returns:
        str: The action space label
    """
    try:
        if isinstance(action_space['speed']['high'], float, int) \
            and isinstance(action_space['speed']['low'], float, int) \
            and isinstance(action_space['steering_angle']['high'], float, int) \
            and isinstance(action_space['steering_angle']['low'], float, int):
            return 'continuous'
    except:
        try:
            if isinstance(action_space, list) \
                and all([
                    isinstance(a, dict) and \
                    isinstance(a['steering_angle'], float, int) and \
                                            isinstance(a['speed'], float, int) \
                    for a in action_space]):
                    return 'discrete'
        except:
            raise Exception("Invalid action space provided. Could not give 'continuous' or 'discrete' label")



assert check_sensor_property(
    data['sensor']), f"Invalid 'sensor' value(s) detected: {str(data['sensor'])}"
assert check_neural_network_property(
    data['neural_network']), f"Invalid 'neural_network' value detected: {str(data['neural_network'])}"
assert data['training_algorithm'] == "sac" or data[
    'training_algorithm'] == "clipped_ppo", f"Invalid 'training_algorithm' detected:  {str(data['training_algorithm'])}"
# assert check_neural_network_property(data['neural_network']), "Incorrect neural netowork value detected"


action_space
        },



action_space_type
version
# # Iterating through the json
# # list
# for i in data['emp_details']:
#     print(i)

# # Closing file
# f.close()
