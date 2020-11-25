import rospy 
import rospkg 
from gazebo_msgs.msg import ModelState 
from gazebo_msgs.srv import SetModelState



def test1():
    rospy.wait_for_service('/gazebo/set_model_state')

    state_msg = ModelState()
    state_msg.model_name = 'turtlebot3_waffle_pi'
    state_msg.pose.position.x = 0
    state_msg.pose.position.y = 0
    state_msg.pose.position.z = 0
    state_msg.pose.orientation.x = -0.00149407013669
    state_msg.pose.orientation.y = 0.000550440733234
    state_msg.pose.orientation.z = 0.937933500363
    state_msg.pose.orientation.w = 0.346811495868

    try:
        set_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
        resp = set_state(state_msg)

    except rospy.ServiceException, e:
        print("Service call failed: %s" % e)


def test2():
    rospy.wait_for_service('/gazebo/set_model_state')

    state_msg = ModelState()
    state_msg.model_name = 'turtlebot3_waffle_pi'
    state_msg.pose.position.x = 0
    state_msg.pose.position.y = 0
    state_msg.pose.position.z = 0
    state_msg.pose.orientation.x = 0.00134511812359
    state_msg.pose.orientation.y = 0.000847180193177
    state_msg.pose.orientation.z = -0.846710167166
    state_msg.pose.orientation.w = 0.532052032946

    try:
        set_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
        resp = set_state(state_msg)

    except rospy.ServiceException, e:
        print("Service call failed: %s" % e)