import sys
import psycopg2
from psycopg2 import sql
import time
from threading import Thread

import odom_structures

# *** Summary *** #

# This python code reads Odometry (Pose) ROS data from:
# pose1.txt - the Node 1 odomedry data file
# pose2.txt - the Node 2 odomedry data file
# pose3.txt - the Node 3 odomedry data file
# pose4.txt - the Node 4 odomedry data file

# Then,
# it creates transactions to PostgreSQL database and get its time.

# All data is sent in transactions made simultaneously.
# This is done using threads.

# Output files:
# out_times1.txt - the Node 1 transaction times
# out_times2.txt - the Node 2 transaction times
# out_times3.txt - the Node 3 transaction times
# out_times4.txt - the Node 4 transaction times
#                               (time in seconds)

# *** Code *** #

# Dropping table and creating a new one, to make transactions
def setup_database(db):
    cur = db.cursor()
    cur.execute('''
        DROP TABLE IF EXISTS transactions;
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id SERIAL PRIMARY KEY,
            seq INTEGER,
            secs INTEGER,
            nsecs INTEGER,
            frame_id TEXT,
            child_frame_id TEXT,
            position_x REAL,
            position_y REAL,
            position_z REAL,
            orientation_x REAL,
            orientation_y REAL,
            orientation_z REAL,
            orientation_w REAL,
            covariance TEXT,
            linear_x REAL,
            linear_y REAL,
            linear_z REAL,
            angular_x REAL,
            angular_y REAL,
            angular_z REAL,
            twist_covariance TEXT
        );
    ''')
    db.commit()
    cur.close()

# Interacting with the PostgreSQL database, by inserting odom data into table,
# and collecting the transaction time
def interact(db, odom):
    with db.cursor() as cur:
        sql_query = sql.SQL('''
            INSERT INTO transactions (
                seq, secs, nsecs, frame_id, child_frame_id, 
                position_x, position_y, position_z, 
                orientation_x, orientation_y, orientation_z, orientation_w,
                covariance, linear_x, linear_y, linear_z, 
                angular_x, angular_y, angular_z, twist_covariance
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        ''')

        values = (
            odom.seq, odom.secs, odom.nsecs, odom.frame_id, odom.child_frame_id,
            odom.position_x, odom.position_y, odom.position_z,
            odom.orientation_x, odom.orientation_y, odom.orientation_z, odom.orientation_w,
            str(odom.covariance), odom.linear_x, odom.linear_y, odom.linear_z,
            odom.angular_x, odom.angular_y, odom.angular_z, str(odom.twist_covariance)
        )

        # Getting time
        start = time.time()
        cur.execute(sql_query, values)
        db.commit()
        aux_time = time.time() - start

        print('Done! Time:', aux_time, 'seconds.')
        return aux_time

# Function used to send transactions simultaneously, using Threads
def sendTransactionsSimultaneously(db, odomData):
    threads = []
    times = []
    for odom in odomData:
        thread = Thread(target=lambda: times.append(interact(db, odom)))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    return times

# Reading odom (pose) data from the files,
# returns the odomData list, with the data read for each file
def readOdomData(files):
    print('Reading files...')
    odomData = []
    for file in files:
        odomData.append(odom_structures.cleanPose(file))
    print('Done!')
    return list(zip(*odomData)) # Transposing

# Writing the times collected into output files
def writeTimesToFile(transactionTimes):
    print('Writing times...')
    transactionTimes = [list(column) for column in zip(*transactionTimes)]
    for i, times in enumerate(transactionTimes, start=1):
        with open(f'out_times{i}.txt', 'a') as f:
            for time in times:
                f.write(f'{time}\n')
    print('Done!')

# Main function
def main():
    # You need to set these constants correctly
    db = psycopg2.connect(
        dbname='', 
        user='', 
        password='', 
        host='localhost', 
        port='5432'
    )
    
    setup_database(db)
    
    files = ['pose1.txt', 'pose2.txt', 'pose3.txt', 'pose4.txt']

    odomData = readOdomData(files)

    transactionTimes = []
    for i, odom in enumerate(odomData, start=1):
        print(f"Transaction number: {i}")
        transactionTimes.append(sendTransactionsSimultaneously(db, odom))
    
    writeTimesToFile(transactionTimes)
    
    db.close()

if __name__ == "__main__":
    main()