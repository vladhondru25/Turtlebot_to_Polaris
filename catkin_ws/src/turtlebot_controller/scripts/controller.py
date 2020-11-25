import rospy
from geometry_msgs.msg import Twist

import Queue
import threading

from pid import PID


class Controller(threading.Thread):
    def __init__(self):
        super(Controller, self).__init__()
        # Lock for mutual exclusion
        self._orientation_lock = threading.Lock()

        self._mode_autonomous = False    # Mode flag
        self._run_flag = True            # Flag for running the controller loop

        self._queue_velocities = Queue.Queue(maxsize=2)    # Queue for storing velocities commands
        self._queue_orientation = Queue.Queue(maxsize=5)   # Queue for orientations from IMU

        self._pub = rospy.Publisher('cmd_vel', Twist, queue_size=1)  # ROS publisher for velocity commands

        self._run_control_loop = PID(self._pub)  # Instance of the PID controller

        self.start()

    # Stop the Controller thread
    def stop(self):
        self._run_flag = False
        rospy.loginfo("Controller thread stopped.")
        self.join()

    # Add velocity command to queue
    def add_cmd_vel(self, command):
        if self._queue_velocities.full():
            self._queue_velocities.get(block=False, timeout=0.1)
        self._queue_velocities.put(command, block=False, timeout=None)

    # Add orientation to queue
    def add_orientation(self, angles):
        if self._queue_orientation.full():
            self._queue_orientation.get(block=False, timeout=0.1)
        self._queue_orientation.put(angles, block=False, timeout=None)

    # Change between the two modes
    def toggle_mode(self):
        self._mode_autonomous = not self._mode_autonomous

        if self._mode_autonomous:
            rospy.loginfo("Autonomous mode")
        else:
            rospy.loginfo("Manual mode")

    # Controller thread loop
    def run(self):
        while self._run_flag:
            if self._mode_autonomous:
                if not self._queue_orientation.empty():
                    self._orientation_lock.acquire()
                    orientation = self._queue_orientation.get(block=False, timeout=0.1)

                    # Get the current orientation and pass it to the PID controller
                    yaw = orientation[2]
                    self._run_control_loop.step(yaw)

                    self._orientation_lock.release()
            else:
                if not self._queue_velocities.empty():
                    # Publish the velocity commands from the keyboard
                    command = self._queue_velocities.get(block=False, timeout=0.1)
                    self._pub.publish(command)
        