import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from datetime import datetime, timedelta
import os
import threading
import csv
from pynput import keyboard, mouse
import time

# Function to convert time string to datetime object
def str_to_time(time_str):
    return datetime.strptime(time_str, '%H:%M:%S')

def track_idle_activity(idle_threshold=5, csv_file='idle_times.csv'):
    # Global variables to track the last activity time and idle periods
    last_activity_time = time.time()
    idle_start_time = None

    # Initialize the CSV file and write the header
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Idle Start Time', 'Idle End Time', 'Idle'])

    def on_activity():
        nonlocal last_activity_time, idle_start_time
        current_time = time.time()
        idle_time = current_time - last_activity_time
        
        if idle_time > idle_threshold:
            pass
        else:
            if idle_start_time is not None:
                idle_end_time = last_activity_time
                idle_start_str = datetime.fromtimestamp(idle_start_time).strftime('%H:%M:%S')
                idle_end_str = datetime.fromtimestamp(idle_end_time).strftime('%H:%M:%S')
                print(f"Idle from {idle_start_str} to {idle_end_str}")

                # Write to CSV
                with open(csv_file, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([idle_start_str, idle_end_str, 1])

                idle_start_time = None

        last_activity_time = current_time

    def check_idle_time():
        nonlocal idle_start_time, last_activity_time
        while True:
            current_time = time.time()
            idle_time = current_time - last_activity_time
            
            if idle_time > idle_threshold and idle_start_time is None:
                idle_start_time = last_activity_time
                print("REACHED THRESHOLD")
            
            time.sleep(1)

    # Keyboard listener
    def on_key_press(key):
        on_activity()

    def on_key_release(key):
        on_activity()

    keyboard_listener = keyboard.Listener(on_press=on_key_press, on_release=on_key_release)

    # Mouse listener
    def on_click(x, y, button, pressed):
        on_activity()

    def on_move(x, y):
        on_activity()

    mouse_listener = mouse.Listener(on_click=on_click, on_move=on_move)

    # Start the listeners in separate threads
    keyboard_listener.start()
    mouse_listener.start()

    # Start the idle time checker
    idle_checker_thread = threading.Thread(target=check_idle_time)
    idle_checker_thread.daemon = True
    idle_checker_thread.start()

    # Keep the main thread running
    keyboard_listener.join()
    mouse_listener.join()

def plot_dynamic_idle_activity(csv_file = "idle_times.csv", wait_time=10):
    # Wait for a specified duration before reading the CSV file
    print(f"Waiting for {wait_time} seconds to populate CSV file...")
    time.sleep(wait_time)

    # Function to read and process the CSV file
    def read_and_process_csv():
        if not os.path.exists(csv_file):
            return [], []

        df = pd.read_csv(csv_file)

        times = []
        activity = []

        for i in range(len(df)):
            idle_start = str_to_time(df.loc[i, 'Idle Start Time'])
            idle_end = str_to_time(df.loc[i, 'Idle End Time'])
            
            if i == 0:
                times.append(idle_start)
                activity.append(1)
            else:
                prev_idle_end = str_to_time(df.loc[i-1, 'Idle End Time'])
                # Fill the gap with 0
                gap_start = prev_idle_end + timedelta(seconds=1)
                while gap_start < idle_start:
                    times.append(gap_start)
                    activity.append(0)
                    gap_start += timedelta(seconds=1)
            
            # Add idle period with 1
            current_time = idle_start
            while current_time <= idle_end:
                times.append(current_time)
                activity.append(1)
                current_time += timedelta(seconds=1)
        
        return times, activity

    # Initial read and process of the CSV file
    times, activity = read_and_process_csv()

    # Create the initial plot
    fig, ax = plt.subplots(figsize=(12, 6))
    line, = ax.plot(times, activity, drawstyle='steps-post')
    ax.set_xlabel('Time')
    ax.set_ylabel('Activity')
    ax.set_title('Idle and Active Periods')
    ax.set_ylim(-0.1, 1.1)
    ax.grid(True)

    # Function to update the plot
    def update(frame):
        times, activity = read_and_process_csv()
        line.set_data(times, activity)
        ax.set_xlim(min(times) if times else datetime.now(), max(times) if times else datetime.now() + timedelta(seconds=1))
        return line,

    # Animation function
    ani = FuncAnimation(fig, update, interval=1000)

    # Show the plot
    plt.show()