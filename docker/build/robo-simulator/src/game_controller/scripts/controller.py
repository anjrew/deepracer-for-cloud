#!/usr/bin/env python
print("Starting script")

import pygame
import sys
print(sys.version)
import rospy
print(rospy.__file__)
from std_msgs.msg import Float64
import logging

# Define ROS topics for speed and steering commands
speed_topics = [
    '/racecar/left_rear_wheel_velocity_controller/command', 
    '/racecar/right_rear_wheel_velocity_controller/command',
    '/racecar/left_front_wheel_velocity_controller/command', 
    '/racecar/right_front_wheel_velocity_controller/command'
]

steering_topics = [
    '/racecar/left_steering_hinge_position_controller/command', 
    '/racecar/right_steering_hinge_position_controller/command'
]

print("Initializing ROS node")

# Initialize ROS node
rospy.init_node('game_controller')

print("Creating ROS publishers")
# Initialize ROS publishers for speed and steering commands
speed_publishers = [rospy.Publisher(topic, Float64, queue_size=10) for topic in speed_topics]
steering_publishers = [rospy.Publisher(topic, Float64, queue_size=10) for topic in steering_topics]

# Initialize Pygame library
print("Initializing Pygame")
pygame.init()
pygame.joystick.init()
print("Number of joysticks: {}".format(pygame.joystick.get_count()))
joystick = pygame.joystick.Joystick(0)
print("Initializing joystick: {}".format(joystick.get_name()))
joystick.init()

# Define constants for speed and steering limits
MAX_SPEED = 1.0
MIN_SPEED = -1.0
MAX_STEERING_ANGLE = 0.5
MIN_STEERING_ANGLE = -0.5

print("Starting main loop")
# Main loop for reading input from game controller and publishing commands to ROS
while not rospy.is_shutdown():
    pygame.event.pump()

    # Read input from game controller
    speed = joystick.get_axis(1)  # left joystick y-axis
    steering = joystick.get_axis(0)  # left joystick x-axis
    print("speed: ", speed, "steering: ", steering)

    # Scale input to speed and steering limits
    speed = max(MIN_SPEED, min(speed, MAX_SPEED))
    steering = max(MIN_STEERING_ANGLE, min(steering, MAX_STEERING_ANGLE))

    # Publish speed and steering commands to ROS topics
    for publisher in speed_publishers:
        publisher.publish(speed)

    for publisher in steering_publishers:
        publisher.publish(steering)

    # Sleep for a short period of time to prevent excessive publishing
    rospy.sleep(0.01)
