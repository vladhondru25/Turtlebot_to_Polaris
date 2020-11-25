import tty, select, sys, termios

from geometry_msgs.msg import Twist


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
    keys = {'w': 0.0, 'a': 0.0, 'd': 0.0, 's': 0.0}

    flag_move = input_key in keys.keys()
    keys[input_key] = 0.75

    command = Twist()
    command.linear.x  = keys['w'] - keys['s']
    command.angular.z = keys['a'] - keys['d']

    return (flag_move, command)