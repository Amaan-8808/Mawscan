import csv
import hashlib
import subprocess
import time
import psutil
import os
import json
import requests
import vt
from dotenv import get_key, load_dotenv

def get_system_idle_time():
    idle_time = int(subprocess.check_output("xprintidle").decode('utf-8').strip())
    return idle_time / 1000

def wait_for_idle():
    while True:
        try:

            idle_time = get_system_idle_time()
            
            print(f"System idle time: {idle_time} seconds")

            if idle_time > 15:
                dynamic()
                print("System is idle")
            
            time.sleep(1)
            
        except KeyboardInterrupt:
            break

def calculate_sha256(file_path):
    """Calculate SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def dynamic():
    
    # ^ DEFINE FIELDS TO EXTRACT
    
    extra_fields = ['pid', 'name', 'username', 'connections', 'cmdline', 'exe', 'nice', 'open_files','cpu_percent', 'memory_percent', 'create_time']
    
    # ^ EXTRACT DATA OF RUNNING PROCESS
    
    processes = []
    for proc in psutil.process_iter(extra_fields):
        
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    if os.path.exists('processes.csv'):
        os.remove('processes.csv')
        
    with open('processes.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=extra_fields)
        writer.writeheader()
    
    # ^ WRITE PROCESS INFO INTO CSV
    
    cmdlist = []
    with open('processes.csv', 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=extra_fields)

        for process in processes:
            
            try:
                writer.writerow(process)
                if len(process['cmdline']) > 0:                    
                    cmdlist.append(process['cmdline'][0])
            
            except KeyError:
                pass
    
    # ^ check if file exists
    cmdlist = list(set(cmdlist))
    
    if os.path.exists("verified_process.json"):
        with open("verified_process.json", 'r') as json_file:
            data_list = json.load(json_file)
        
        verified_list = []
        for i in data_list:
            verified_list.append(i["process"])
        
        # ^ remove approved processes
        verified_list = list(set(verified_list))
        
        for i in cmdlist:
            if i in verified_list:
                print("removed process - ", i)
                cmdlist.remove(i)
        
    # ^ check virustotal for current processes
    print("\n")
    load_dotenv()
    api_key = get_key('.env', "VT_API_KEY")
    malw_list = []

    for i in cmdlist:
        
        print("ANALYSING FILE: ", i)
        print("WAITING FOR VIRUSTOTAL ANALYSIS...")
        
        # ^ calculate sha256 hash of file
        try:
            file_hash = calculate_sha256(i)
        except Exception as e:
            print(e)
            print("cannot test file - ",str(i))
            print("\n")
            continue
        
        # ^ virustotal api request
        url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
        headers = {"accept": "application/json", "x-apikey": api_key}
        response = requests.get(url, headers=headers)
        val = response.json()
        keys = list(val.keys())
        
        if ("error" not in keys):
        
            first_check = val["data"]["attributes"]["last_analysis_stats"]
            
            # ^ count of bad & good
            bad_count = int(first_check["malicious"]) + int(first_check["suspicious"])
            neutral_count = int(first_check["undetected"])
            good_count = int(first_check["harmless"])
            
            # ^ give verdict of benign & malicious
            if bad_count > neutral_count and bad_count > good_count:
                
                malw_list.append(i)
                
                # ^ check if file exists
                if os.path.exists("malicious_process.json"):
                    
                    data = []
                    
                    with open("malicious_process.json", 'r') as json_file:
                        data = json.load(json_file)
                    
                    data.append({"process" : i})
                    
                    with open("malicious_process.json", "w") as json_file:
                        json.dump(data, json_file, indent=4)
                
                # ^ create file if it doesn't exist
                else:
                    
                    data = []
                    
                    data.append({"process" : i})
                    
                    with open("malicious_process.json", "w") as json_file:
                        json.dump(data, json_file, indent=4)
                
                print("MALICIOUS PROCESS\n")
            
            elif good_count > bad_count:
                
                if os.path.exists("verified_process.json"):
                    
                    data = []
                    
                    with open("verified_process.json", 'r') as json_file:
                        data = json.load(json_file)
                    
                    data.append({"process" : i})
                    
                    with open("verified_process.json", "w") as json_file:
                        json.dump(data, json_file, indent=4)
                
                else:
                    
                    data = []
                    
                    data.append({"process" : i})
                    
                    with open("verified_process.json", "w") as json_file:
                        json.dump(data, json_file, indent=4)
                
                print("VERIFIED PROCESS\n")
            
        else:
            
            if os.path.exists("verified_process.json"):
                
                data = []
                
                with open("verified_process.json", 'r') as json_file:
                    data = json.load(json_file)
                
                data.append({"process" : i})
                
                with open("verified_process.json", "w") as json_file:
                    json.dump(data, json_file, indent=4)
            
            else:
                
                data = []
                
                data.append({"process" : i})
                
                with open("verified_process.json", "w") as json_file:
                    json.dump(data, json_file, indent=4)
            
            print("VERIFIED PROCESS\n")
            