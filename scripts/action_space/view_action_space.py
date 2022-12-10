import json
from argparse import ArgumentParser
import matplotlib.pyplot as plt
import math

parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="file",
                    help="The file path of the action space file", metavar="file_path")

args = vars(parser.parse_args())


input_file = open(args['file'])

meta_data = json.load(input_file)
action_space = meta_data['action_space']
print('Amount of actions in the action space: {}'.format(len(action_space)))
print('Creating action space graph')
x_list = []
y_list = []

r_list = []
theta_list = []

for ang in action_space:
    
    r = ang['speed']; # Speed
    r_list.append(r)
    theta = math.radians(ang['steering_angle'])
    theta_list.append(theta)

    x = r * math.cos(theta)
    y = r * math.sin(theta)

    x_list.append(x)
    y_list.append(y)

fig = plt.figure(figsize=(180,180))

# CARTESIAN COORDINATE
ax1 = plt.subplot(122, projection='polar')
ax1.set_theta_zero_location("N") # type: ignore
c = ax1.scatter(theta_list, r_list , cmap='hsv', alpha=0.75)
ax1.set_thetamin(-35)  # type: ignore
ax1.set_thetamax(35)  # type: ignore

# POLAR COORDINATE
ax2 = plt.subplot(121)
ax2.set_xlabel('Steering')
ax2.set_ylabel('Speed')
ax2.scatter(x_list, y_list)

plt.show()

