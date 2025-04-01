import matplotlib.pyplot as plt

# Plotting boxplot transaction times graph for comparison:
def plotGraph(nodeTimes):
    plt.figure(figsize=(10, 6))

    plt.boxplot(nodeTimes, labels=['Default System', 'Faulty Node 4'])

    # plt.xlabel('Nodes', fontsize=20)
    plt.ylabel('Transaction Time (s)', fontsize=22)
    # plt.title('Transaction Times', fontsize=20)
    plt.grid(True)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=14)
    plt.savefig('time-comparison-boxplot.png', dpi=300)

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

	# Rename the files if needed
    files1 = ['out_times1.txt', 'out_times2.txt', 
             'out_times3.txt', 'out_times4.txt']
    
    files2 = ['out_times12.txt', 'out_times22.txt', 
             'out_times32.txt']

    times = []

    # Reading each file data
    times1, t = readFiles(files1)

    times2, t = readFiles(files2)

    times = [times1, times2]

    # Plotting graph and saving image
    plotGraph(times)

if __name__ == "__main__":
    main()
