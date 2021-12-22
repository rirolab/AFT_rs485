#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import rospy
from std_msgs.msg import String
import serial
import binascii
import time
import numpy as np
import decimal
from matplotlib import pyplot as plt
from matplotlib import animation
import csv 

ser = serial.Serial()
pub = rospy.Publisher('RS485',String,queue_size=10)
f = open('data.csv','a')
wr = csv.writer(f)

def initSerial():
    
    global ser
    
    ser.baudrate = 115200
    ser.port = '/dev/ttyUSB0' #
    #ser.port = 'COM7'
    #ser.timeout =0
    ser.stopbits = serial.STOPBITS_ONE
    ser.bytesize = 8
    ser.parity = serial.PARITY_NONE
    ser.rtscts = 0

def callback(data):
    
    rospy.loginfo(rospy.get_caller_id())

def buff():
    buffer = np.array([])
    rospy.init_node('Connect_signal_rs485', anonymous=True)
    #rate = rospy.Rate(10)
    while True:
        mHex = ser.read(1)
        if len(mHex)!= 0:
                hxstr=binascii.hexlify(bytearray(mHex)) # binary to 16
                sig_msg = hxstr.decode() #unicode
                if sig_msg != '0a':
                    buffer = np.append(buffer, sig_msg)
                    
                else:
                    #buffer = np.array([buffer]) #(,12)->(1,12)
                    #time.sleep(0.1)
                    break
    #rospy.loginfo(buffer)
    return(buffer) #numpy.array[numpy.unicode_]

def transmit(data):
    """
    transmit ( hexadecimal(16) data to Decimal(10) data  
    type: np.array [Fx, Fy, Fz, Tx, Ty, Tz] 
    """
    Datafield = np.array([])
    for i in data:
        #Datafield[0][i] = int(Datafield[0][i],16)
        a = int(i, 16)
        Datafield = np.append(Datafield, a)
    
    if len(Datafield) == 12:
        Fout = Datafield[0:6]
        Tout = Datafield[6:]

        Fx = Fout[0] * 256. + Fout[1]
        Fy = Fout[2] * 256. + Fout[3]
        Fz = Fout[4] * 256. + Fout[5]

        Tx = Tout[0] * 256. + Tout[1]
        Ty = Tout[2] * 256. + Tout[3]
        Tz = Tout[4] * 256. + Tout[5]

        # output data to [N],[N/mm]
        Force = np.array([Fx, Fy, Fz])/100. - 50.
        Torque = np.array([Tx, Ty, Tz])/100. - 200.

        output = np.append(Force, Torque)
        return(output)

def bias():
    """
    bias_val  (initial value for calibration)
    type: np.array [Fx, Fy, Fz, Tx, Ty, Tz] 
    """
    bias_val = [0., 0., 0., 0., 0., 0.]
    cst = 0.
    for i in range (5):
        tt = buff()
        tt = tt.tolist()
        tt = transmit(tt) 
        if tt is not None:
                bias_val = bias_val + tt 
                cst += 1.
    bias_val = bias_val / cst
    return(bias_val)

def cali_output(output, bias_val):
    """
    cali_output (Decimal data + calibration: output-initial output)
    type: np.array [Fx, Fy, Fz, Tx, Ty, Tz] 
    """
    output = output - bias_val

    return(output)

fig = plt.figure()    
axs = [plt.subplot(321, xlim=(0, 50), ylim=([-15, 15])),
            plt.subplot(323, xlim=(0, 50), ylim=([-15, 15])),
            plt.subplot(325, xlim=(0, 50), ylim=([-15, 15])),
            plt.subplot(322, xlim=(0, 50), ylim=([-75, 75])),
            plt.subplot(324, xlim=(0, 50), ylim=([-75, 75])),
            plt.subplot(326, xlim=(0, 50), ylim=([-75, 75]))]

#max_points = 50
max_points = 100

lines = [] 
for i in range(6): 
    line = np.ones(max_points, dtype=np.float) * np.nan
    lines.append(line)

def animate(i):
    try:
        y = get_data()
        wr.writerow(y)
    except: 
        y = 0
    
    for i in range(6):
        axs[i]
        new_y = np.r_[lines[i][1:], y[i]]
        lines[i] = new_y
        axs[i].cla()
        axs[i].plot(np.arange(max_points), new_y, lw=1, c='blue',ms=1)


def get_data(): 
    bias_val = bias()
    buffer = buff().tolist()
    #buffer = buffer
    if len(buffer)!= 0:
        output = transmit(buffer) # (1,12) 16 -> 10 [0][1]
        #print_msg = cali_output(output, bias_val)
        if output is not None:
            print_msg = cali_output(output, bias_val)
            rospy.loginfo(print_msg)
            
            

    return print_msg 

def talk():
    rospy.init_node('Connect_signal_rs485', anonymous=True)
    #rate = rospy.Rate(10)
    anim = animation.FuncAnimation(fig, animate, interval = 10, blit=False)
    #anim2 = animation.FuncAnimation(fig, animate_Fy,interval = 10)
    plt.show()




if __name__ == "__main__":

    try:  
    
        initSerial()
        ser.open()
        get_data()
        talk()

    except rospy.ROSInterruptException:
        f.close()
        pass