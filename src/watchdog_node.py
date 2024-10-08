#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
import subprocess

def ping_target(target_ip):
    # Ping the target IP once (-c 1), timeout after 1 second (-W 1)
    try:
        output = subprocess.check_output(
            ['ping', '-c', '1', '-W', '1', target_ip],
            stderr=subprocess.STDOUT,  # Combine stdout and stderr
            universal_newlines=True  # Return output as a string
        )
        return True
    except subprocess.CalledProcessError:
        return False

def watchdog():
    rospy.init_node('network_watchdog_node')

    target_ip = rospy.get_param('~target_ip', '192.168.1.103')  # Controller IP

    pub = rospy.Publisher('controller_status', String, queue_size=1)
    rate = rospy.Rate(1)  # Ping once per second

    while not rospy.is_shutdown():
        if ping_target(target_ip):
            rospy.loginfo("reachable")
            pub.publish("reachable")

        else:
            rospy.logwarn("unreachable")
            pub.publish("unreachable")

        rate.sleep()

if __name__ == '__main__':
    try:
        watchdog()
    except rospy.ROSInterruptException:
        pass
