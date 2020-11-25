#!/usr/bin/env python


import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Imu

import sys, termios
from subscribers import Subscriber
from controller import Controller
import utilities
import tests


if __name__ == '__main__':
    settings = termios.tcgetattr(sys.stdin)

    controller = Controller()

    try:
        rospy.init_node('turtlebot_node', anonymous=True)
        rate = rospy.Rate(20) # 10Hz

        subscriber = Subscriber(controller)

        while not rospy.is_shutdown():
            input_key = utilities.getKey(0.5, settings)

            if (input_key == '\x03'):
                break

            elif (input_key == ' '):
                controller.toggle_mode()

            elif (input_key == 't'):
                tests.test1()
            elif (input_key == 'y'):
                tests.test2()
            
            else:
                _, command = utilities.process_key(input_key)
                controller.add_cmd_vel(command)

            rate.sleep()

    except Exception as e:
        print(e)

    finally:
        controller.stop()
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)