import sys
from web3 import Web3
from eth_account import Account
from web3.middleware import geth_poa_middleware
import time
from threading import Thread

import contract
import odom_structures

# *** Summary *** #

# This python code reads Odometry (Pose) ROS data from:
# pose1.txt - the Node 1 odomedry data file
# pose2.txt - the Node 2 odomedry data file
# pose3.txt - the Node 3 odomedry data file
# pose4.txt - the Node 4 odomedry data file

# Then,
# it creates transactions to a Blockchain IBFT private network and get its time.

# All data is sent in transactions made simultaneously.
# This is done using threads.

# Output files:
# out_times1.txt - the Node 1 transaction times
# out_times2.txt - the Node 2 transaction times
# out_times3.txt - the Node 3 transaction times
# out_times4.txt - the Node 4 transaction times
#                               (time in seconds)


# *** Code *** #


# Interacting once with the private blockchain network.
# Prints the transaction time and its receipt.
# Returns the transaction time.
def interact(w3, privateKey, odom, contractInterface):

    # Getting contract bytecode (bin)
    bytecode = contractInterface['bin']

    # Getting contract abi
    abi = contractInterface['abi']

    # Getting account info
    account = Account.from_key(privateKey)

    fromAddress = account.address

    # Contract Address (from Remix IDE)
    contractAddress = '0x7105A11e8487BfaF8c02aA6A7cdA5283f971107c'
    contract = w3.eth.contract(abi=abi, address=contractAddress)
    
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
        'gas': 100000,
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
    
    print('Done! Time:', aux_time, 'seconds.')

    # print('Receipt: ')
    # print(receipt)
    
    return aux_time


# Sending concurrent transactions using threads:
def sendTransactionsSimultaneously(w3, privateKeys, odomData, contractInterface):
    threads = []
    times = []
    for privateKey, odom in zip(privateKeys, odomData):
        thread = Thread(target=lambda: times.append(interact(w3, privateKey, odom, contractInterface)))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return times


# Main code:
def main():
    # Compiling solidity contract
    compiledSol = contract.compile_sol()

    # Retrieving the contract interface
    contract_id, contractInterface = compiledSol.popitem()

    # Web3.py instance
    rpc_url = 'http://127.0.0.1:8545'
    w3 = Web3(Web3.HTTPProvider(rpc_url))

    # For a private PoA IBFT network
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # Getting data from files
    files = ['pose1.txt', 'pose2.txt', 'pose3.txt', 'pose4.txt']
    odomData = []
    for file in files:
        odomData.append(odom_structures.cleanPose(file))
    odomData = list(zip(*odomData)) # Transposing

    # Sending transactions and getting its time
    transactionTimes = []
    # From Node1 to Node 4 private keys
    privateKeys = ['0xdadf3caf650d1b644852426ba2044b42dffc510693bfeedda2bfb1e4be30483d',
                    '0x4e271fb2bb984d98a912eca1b1de33b0963e4d6f0c41bbc807b1d266c9845ecf',
                    '0xfdc9d229ee345848288523ebf8aa4adcb2ec72aa061d56654420934e88b1529a',
                    '0x15585a55249d7ed614763f63e653ff3252c892b5a5c3cd3a021329551f1961c2']
    
    i = 1
    for odom in odomData:
        print("Transaction number: " + str(i))
        transactionTimes.append(sendTransactionsSimultaneously(w3, privateKeys, odom, contractInterface))
        i += 1
        
    # Transposing again to get each node time
    transactionTimes = [list(column) for column in zip(*transactionTimes)] 

    # Getting each node time
    i = 1
    for times in transactionTimes:
        with open('out_times' + str(i) + '.txt', 'a') as f:
            for time in times:
                f.write(str(time) + '\n')
        i += 1

if __name__ == "__main__":
    main()