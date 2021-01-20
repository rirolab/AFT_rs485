#!/usr/bin/env python2
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

import serial
import binascii
import time

class Listener(Node):

    def __init__(self):

        super().__init__('Listener')

        self.subcription=self.create_subscription(
            String,
            'RS485',
            self.callback,
            10)

        self.subcription

    def callback(self,msg):

        print_msg=[msg.data[i:i+2] for i in range(0,len(msg.data),2)]
        #print(print_msg)
        self.get_logger().info(msg.data)

def main(args=None):
   
    rclpy.init(args=args)
    
    listener_rs485=Listener()

    rclpy.spin(listener_rs485)

    listener_rs485.destroy_node()

    rclpy.shutdown()

if __name__=='__main__':

    main()