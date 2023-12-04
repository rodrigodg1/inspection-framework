# This python code reads Odometry ROS data from a odom.txt file
# It creates transactions to a Blockchain network with this data
# and evaluates the transaction time using python time library.

from dataclasses import dataclass
import sys
import yaml
from web3 import Web3
from eth_account import Account
from solcx import compile_source
from web3.middleware import geth_poa_middleware
import time

# Odom Data structure
class Data:
	seq: int = -1
	secs: int = -1
	nsecs: int = -1
	frame_id: str = ""
	child_frame_id: str = ""
	position_x: int = -1
	position_y: int = -1
	position_z: int = -1
	orientation_x: int = -1
	orientation_y: int = -1
	orientation_z: int = -1
	orientation_w: int = -1
	covariance: list = []
	linear_x: int = -1
	linear_y: int = -1
	linear_z: int = -1
	angular_x: int = -1
	angular_y: int = -1
	angular_z: int = -1
	twist_covariance: list = []

# Function used to read the odom.txt file
def read_file(file_name):
	with open(file_name, 'r') as file:
		data = file.read()
	return data

# Function used to convert txt data into Data structure
def clear(block):
	
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

# Function used to 'clean' all file data
def clean_odom(file_name):

	# reads imu_data.txt file
	data = read_file(file_name)

	# cleans header
	blocks = data.strip().split('---')

	# converts block txt data to Data structure
	clean_blocks = []
	for block in blocks:
		if block:
			clean_blocks.append(clear(block))
			
	return clean_blocks

# Debugging clean_odom
def print_odom(odom_data):
    for odom in odom_data:
            print('--This--')
            print(odom.seq)
            print(odom.secs)
            print(odom.nsecs)
            print(odom.frame_id)
            print(odom.child_frame_id)
            print([odom.position_x,
                odom.position_y,
                odom.position_z])
            print([odom.orientation_x,
                odom.orientation_y,
                odom.orientation_z,
                odom.orientation_w])
            print(odom.covariance)
            print([odom.linear_x,
                odom.linear_y,
                odom.linear_z])
            print([odom.angular_x,
                odom.angular_y,
                odom.angular_z])
            print(odom.twist_covariance)

# This function is used to compile our Robot Local Data smart contract
def compile_sol():
    # Share data solidity source code
    compiled_sol = compile_source(
        '''
        // SPDX-License-Identifier: GPL-3.0

        pragma solidity >=0.8.2 <0.9.0;

        contract RobotLocalizationData {

            // Private variable that stores the place of inspection
            string private place;
            // Private variable that stores the date of inspection
            string private date;
            // Private variable that stores an array of inspector adresses
            address[] private inspectors;

            constructor() {
                place = "aqui";
                date = "outubro";
            }

            struct Time {
                uint32 secs;
                uint32 nsecs;
            }

            struct Vector3 {
                uint32 x;
                uint32 y;
                uint32 z;
            }

            struct Quaternion {
                uint32 x;
                uint32 y;
                uint32 z;
                uint32 w;
            }

            struct Pose {
                Vector3 position;
                Quaternion orientation;
            }

            struct Twist {
                Vector3 linear;
                Vector3 angular;
            }

            struct Header {
                uint32 seq;
                Time stamp;
                string frame_id;
            }

            struct PoseWithCovariance {
                Pose pose;
                uint32[36] covariance;
            }

            struct TwistWithCovariance {
                Twist twist;
                uint32[36] covariance;
            }

            struct Orientation {
                Quaternion o;
                uint[9] covariance;
            }

            struct Group {
                Vector3 a;
                uint[9] covariance;
            }

            struct Odom {
                Header header;
                string child_frame_id;
                PoseWithCovariance pose;
                TwistWithCovariance twist;
            }

            struct ImuAngular {
                Header header; 
                Vector3 vector;
            }

            struct ImuMag {
                Header header;
                Vector3 vector;
            }

            struct ImuData {
                Header header;
                Orientation orientation;
                Group angular_velocity;
                Group linear_acceleration;
            }

            // Public variables that stores robot data
            Odom public odom;
            ImuAngular public imu_angular;
            ImuMag public imu_mag;
            ImuData public imu_data;

            function updateOdom(
                uint32 seq,
                uint32 stampSecs,
                uint32 stampNsecs,
                string memory frameId,
                string memory childFrameId,
                uint32[3] memory position,
                uint32[4] memory orientation,
                uint32[36] memory poseCovariance,
                uint32[3] memory linear,
                uint32[3] memory angular,
                uint32[36] memory twistCovariance
            ) public {
                odom.header.seq = seq;
                odom.header.stamp.secs = stampSecs;
                odom.header.stamp.nsecs = stampNsecs;
                odom.header.frame_id = frameId;

                odom.child_frame_id = childFrameId;

                odom.pose.pose.position.x = position[0];
                odom.pose.pose.position.y = position[1];
                odom.pose.pose.position.z = position[2];

                odom.pose.pose.orientation.x = orientation[0];
                odom.pose.pose.orientation.y = orientation[1];
                odom.pose.pose.orientation.z = orientation[2];
                odom.pose.pose.orientation.w = orientation[3];

                for (uint256 i = 0; i < 36; i++) {
                    odom.pose.covariance[i] = poseCovariance[i];
                }

                odom.twist.twist.linear.x = linear[0];
                odom.twist.twist.linear.y = linear[1];
                odom.twist.twist.linear.z = linear[2];

                odom.twist.twist.angular.x = angular[0];
                odom.twist.twist.angular.y = angular[1];
                odom.twist.twist.angular.z = angular[2];

                for (uint256 i = 0; i < 36; i++) {
                    odom.twist.covariance[i] = twistCovariance[i];
                }
            }

            function updateImuMag(
                uint32 seq,
                uint32 stampSecs,
                uint32 stampNsecs,
                string memory frameId,
                uint32[3] memory position
            ) public {
                imu_mag.header.seq = seq;
                imu_mag.header.stamp.secs = stampSecs;
                imu_mag.header.stamp.nsecs = stampNsecs;
                imu_mag.header.frame_id = frameId;

                imu_mag.vector.x = position[0];
                imu_mag.vector.y = position[1];
                imu_mag.vector.z = position[2];
            }

            function updateImuAngular(
                uint32 seq,
                uint32 stampSecs,
                uint32 stampNsecs,
                string memory frameId,
                uint32[3] memory position
            ) public {
                imu_angular.header.seq = seq;
                imu_angular.header.stamp.secs = stampSecs;
                imu_angular.header.stamp.nsecs = stampNsecs;
                imu_angular.header.frame_id = frameId;

                imu_angular.vector.x = position[0];
                imu_angular.vector.y = position[1];
                imu_angular.vector.z = position[2];
            }

            function updateImuData(
                uint32 seq,
                uint32 stampSecs,
                uint32 stampNsecs,
                string memory frameId,
                uint32[4] memory orientation,
                uint32[9] memory o_covariance,
                uint32[3] memory angular_velocity,
                uint32[9] memory av_covariance,
                uint32[3] memory linear_acceleration,
                uint32[9] memory la_covariance
            ) public {
                imu_data.header.seq = seq;
                imu_data.header.stamp.secs = stampSecs;
                imu_data.header.stamp.nsecs = stampNsecs;
                imu_data.header.frame_id = frameId;

                imu_data.orientation.o.x = orientation[0];
                imu_data.orientation.o.y = orientation[1];
                imu_data.orientation.o.z = orientation[2];
                imu_data.orientation.o.w = orientation[3];
                
                for(uint i = 0; i < 9; i++){
                    imu_data.orientation.covariance[i] = o_covariance[i];
                }

                imu_data.angular_velocity.a.x = angular_velocity[0];
                imu_data.angular_velocity.a.y = angular_velocity[0];
                imu_data.angular_velocity.a.z = angular_velocity[2];

                for(uint i = 0; i < 9; i++){
                    imu_data.angular_velocity.covariance[i] = av_covariance[i];
                }

                imu_data.linear_acceleration.a.x = linear_acceleration[0];
                imu_data.linear_acceleration.a.y = linear_acceleration[0];
                imu_data.linear_acceleration.a.z = linear_acceleration[2];

                for(uint i = 0; i < 9; i++){
                    imu_data.linear_acceleration.covariance[i] = la_covariance[i];
                }
            }
        }
        ''',
        output_values=['abi', 'bin']
    )
    return compiled_sol

# This function is used to interact with the blockchain
def interact(w3, compiled_sol, odom_data):
    # Retrieve the contract interface
    contract_id, contract_interface = compiled_sol.popitem()

    # Getting contract bytecode (bin)
    bytecode = contract_interface['bin']

    # Getting contract abi
    abi = contract_interface['abi']

    # Private Key (account that will send transactions)
    privateKey = '8f2a55949038a9610f50fb23b5883af3b4ecb3c3bb792cbcefbd1542c692be63'

    account = Account.from_key(privateKey)

    fromAddress = account.address

    # Contract Address and Getting contract
    contractAddress = '0x9FBDa871d559710256a2502A2517b794B482Db40'
    contract = w3.eth.contract(abi=abi, address=contractAddress)
    
    transaction_times = []
    
    for odom in odom_data:
        print('Transacting...')
        # Setting function and getting data
        data = contract.encodeABI(fn_name='updateOdom', args=[odom.seq,
                                                            odom.secs,
                                                            odom.nsecs,
                                                            odom.frame_id,
                                                            odom.child_frame_id,
                                                            [odom.position_x,
                                                            odom.position_y,
                                                            odom.position_z],
                                                            [odom.orientation_x,
                                                            odom.orientation_y,
                                                            odom.orientation_z,
                                                            odom.orientation_w],
                                                            odom.covariance,
                                                            [odom.linear_x,
                                                            odom.linear_y,
                                                            odom.linear_z],
                                                            [odom.angular_x,
                                                            odom.angular_y,
                                                            odom.angular_z],
                                                            odom.twist_covariance]
                                                            )

        nonce = w3.eth.get_transaction_count(fromAddress)
        rawtxOptions = {
            'to': contractAddress,  
            'value': 0,
            'gas': 2000000,
            'gasPrice': w3.to_wei('50', 'gwei'),
            'nonce': nonce,
            'data': data,  
            'chainId': 1337
        }

        start = time.time()
        # Interacting with contract function
        signed_txn = w3.eth.account.sign_transaction(rawtxOptions, privateKey)

        # Send transaction
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

        # Transaction Done
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        
        aux_time = time.time() - start
        transaction_times.append(aux_time)
        
        print('Done! Time:', aux_time, 'seconds.')

        print('Receipt: ')
        print(receipt)
    
    return transaction_times

# Main code
def main():
    # Compiling solidity contract
    compiled_sol = compile_sol()

    # Web3.py instance
    rpc_url = 'http://127.0.0.1:8545'
    w3 = Web3(Web3.HTTPProvider(rpc_url))

    # For PoA network
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # Converting odom.txt to Data structure
    odom_data = clean_odom('odom.txt')

    # Sending transactions and getting its time
    transaction_times = interact(w3, compiled_sol, odom_data)

    with open('out_times.txt', 'a') as f:
        for time in transaction_times:
            f.write(str(time) + '\n')

if __name__ == "__main__":
    main()
