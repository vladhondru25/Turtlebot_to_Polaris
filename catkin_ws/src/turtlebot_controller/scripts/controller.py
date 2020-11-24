#!/usr/bin/env python


import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Imu

import tty, select, sys, termios
from subscribers import Subscriber


# Taken from ros-teleop/telep_twist_keyboard package
def getKey(key_timeout, settings):
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], key_timeout)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

# Return a command velocity given the input keys
def process_key(input_key):
    keys = {'w': 0, 'a': 0, 'd': 0, 's': 0, 'q': 0, 'e': 0}

    keys[input_key] = 1

    command = Twist()
    command.linear.x  = keys['w'] - keys['s']
    command.linear.y  = keys['a'] - keys['d']
    command.angular.z = keys['q'] - keys['e']

    return command


if __name__ == '__main__':
    settings = termios.tcgetattr(sys.stdin)

    try:
        subscriber = Subscriber()

        pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        rospy.init_node('controller', anonymous=True)
        rate = rospy.Rate(10) # 10Hz

        while not rospy.is_shutdown():
            # hello_str = "hello world %s" % rospy.get_time()
            # rospy.loginfo(hello_str)

            input_key = getKey(1.0, settings)

            if (input_key == '\x03'):
                break

            command = process_key(input_key)
            # print(command)

            pub.publish(command)
            rate.sleep()

        # rospy.spin()

    except rospy.ROSInterruptException:
        pass

    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)