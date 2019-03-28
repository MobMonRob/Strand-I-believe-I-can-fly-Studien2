#!/usr/bin/env python

import rospy
from drone_controller import DroneController
from communication_manager import CommunicationManager


def init_node():
    """
    Initializes ROS node 'airsim_connector'.
    """

    def on_shutdown():
        """
        Lands the drone when ROS node is shut down. Do NOT wait for it's execution to shutdown node immediately.
        """
        try:
            rospy.loginfo('Release API control of drone as node is shutdown!')
            drone_controller.release_control()
        except:
            rospy.loginfo('Drone was not initialized at shutdown!')
            rospy.signal_shutdown('Shutdown airsim_connector node')

    rospy.init_node('airsim_connector',
                    log_level = (rospy.DEBUG if rospy.get_param('/airsim_connector/debug') else rospy.ERROR))
    rospy.on_shutdown(on_shutdown)
    drone_controller = DroneController()
    communication_manager = CommunicationManager(drone_controller)
    communication_manager.start_listening()
    while not rospy.is_shutdown():
        rospy.logdebug('Performing next action')
        drone_controller.perform_action()


if __name__ == '__main__':
    init_node()
