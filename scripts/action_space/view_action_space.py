import json
from argparse import ArgumentParser
import matplotlib.pyplot as plt

parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="file",
                    help="The file path of the action space file", metavar="file_path")

args = vars(parser.parse_args())


input_file = open(args['file'])

meta_data = json.load(input_file)
action_space = meta_data['action_space']

print('Creating action space graph')
x = []
y = []
for ang in action_space:
    x.append(ang['steering_angle'])
    y.append(ang['speed'])
    

plt.xlabel('Steering Angle')
plt.ylabel('Speed')
plt.scatter(x, y)
plt.show()