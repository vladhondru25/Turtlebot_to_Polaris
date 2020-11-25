#!/usr/bin/env python


import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Imu

import sys, termios
from subscribers import Subscriber
from controller import Controller
import utilities


if __name__ == '__main__':
    settings = termios.tcgetattr(sys.stdin)

    controller = Controller()

    try:
        rospy.init_node('turtlebot_node', anonymous=True)
        rate = rospy.Rate(20) # 10Hz

        subscriber = Subscriber()

        while not rospy.is_shutdown():
            input_key = utilities.getKey(0.5, settings)

            if (input_key == '\x03'):
                break

            elif (input_key == ' '):
                controller.toggle_mode()
            
            else:
                _, command = utilities.process_key(input_key)
                controller.add_cmd_vel(command)

            rate.sleep()

        # rospy.spin()

    except rospy.ROSInterruptException:
        rospy.loginfo("Exception")
        pass

    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        controller.stop()