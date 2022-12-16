import json
from argparse import ArgumentParser
import matplotlib.pyplot as plt
import numpy as np
import math

parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="file",
                    help="The file path of the action space file", metavar="file_path")

args = vars(parser.parse_args())


input_file = open(args['file'])

meta_data = json.load(input_file)
action_space = meta_data['action_space']


def rotate(x,y,xo,yo,theta): #rotate x,y around xo,yo by theta (rad)
    xr=math.cos(theta)*(x-xo)-math.sin(theta)*(y-yo)   + xo
    yr=math.sin(theta)*(x-xo)+math.cos(theta)*(y-yo)  + yo
    return [xr,yr]


print('Amount of actions in the action space: {}'.format(len(action_space)))
print('Creating action space graph')
x_polar_list = []
y_polar_list = []

x_list = []
y_list = []


r_list = []
theta_list = []

for ang in action_space:
    
    x_list.append(ang['speed'])
    y_list.append(ang['steering_angle'])
    
    r = ang['speed']; # Speed
    r_list.append(r)
    theta = math.radians(ang['steering_angle'])
    theta_list.append(theta)

    x = r * math.cos(theta)
    y = r * math.sin(theta)
    x, y, = rotate(x,y,0,0,math.radians(90))

    x_polar_list.append(x)
    y_polar_list.append(y)

fig = plt.figure(figsize=(180,180))

# POLAR COORDINATE
ax1 = plt.subplot(122, projection='polar')
ax1.set_theta_zero_location("N") # type: ignore
c = ax1.scatter(theta_list, r_list , cmap='hsv', alpha=0.75)
ax1.set_thetamin(-30)  # type: ignore
ax1.set_thetamax(30)  # type: ignore
ax1.set_xticks(np.pi/180. * np.linspace(35,  -40, 15, endpoint=False))


# CARTESIAN COORDINATE
ax2 = plt.subplot(121)
ax2.set_xlabel('Steering')
ax2.set_ylabel('Speed')
ax2.scatter(x_polar_list, y_polar_list)


# NORMAL COORDINATE
# ax3 = plt.subplot(120)
# ax3.set_thetamin(-30)  # type: ignore
# ax3.set_thetamax(30)  # type: ignore
# ax2.scatter(x_list, y_list)


plt.show()

