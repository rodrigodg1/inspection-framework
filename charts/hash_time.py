import sys
import matplotlib.pyplot as plt
from merkletools import MerkleTools
import time

def read_file(file_name):
    with open(file_name, 'r') as file:
        data = file.read()
    return data

def calculate_hash_time(data):
    mt = MerkleTools(hash_type="sha256")
    header_blocks = data.strip().split('---')
    header_times = []

    for block in header_blocks:
        if block:
            #get time
            start = time.process_time()
            mt.add_leaf(block, True)
            header_times.append((time.process_time() - start)*1e6)  
            
    #tree creation time
    start = time.process_time()
    mt.make_tree()
    #header_times.append((time.process_time() - start)*1e6) #last append == tree creation time
            
    return header_times
    
def plot_box_plot(header_sizes_list, file_names):
    plt.style.use('seaborn-white')  # Change the box plot style
    fig, ax = plt.subplots(figsize=(10, 6))  # Adjust the figure size
    ax.boxplot(header_sizes_list, labels=file_names, widths=0.5)
    ax.set_title('Merkle Tree', fontsize=20)
    ax.set_ylabel('Time in ns', fontsize=16)
    ax.tick_params(axis='both', labelsize=14)
    ax.grid(axis='y')  # Add gridlines

    plt.show()

file_names = ['odom.txt', 'imu_data.txt', 'imu_mag.txt', 'imu_angular.txt']
file_labels = {
    'odom.txt': 'Odometry',
    'imu_data.txt': 'IMU_Data',
    'imu_mag.txt': 'IMU_Magnetometer',
    'imu_angular.txt': 'IMU_Angular_Velocity',
}

header_hashes_list = []
labels = []

#reads all files
for file_name in file_names:
    data = read_file("odom.txt")
    #vector with hash calculation times
    header_hash_time = calculate_hash_time(data)
    #print(header_hash_time)
    header_hashes_list.append(header_hash_time)
    labels.append(file_labels[file_name])
    
plot_box_plot(header_hashes_list, labels)
    
