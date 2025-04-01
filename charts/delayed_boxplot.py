import matplotlib.pyplot as plt

# Plotting boxplot transaction times graph for the delayed evaluations:
def plotGraph(nodeTimes):
    plt.figure(figsize=(10, 6))

    plt.boxplot(nodeTimes, labels=['100ms Delay', '200ms Delay', '300ms Delay'])

    # plt.xlabel('Nodes', fontsize=20)
    plt.ylabel('Transaction Time (s)', fontsize=22)
    # plt.title('Transaction Times', fontsize=20)
    plt.grid(True)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=14)
    plt.savefig('delay-boxplot.png', dpi=300)

# Reading input file data:
def readFiles(files):
    times = []
    transactions = []

    for fileName in files:
        with open(fileName, 'r') as f:
            num = 1
            for line in f:
                transactions.append(num)
                times.append(float(line))
                num += 1
    return times, transactions

def main():

    # Setting files names
    files1 = ['100msdelay_out1.txt', '100msdelay_out2.txt',
              '100msdelay_out3.txt', '100msdelay_out4.txt']
    
    files2 = ['200msdelay_out1.txt', '200msdelay_out2.txt',
              '200msdelay_out3.txt', '200msdelay_out4.txt']
    
    files3 = ['300msdelay_out1.txt', '300msdelay_out2.txt',
              '300msdelay_out3.txt', '300msdelay_out4.txt']
    
    times = []

    # Reading each file data
    times1, t = readFiles(files1)

    times2, t = readFiles(files2)

    times3, t = readFiles(files3)

    times = [times1, times2, times3]

    # Plotting graph and saving image
    plotGraph(times)

if __name__ == "__main__":
    main()
