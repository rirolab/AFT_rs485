## FT sensor module

- **Enviroment**: ROS melodic(UBUNTU 18.04LTS)
- **Modules**: Graphs, save csv file
- **doc**: circuit diagram

### To do
- Fixing y label
- Add rostopic /RS485 
- Connect to Haetae gripper 
- Gripper Modeling(need to add gripper cover)

#### 1. Please install pyserial

    python -m pip install pyserial

#### 2. Run roscore
    roscore
    python connect_signal_rs485.py
    
#### ( if tty denied ) 

    sudo usermod -a -G dialout USER_NAME

#### ( if port is not ttyUSB0, please rewrite the connect_signal.py line 18 )

    ls /dev/ttyUSB0
    
\
\
TODO: Chanyoung Ahn
