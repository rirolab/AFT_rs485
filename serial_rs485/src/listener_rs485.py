#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import serial
import binascii
import time

def callback(data):

    sig_msg=data.data.encode()
    print_msg=[sig_msg[i:i+2] for i in range(0,len(sig_msg),2)]
    rospy.loginfo(print_msg)
    
def listener():

    rospy.init_node('Listener_RS485', anonymous=True)

    rospy.Subscriber("RS485", String, callback)

    rospy.spin()

if __name__ == '__main__':
    listener()