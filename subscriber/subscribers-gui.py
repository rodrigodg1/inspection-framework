#!/usr/bin/env python3

# Import necessary modules
import rospy
import tkinter as tk
from tkinter import ttk
from geometry_msgs.msg import Vector3Stamped
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry

# Define a class FrontEnd
class FrontEnd:
    def __init__(self, master):
        # Initialize the master window
        self.master = master
        self.master.title("Front End Subscriber")
        self.tab_control = ttk.Notebook(self.master)

        # Create tabs
        self.angular_velocity_tab = ttk.Frame(self.tab_control)
        self.imu_data_tab = ttk.Frame(self.tab_control)
        self.imu_mag_tab = ttk.Frame(self.tab_control)
        self.odom_tab = ttk.Frame(self.tab_control)

        # Add tabs to the notebook
        self.tab_control.add(self.angular_velocity_tab, text='Angular Velocity')
        self.tab_control.add(self.imu_data_tab, text='IMU Data')
        self.tab_control.add(self.imu_mag_tab, text='IMU Mag')
        self.tab_control.add(self.odom_tab, text='Odometry')

        # Create scrollbars and a listbox on the "Angular Velocity" tab
        self.angular_velocity_scrollbar_y = tk.Scrollbar(self.angular_velocity_tab, orient="vertical")
        self.angular_velocity_scrollbar_x = tk.Scrollbar(self.angular_velocity_tab, orient="horizontal")
        self.angular_velocity_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.angular_velocity_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.angular_velocity_listbox = tk.Listbox(self.angular_velocity_tab, height=80, width=270,font=('Consolas', 9), yscrollcommand=self.angular_velocity_scrollbar_y.set, xscrollcommand=self.angular_velocity_scrollbar_x.set)
        self.angular_velocity_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.angular_velocity_scrollbar_y.config(command=self.angular_velocity_listbox.yview)
        self.angular_velocity_scrollbar_x.config(command=self.angular_velocity_listbox.xview)

# Create scrollbars and a listbox on the "IMU Data" tab
        self.imu_data_scrollbar_y = tk.Scrollbar(self.imu_data_tab, orient="vertical")
        self.imu_data_scrollbar_x = tk.Scrollbar(self.imu_data_tab, orient="horizontal")
        self.imu_data_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.imu_data_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.imu_data_listbox = tk.Listbox(self.imu_data_tab, height=80, width=270,font=('Consolas', 9), yscrollcommand=self.imu_data_scrollbar_y.set, xscrollcommand=self.imu_data_scrollbar_x.set)
        self.imu_data_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.imu_data_scrollbar_y.config(command=self.imu_data_listbox.yview)
        self.imu_data_scrollbar_x.config(command=self.imu_data_listbox.xview)

        # Create scrollbars and a listbox on the "IMU Mag" tab
        self.imu_mag_scrollbar_y = tk.Scrollbar(self.imu_mag_tab, orient="vertical")
        self.imu_mag_scrollbar_x = tk.Scrollbar(self.imu_mag_tab, orient="horizontal")
        self.imu_mag_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.imu_mag_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.imu_mag_listbox = tk.Listbox(self.imu_mag_tab, height=80, width=270,font=('Consolas', 9), yscrollcommand=self.imu_mag_scrollbar_y.set, xscrollcommand=self.imu_mag_scrollbar_x.set)
        self.imu_mag_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.imu_mag_scrollbar_y.config(command=self.imu_mag_listbox.yview)
        self.imu_mag_scrollbar_x.config(command=self.imu_mag_listbox.xview)

        # Create scrollbars and a listbox on the "Odometry" tab
        self.odom_scrollbar_y = tk.Scrollbar(self.odom_tab, orient="vertical")
        self.odom_scrollbar_x = tk.Scrollbar(self.odom_tab, orient="horizontal")
        self.odom_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.odom_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.odom_listbox = tk.Listbox(self.odom_tab, height=80, width=270,font=('Consolas', 9), yscrollcommand=self.odom_scrollbar_y.set, xscrollcommand=self.odom_scrollbar_x.set)
        self.odom_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.odom_scrollbar_y.config(command=self.odom_listbox.yview)
        self.odom_scrollbar_x.config(command=self.odom_listbox.xview)

        # Add the notebook to the master window
        self.tab_control.pack(expand=1, fill='both')


    # Define callback functions for each subscribed topic to display received data
    def angular_velocity_callback(self, data):
        self.angular_velocity_listbox.insert(0, "Received angular velocity: \n%s" % data)

    def imu_data_callback(self, data):
        self.imu_data_listbox.insert(0, "Received IMU data: \n%s" % data)

    def imu_mag_callback(self, data):
        self.imu_mag_listbox.insert(0, "Received IMU mag: \n%s" % data)

    def odom_callback(self, data):
        self.odom_listbox.insert(0, "Received odometry data: \n%s" % data)

    # Subscribe to each topic and initialize the node
    def subscribe_to_topics(self):
        rospy.init_node('front_end_subscriber', anonymous=True)

        rospy.Subscriber("/imu/angular_velocity", Vector3Stamped, self.angular_velocity_callback)
        rospy.Subscriber("/imu/data", Imu, self.imu_data_callback)
        rospy.Subscriber("/imu/mag", Vector3Stamped, self.imu_mag_callback)
        rospy.Subscriber("/odom", Odometry, self.odom_callback)

# Create a root window
root = tk.Tk()

# Create an instance of the FrontEnd class and subscribe to topics
front_end = FrontEnd(root)
front_end.subscribe_to_topics()

# Start the GUI mainloop
root.mainloop()

# Spin the rospy node
rospy.spin()