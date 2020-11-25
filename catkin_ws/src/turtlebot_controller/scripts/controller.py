import rospy
from geometry_msgs.msg import Twist

import Queue
import threading


class Controller(threading.Thread):
    def __init__(self):
        super(Controller, self).__init__()

        self._mode_autonomous = False
        self._run_flag = True
        self._queue = Queue.Queue(maxsize=2)
        self._pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)

        self.start()

    def add_cmd_vel(self, command):
        if self._queue.full():
            self._queue.get(block=False, timeout=0.1)
        self._queue.put(command, block=False, timeout=None)

    def toggle_mode(self):
        self._mode_autonomous = not self._mode_autonomous

        if self._mode_autonomous:
            rospy.loginfo("Autonomous mode")
        else:
            rospy.loginfo("Manual mode")

    def stop(self):
        _run_flag = False
        rospy.loginfo("Controller thread stopped.")
        self.join()

    def run(self):
        while self._run_flag:
            if self._mode_autonomous:
                continue
            else:
                if not self._queue.empty():
                    command = self._queue.get(block=False, timeout=0.1)
                    self._pub.publish(command)