# Hacking the RoboContainer

1. Attach into the container
2. Source the commands
```source /opt/ros/melodic/setup.bash```
3. List the commands
```rostopic list | grep command```
4. Listen to relevant topics
    - rostopic echo /racecar/left_steering_hinge_position_controller/command
    - rostopic echo /racecar/right_steering_hinge_position_controller/command
5. List services:
```rosservice list```
6. Get info of a service
```rosservice info <service>```
7. Get relevant service type
```rosservice type /gazebo/reset_world```
8. Show service type message structure
```rossrv show <ServiceType(output from previous)>```
9. Send a message to the service
```rosservice call /gazebo/reset_world "{}"```
10. List nodes
```rosnode list```
11. List params
```rosparam list```