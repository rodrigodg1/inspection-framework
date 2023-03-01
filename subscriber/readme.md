# Front End Subscriber

This script creates a GUI using the tkinter module to display data from subscribed topics.

## Dependencies

This script requires the following modules:
- rospy
- tkinter
- geometry_msgs.msg
- sensor_msgs.msg
- nav_msgs.msg

## Usage

To use this script, run the following command:

    ```console
    rosrun subscriber subscriber.py
    ```

## Classes

### FrontEnd

The `FrontEnd` class creates the GUI and defines callback functions for each subscribed topic to display received data.

#### Methods

- `__init__(self, master)`: Initializes the master window and creates tabs with scrollbars and listboxes for each topic.
- `angular_velocity_callback(self, data)`: Inserts received angular velocity data into the listbox on the "Angular Velocity" tab.
- `imu_data_callback(self, data)`: Inserts received IMU data into the listbox on the "IMU Data" tab.
- `imu_mag_callback(self, data)`: Inserts received IMU mag data into the listbox on the "IMU Mag" tab.
- `odom_callback(self, data)`: Inserts received odometry data into the listbox on the "Odometry" tab.
