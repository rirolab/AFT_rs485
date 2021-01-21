#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import rospy
from std_msgs.msg import String
import serial
import binascii
import time

ser = serial.Serial()

def initSerial():
    
    global ser
    
    ser.baudrate = 115200
    ser.port = '/dev/ttyUSB0'
    #ser.port = 'COM7'
    #ser.timeout =0
    ser.stopbits = serial.STOPBITS_ONE
    ser.bytesize = 8
    ser.parity = serial.PARITY_NONE
    ser.rtscts = 0

def callback(data):
    
    rospy.loginfo(rospy.get_caller_id())

def talk():
    
    pub=rospy.Publisher('RS485',String,queue_size=10)
    rospy.init_node('Connect_signal_RS485', anonymous=True)
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():

        mHex = ser.read(17)
        
        if len(mHex)!= 0:
        
            hxstr=binascii.hexlify(bytearray(mHex))
            sig_msg=hxstr.decode()
            #temp2=temp.encode()
            print_msg=[sig_msg[i:i+2] for i in range(0,len(sig_msg),2)]
            rospy.loginfo(print_msg)
            pub.publish(sig_msg)
            time.sleep(0.1)

if __name__ == "__main__":

    try:  
    
        initSerial()
        ser.open()
        talk()

    except rospy.ROSInterruptException:
    
        pass
