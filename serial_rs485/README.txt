THIS PACKAGE IS TESTED ON ROS2 DASHING(UBUNTU 18.04LTS)

1. Please install ros2 dashing: https://index.ros.org/doc/ros2/Installation/Dashing/Linux-Install-Debians/

2. Please install pyserial -> python -m pip install pyserial

2. if tty denied -> sudo usermod -a -G dialout USER_NAME

3.if port is not ttyUSB0, please rewrite the connect_signal.py line 18.

4. ros2 run 