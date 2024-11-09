# import psutil
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation

# # Function to collect CPU utilization data for one second
# def collect_cpu_utilization(interval):
#     return psutil.cpu_percent(interval=interval)

# # Main function to collect data and plot the graph
# def main(duration=60, interval=1):
#     print(f"Collecting CPU utilization data for {duration} seconds with an interval of {interval} second(s).")
    
#     cpu_percentages = []
#     times = []

#     # Function to update the graph
#     def update(frame):
#         cpu_percentage = collect_cpu_utilization(interval)
#         cpu_percentages.append(cpu_percentage)
#         times.append(frame)
#         ax.clear()
#         ax.plot(times, cpu_percentages, marker='o', linestyle='-', color='b')
#         ax.set_title('CPU Utilization Over Time')
#         ax.set_xlabel(f'Time (seconds, interval={interval}s)')
#         ax.set_ylabel('CPU Utilization (%)')
#         ax.grid(True)

#     fig, ax = plt.subplots(figsize=(10, 5))

#     # Animate the plot with data updates
#     ani = FuncAnimation(fig, update, frames=range(duration), interval=interval * 1000)

#     plt.show()

# if __name__ == "__main__":
#     # Running the main function with duration and interval
#     main(duration=60, interval=1)

# ! OLD UPDATE FUNCTION ------------

    # Function to update the graph
    # def update(frame):
    #     cpu_percentage = collect_cpu_utilization(interval)
    #     cpu_percentages.append(cpu_percentage)
    #     current_time = datetime.now()  # Get the current local time
    #     times.append(current_time)
    #     ax.clear()
    #     ax.plot(times, cpu_percentages, marker='o', linestyle='-', color='b')
    #     ax.set_title('CPU Utilization Over Time')
    #     ax.set_xlabel('Time')
    #     ax.set_ylabel('CPU Utilization (%)')
    #     ax.grid(True)
    #     # Format x-axis to display time
    #     ax.set_xticks(times)
    #     ax.set_xticklabels([time.strftime('%H:%M:%S') for time in times])

# ! WORKING

import psutil
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime, timedelta

# Function to collect CPU utilization data for one second
def collect_cpu_utilization(interval):
    return psutil.cpu_percent(interval=interval)

# Main function to collect data and plot the graph
def cpumain(duration=60, interval=1):
    print(f"Collecting CPU utilization data for {duration} seconds with an interval of {interval} second(s).")

    cpu_percentages = []
    times = []
    
    # Function to update the graph
    # Function to update the graph
    def update(frame):
        cpu_percentage = collect_cpu_utilization(interval)
        cpu_percentages.append(cpu_percentage)
        current_time = datetime.now()  # Get the current local time
        times.append(current_time)
        ax.clear()
        ax.plot(times, cpu_percentages, marker='o', linestyle='-', color='b')
        ax.set_title('CPU Utilization Over Time')
        ax.set_xlabel('Time')
        ax.set_ylabel('CPU Utilization (%)')
        ax.grid(True)
        
        # Update x-axis labels and limits
        num_labels = 6
        if len(times) > num_labels:
            start_index = max(0, len(times) - num_labels)
            interval_index = max(1, (len(times) - start_index) // num_labels)
            visible_times = times[start_index::interval_index]
            ax.set_xticks(visible_times)
            ax.set_xticklabels([time.strftime('%H:%M:%S') for time in visible_times])
            ax.set_xlim(times[start_index], times[-1])  # Set x-axis limits
        else:
            ax.set_xticks(times)
            ax.set_xticklabels([time.strftime('%H:%M:%S') for time in times])
            ax.set_xlim(times[0], times[-1])  # Set x-axis limits



    fig, ax = plt.subplots(figsize=(10, 5))

    # Animate the plot with data updates
    ani = FuncAnimation(fig, update, frames=range(duration), interval=interval * 1000)

    plt.show()