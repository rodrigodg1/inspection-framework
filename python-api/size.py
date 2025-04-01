import sys
import odom_structures

def main():
    print('Processing data from files...')

    # Getting data from files
    files = ['../data/pose1.txt', '../data/pose2.txt', '../data/pose3.txt', '../data/pose4.txt']
    odomData = []
    for file in files:
        odomData.append(odom_structures.cleanPose(file))
    odomData = list(zip(*odomData)) # Transposing
    
    size = 0
    for odom in odomData:
        for node in odom:
            size += sys.getsizeof(node)

    with open('out_size.txt', 'a') as f:
        f.write(f'Total size in bytes: {size}')

if __name__ == "__main__":
    main()