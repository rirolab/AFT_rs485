
#!/usr/bin/env python2
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
import serial
import binascii
import time
import pkg_resources

ser = serial.Serial(

    baudrate = 115200,
    port = '/dev/ttyUSB0',
    #ser.port = 'COM7'
    #ser.timeout =0
    stopbits = serial.STOPBITS_ONE,
    bytesize = 8,
    parity = serial.PARITY_NONE,
    rtscts = 0,
)

class Connect_Signal(Node):

    def __init__(self):

        super().__init__('Connect_signal')

        self.publisher_=self.create_publisher(String, 'RS485',10)

        timer_period = 0.1  # seconds

        self.timer = self.create_timer(timer_period, self.callback)

    def callback(self):

        mHex = ser.read(17)

        if len(mHex)!= 0:

            hxstr=binascii.hexlify(bytearray(mHex))
            sig_msg=String()
            sig_msg.data=hxstr.decode()
            print_msg=[sig_msg.data[i:i+2] for i in range(0,len(sig_msg.data),2)]
            self.publisher_.publish(sig_msg)
            self.get_logger().info(sig_msg.data)

def main(args=None):
   
    rclpy.init(args=args)

    connect_signal_rs485=Connect_Signal()

    rclpy.spin(connect_signal_rs485)

    connect_signal_rs485.destroy_node()
    
    rclpy.shutdown()

if __name__=='__main__':
    
    main()