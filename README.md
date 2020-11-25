# Turtlebot oriented to Polaris

Task: Write appropriate ROS/Python​ that continuously orientates a turtlebot to Polaris (the north star) from anywhere on Earth.

## Requirements
ROS1 Melodic \
Python2 \
Turtlebot3

## How to run
From the catkin_ws folder, source the setup.sh file ('source devel/setup.bash'), then, in two separate terminals:

       roslaunch turtlebot_sim turtlebot.launch
       roslaunch turtlebot_controller controller.launch

The first command lunches the simulation environment, while the second one runs the controller. In the controller can be used as follows: \
    - The turtlebot operates in 2 modes: Autonomous and Manual \
    - In Manual mode (default mode), the robot can be controlled using W, A, S, D keys (W,S for linear velocity, A,D for angular velocity) \
    - Change between the modes using whitespace \
    - In autonomous mode, the robot will try to orientate itself to Polaris \
    - Press 't' to run test 1 (change position of robot) then switch to autonomous mode (if not already) to watch robot orientate itself \
    - Press 'y' to run test 1 (change position of robot) then switch to autonomous mode (if not already) to watch robot orientate itself
    
The orientation relative to the north is obtained from the IMU sensor (that contains a magnetometer). The IMU measurements are read and a PID controller is used to correct this angle.