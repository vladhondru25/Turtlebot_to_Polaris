import rospy
from geometry_msgs.msg import Twist

import Queue
import threading

from pid import PID


class Controller(threading.Thread):
    def __init__(self):
        super(Controller, self).__init__()
        self._orientation_lock = threading.Lock()

        self._mode_autonomous = False
        self._run_flag = True

        self._queue_velocities = Queue.Queue(maxsize=2)
        self._queue_orientation = Queue.Queue(maxsize=5)

        self._pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)

        self._run_control_loop = PID(self._pub)

        self.start()

    def stop(self):
        self._run_flag = False
        rospy.loginfo("Controller thread stopped.")
        self.join()

    def add_cmd_vel(self, command):
        if self._queue_velocities.full():
            self._queue_velocities.get(block=False, timeout=0.1)
        self._queue_velocities.put(command, block=False, timeout=None)

    def add_orientation(self, angles):
        if self._queue_orientation.full():
            self._queue_orientation.get(block=False, timeout=0.1)
        self._queue_orientation.put(angles, block=False, timeout=None)

    def toggle_mode(self):
        self._mode_autonomous = not self._mode_autonomous

        if self._mode_autonomous:
            rospy.loginfo("Autonomous mode")
        else:
            rospy.loginfo("Manual mode")

    def run(self):
        while self._run_flag:
            if self._mode_autonomous:
                if not self._queue_orientation.empty():
                    self._orientation_lock.acquire()
                    orientation = self._queue_orientation.get(block=False, timeout=0.1)

                    yaw = orientation[2]
                    self._run_control_loop.step(yaw)

                    self._orientation_lock.release()
            else:
                if not self._queue_velocities.empty():
                    command = self._queue_velocities.get(block=False, timeout=0.1)
                    self._pub.publish(command)

            # rospy.sleep(1)

        