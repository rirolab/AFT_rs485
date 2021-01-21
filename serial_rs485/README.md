Serial_RS485 to usb
===================

THIS PACKAGE IS TESTED ON ROS2 DASHING(UBUNTU 18.04LTS)
-------------------------------------------------------

#1. Please install ros2 dashing

Link: <https://index.ros.org/doc/ros2/Installation/Dashing/Linux-Install-Debians/>

#2. Please install pyserial

    python -m pip install pyserial

#3. if tty denied 

    sudo usermod -a -G dialout USER_NAME

#4.if port is not ttyUSB0, please rewrite the connect_signal.py line 18.

#5. ros2 run 