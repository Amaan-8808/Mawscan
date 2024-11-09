import os
import subprocess
import sys
import time
import json
import threading
from datetime import datetime, timedelta
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from dateutil.relativedelta import relativedelta

def run_command(config):
    command = config['COMMAND']
    split_command = command.split(" ")
    
    # ~ NAME OF FILE TO BE EXECUTED
    flag = 0
    print("\nCOMMAND EXECUTING - ",str(command))
    
    if "python" not in split_command and "runme.py" not in split_command:
        flag = flag + 1
    
    if flag > 0:
        print("ARTIFICIAL COMMAND INJECTED !!! EXITING PROGRAM !!!")
        sys.exit()
        
    elif flag == 0:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("\nCOMMAND FOR CONFIG "+str(config["CONFIG"])+" EXECUTED SUCCESSFULLY")
    else:
        print("Command failed with error:")
        print(result.stderr)
        print(f"Running command: {command} at {datetime.now()}")

def schedule_tasks(config_data):
    
    for config in config_data['config']:

        if "FREQUENCY" in list(config.keys()):
            frequency = config['FREQUENCY']
        else:
            continue
        
        try:
            scheduled_time_str = config['TIME']
        except:
            scheduled_time_str = '00:00:00'

        try:
            scheduled_time = datetime.strptime(scheduled_time_str, '%H:%M:%S').time()
        except ValueError:
            scheduled_time = datetime.strptime(f"{scheduled_time_str}:00", '%H:%M:%S').time()

        scheduled_datetime = datetime.now().replace(hour=scheduled_time.hour, minute=scheduled_time.minute, second=scheduled_time.second, microsecond=0)
        
        if frequency == 'daily':
            
            while scheduled_datetime < datetime.now():
                scheduled_datetime += timedelta(days=1)

        elif frequency == 'hourly':

            while scheduled_datetime < datetime.now():
                scheduled_datetime += timedelta(hours=1)
        
        elif frequency == 'monthly':

            while scheduled_datetime < datetime.now():
                scheduled_date = scheduled_datetime.date()
                scheduled_date = scheduled_date + relativedelta(months=1)
                scheduled_datetime = datetime.combine(scheduled_date, scheduled_datetime.time())
                break

        delay_seconds = (scheduled_datetime - datetime.now()).total_seconds()
        
        timer = threading.Timer(delay_seconds, run_command, args=(config,))
        timer.start()

def main():
    
    print("\nSCHEDULER STARTED ...")
    
    while True:
        try:
            
            with open('data.json', 'r') as file:
                config_data = json.load(file)
                
            schedule_tasks(config_data)
            del config_data
            
            print("\nWAITING FOR 60 SECONDS")
            time.sleep(20)
            
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    
    if not os.path.exists("data.json"):
        print(f"FILE DATA.JSON DOES NOT EXIST. WAITING FOR IT TO BE CREATED ...")
        while not os.path.exists("data.json"):
            time.sleep(1)

    main()
