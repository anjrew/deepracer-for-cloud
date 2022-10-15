import json
from argparse import ArgumentParser
import matplotlib.pyplot as plt

parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="file",
                    help="The file path of the action space file", metavar="file_path")

args = vars(parser.parse_args())


input_file = open(args['file'])
# input_file = open('./config/discreate-action-space-config.json')
# # returns JSON object as
# # a dictionary
meta_data = json.load(input_file)
action_space = meta_data['action_space']

print('Creating action space graph')
x = []
y = []
for ang in action_space:
    x.append(int(ang['steering_angle']))
    y.append(int(ang['speed']))
plt.scatter(x, y)
plt.show()