import sys
import matplotlib.pyplot as plt

def read_file(file_name):
    with open(file_name, 'r') as file:
        data = file.read()
    return data

def calculate_block_sizes(data):
    header_blocks = data.strip().split('---')
    header_sizes = []

    for block in header_blocks:
        if block:
            header_sizes.append(sys.getsizeof(block))
    return header_sizes

def plot_box_plot(header_sizes_list, file_names):
    plt.style.use('seaborn-white')  # Change the box plot style
    fig, ax = plt.subplots(figsize=(10, 6))  # Adjust the figure size
    ax.boxplot(header_sizes_list, labels=file_names, widths=0.5)
    ax.set_title('ROS messages', fontsize=20)
    ax.set_ylabel('Size in Bytes', fontsize=16)
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

header_sizes_list = []
labels = []

for file_name in file_names:
    data = read_file(file_name)
    header_sizes = calculate_block_sizes(data)
    header_sizes_list.append(header_sizes)
    labels.append(file_labels[file_name])

plot_box_plot(header_sizes_list, labels)
