import json
from argparse import ArgumentParser
import validate_model_metadata_json_functions as func
import sys

parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="file",
                    help="The file to check if it is valid", metavar="file_path")


args = vars(parser.parse_args())

# Opening JSON file
f = open(args['file'])

# # returns JSON object as
# # a dictionary
data = json.load(f)

assert func.check_sensor_property(
    data['sensor']), f"Invalid 'sensor' value(s) detected: {str(data['sensor'])}"

assert func.check_neural_network_property(
    data['neural_network']), f"Invalid 'neural_network' value detected: {str(data['neural_network'])}"

assert data['training_algorithm'] == "sac" or data[
    'training_algorithm'] == "clipped_ppo", f"Invalid 'training_algorithm' detected:  {str(data['training_algorithm'])}"

assert func.check_valid_action_space_property(
    data['action_space_type'], data['action_space']), 'Invalid action space/type detected'

assert func.no_multiple_same_action(data['action_space'])


print('\033[32m' + 'All action space tests passed' + '\033[m')
sys.exit(2)
