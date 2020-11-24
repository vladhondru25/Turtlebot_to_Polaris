import rospy
import tf
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion

class Subscriber:
    def __init__(self):
        rospy.Subscriber('/imu',  Imu, self.imuCallback)
        rospy.Subscriber('/odom', Odometry, self.odomCallback)

    def imuCallback(self, data):
        q = (data.orientation.x, data.orientation.y, data.orientation.z, data.orientation.w)
        euler_angles = tf.transformations.euler_from_quaternion(q)
        roll  = euler_angles[0]
        pitch = euler_angles[1]
        yaw   = euler_angles[2]

        print(euler_angles)

    def odomCallback(self, data):
        pass