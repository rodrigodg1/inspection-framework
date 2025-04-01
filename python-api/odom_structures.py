import yaml

# We define the Odometry ROS data structure:
class Data:
	seq: int = 0
	secs: int = 0
	nsecs: int = 0
	frame_id: str = ""
	child_frame_id: str = ""
	position_x: int = 0
	position_y: int = 0
	position_z: int = 0
	orientation_x: int = 0
	orientation_y: int = 0
	orientation_z: int = 0
	orientation_w: int = 0
	covariance: list = []
	linear_x: int = 0
	linear_y: int = 0
	linear_z: int = 0
	angular_x: int = 0
	angular_y: int = 0
	angular_z: int = 0
	twist_covariance: list = []
	

# Reading .txt files:
def read_file(file_name):
	with open(file_name, 'r') as file:
		data = file.read()
	return data

# Gets a block of Odom.txt and clears to an Odom object: 
def clear_odom(block):
	
	clean = Data()
	data = yaml.safe_load(block)
    
	clean.seq = int(data['header']['seq'])
	clean.secs = int(data['header']['stamp']['secs'])
	clean.nsecs = int(data['header']['stamp']['nsecs'])
	clean.frame_id = data['header']['frame_id']
	clean.child_frame_id = data['child_frame_id']
	clean.position_x = int(data['pose']['pose']['position']['x'])
	clean.position_y = int(data['pose']['pose']['position']['y'])
	clean.position_z = int(data['pose']['pose']['position']['z'])
	clean.orientation_x = int(data['pose']['pose']['orientation']['x'])
	clean.orientation_y = int(data['pose']['pose']['orientation']['y'])
	clean.orientation_z = int(data['pose']['pose']['orientation']['z'])
	clean.orientation_w = int(data['pose']['pose']['orientation']['w'])
	clean.covariance = data['pose']['covariance']
	clean.covariance = [int(i) for i in clean.covariance]
	clean.linear_x = int(data['twist']['twist']['linear']['x'])
	clean.linear_y = int(data['twist']['twist']['linear']['y'])
	clean.linear_z = int(data['twist']['twist']['linear']['z'])
	clean.angular_x = int(data['twist']['twist']['angular']['x'])
	clean.angular_y = int(data['twist']['twist']['angular']['y'])
	clean.angular_z = int(data['twist']['twist']['angular']['z'])
	clean.twist_covariance = data['twist']['covariance']
	clean.twist_covariance = [int(i) for i in clean.twist_covariance]
		
	return clean


# Gets a block of Pose.txt and clears to an Odom object: 
def clear_pose(block):
	
	clean = Data()
	data = yaml.safe_load(block)
    
	clean.position_x = int(data['position']['x']*1e3) # For float correction
	clean.position_y = int(data['position']['y']*1e3)
	clean.position_z = int(data['position']['z']*1e3)
	clean.covariance = [0] * 36
	clean.orientation_x = int(data['orientation']['x']*1e3)
	clean.orientation_y = int(data['orientation']['y']*1e3)
	clean.orientation_z = int(data['orientation']['z']*1e3)
	clean.orientation_w = int(data['orientation']['w']*1e3)
	clean.twist_covariance = [0] * 36
		
	return clean


# Cleaning a hole Odom.txt file:
def cleanOdom(file_name):

	# Reads file
	data = read_file(file_name)

	# Cleans header
	blocks = data.strip().split('---')

	# Converts block txt data to Data structure
	clean_blocks = []
	for block in blocks:
		if block:
			clean_blocks.append(clear_odom(block))
			
	return clean_blocks

# Cleaning a hole Pose.txt file:
def cleanPose(file_name):

	# Reads file
	data = read_file(file_name)

	# Cleans header
	blocks = data.strip().split('---')

	# Converts block txt data to Data structure
	clean_blocks = []
	for block in blocks:
		if block:
			clean_blocks.append(clear_pose(block))

	return clean_blocks