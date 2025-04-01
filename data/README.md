## How did we collect data for the research?

We used the CoppeliaSim simulator to simulate robots doing inspection tasks, and collecting [Odometry/Pose](http://docs.ros.org/en/noetic/api/nav_msgs/html/msg/Odometry.html) data.

All robot trajectory planning and ROS integration are available at [ITV/ROC](https://github.com/ITVRoC/espeleo_vrep_simulation) repositories.

<figure>
  <img src="images/robot.png" alt="Robot in Coppelia simulator">
  <figcaption>An EspeleoRobô robot in an inspection scenario in the Coppelia simulator.</figcaption>
</figure>

## Robot Trajectories

The robots' trajectories for the data collected are the following:

- Robot 1:

<figure>
  <img src="images/traj1.png" alt="Elipse Trajectory">
  <figcaption>An elipse trajectory.</figcaption>
</figure>

- Robot 2:

<figure>
  <img src="images/traj2.png" alt="8 like Trajectory">
  <figcaption>A '8 like' trajectory.</figcaption>
</figure>

- Robot 3:

<figure>
  <img src="images/traj3.png" alt="Rectangular Trajectory">
  <figcaption>A 'rectangular' trajectory.</figcaption>
</figure>

- Robot 4:

<figure>
  <img src="images/traj4.png" alt="Sinusoidal Trajectory">
  <figcaption>A sinusoidal trajectory.</figcaption>
</figure>

## Output Files

The 'pose1.txt', 'pose2.txt', 'pose3.txt', and 'pose4.txt' are the output files for the data collected in each robot simulation. 
