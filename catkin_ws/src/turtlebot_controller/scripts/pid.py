import math

from geometry_msgs.msg import Twist


class PID():
    def __init__(self, pub):
        # PID constants
        self.kp = 1.0
        self.kd = 0.0
        self.ki = 0.0
        self._pub = pub

    def step(self, yaw):
        # Compute the error yaw angle
        yaw_error = -yaw

        # Make sure you rotate in the shortest distance
        if yaw_error >  math.pi:
            yaw_error = yaw_error - math.pi
        if yaw_error < -math.pi:
            yaw_error = yaw_error + math.pi

        # Compute the input correction
        u = self.kp * yaw_error
        # Limit the input
        u = min(1.0, u) 

        command = Twist()
        command.angular.z = u
        
        self._pub.publish(command)
