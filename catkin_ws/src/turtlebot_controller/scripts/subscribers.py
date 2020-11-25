import rospy
import tf
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion

class Subscriber:
    def __init__(self, controller):
        rospy.Subscriber('/imu',  Imu, self.imuCallback)
        rospy.Subscriber('/odom', Odometry, self.odomCallback)

        # Get the instance of controller
        self.controller = controller

    def imuCallback(self, data):
        q = (data.orientation.x, data.orientation.y, data.orientation.z, data.orientation.w)
        euler_angles = tf.transformations.euler_from_quaternion(q)

        self.controller.add_orientation(euler_angles)

    def odomCallback(self, data):
        pass