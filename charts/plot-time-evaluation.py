import matplotlib.pyplot as plt
import numpy as np

# Plotting function
def plot_box_plot(transaction_times):
    # plt.style.use('seaborn-white')  # Change the box plot style
    fig, ax = plt.subplots(figsize=(10, 6))  # Adjust the figure size
    
    # Convert strings to floats
    transaction_times = [float(time.strip()) for time in transaction_times]

    # Create box plot
    ax.boxplot([transaction_times], labels=['Odometry'], widths=0.5)

    ax.set_ylabel('Time in seconds', fontsize=20)
    ax.tick_params(axis='both', labelsize=20)
    ax.grid(axis='y') # Add gridlines

    plt.savefig("mygraph.png")

def main():
    with open('out_times.txt', 'r') as f:
        times = f.readlines()

    # Removing first transaction, since its time is unusual
    times.pop(0)

    plot_box_plot(times)

    times = [float(time.strip()) for time in times]

    # Getting data
    with open('out_time_data.txt', 'w') as f:
        f.write('Mean: ' + str(np.mean(times)) + '\n')
        f.write('STD: ' + str(np.std(times)) + '\n')
        f.write('Min: ' + str(np.min(times)) + '\n')
        f.write('Max: ' + str(np.max(times)) + '\n')

if __name__ == "__main__":
    main()