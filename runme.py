import json
import multiprocessing
import re
import shlex
import subprocess
import sys
import threading
import webbrowser

# from scanner.cpu.cpu import cpumain
from scanner.clamproc_scanner import scan_running_processes
from scanner.dynamic.vt_hash import wait_for_idle

# from scanner.idle.idle_map import plot_dynamic_idle_activity, track_idle_activity
from utils.identify import run_identify
from utils.create_table import create_table
from scanner.md5_scanner import md5_scanner
from scanner.sha1_scanner import sha1_scanner
from scanner.sha256_scanner import sha256_scanner

# from scanner.sha512_scanner import sha512_scanner
from scanner.yara_scanner import yara_scanner
import os
import argparse
import time


def decision(choice, filetype, processes, looping=False):

    # ~ YARA CONTINUOUS SCANNING
    if choice == "YARA":
        if looping:
            while True:
                yara_scanner(filetype, processes)
        else:
            yara_scanner(filetype, processes)

    # ~ MD5 CONTINUOUS SCANNING
    elif choice == "MD5":
        if looping:
            while True:
                md5_scanner(filetype, processes)
        else:
            md5_scanner(filetype, processes)

    # ~ SHA1 CONTINUOUS SCANNING
    elif choice == "SHA1":
        if looping:
            while True:
                sha1_scanner(filetype, processes)
        else:
            sha1_scanner(filetype, processes)

    # ~ SHA256 CONTINUOUS SCANNING
    elif choice == "SHA256":
        if looping:
            while True:
                sha256_scanner(filetype, processes)
        else:
            sha256_scanner(filetype, processes)

    # # ~ SHA512 CONTINUOUS SCANNING
    # elif choice == "SHA512":
    #     if looping:
    #         while True:
    #             sha512_scanner(filetype, processes)
    #     else:
    #         sha512_scanner(filetype, processes)

    elif choice == "VT":
        
        wait_for_idle()
    
    elif choice == "CLAMAV":
        
        infected_processes = scan_running_processes()
        
        if infected_processes:

            for process_name, process_id, result in infected_processes:
                print(f"  Process: {process_name} (PID: {process_id}), Result: {result}")
        
        else:
            print("No infected processes found.")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    # ~ FORCE INDEXING TO REFRESH CACHE

    # ! ============================================= THREADS / PROCESSES ====================================================

    # ~ THREADS
    parser.add_argument(
        "-t",
        "--threads",
        type=int,
        default=10,
        help="Specify the number of threads required for indexing (default=10)",
    )

    # ~ PROCESSES
    parser.add_argument(
        "-p",
        "--processes",
        type=int,
        default=10,
        help="Specify the number of processes required for scanning (default=10)",
    )

    # ! ============================================= CONFIG / SCHEDULE FLAG ====================================================

    # ~ SAVE SCAN CONFIG
    parser.add_argument(
        "--config",
        type=str,
        metavar="CONFIG_NAME",
        help="Save the command to Redis with the specified number",
    )

    # ! ============================================= TIME FLAG ====================================================

    parser.add_argument("--time", type=str, help="Time to run the task (e.g., 14:30)")

    frequency_group = parser.add_mutually_exclusive_group()
    
    frequency_group.add_argument(
        "--daily", action="store_true", help="Run the task daily"
    )
    
    frequency_group.add_argument(
        "--monthly", action="store_true", help="Run the task monthly"
    )
    
    frequency_group.add_argument(
        "--hourly", action="store_true", help="Run the task hourly"
    )

    # ! ============================================= FILE TYPE FOR SCANNING FLAG ====================================================

    # ~ FILETYPE TO SCAN
    parser.add_argument(
        "--type",
        choices=["application", "text", "image", "video", "all"],
        default="application",
        help="Specify the filetype that you want to scan (default=application)",
    )

    # ! ============================================= TYPE OF SCAN ====================================================

    # ~ CONTINUOUS SCANNING
    scanner_type = parser.add_mutually_exclusive_group(required=True)
    
    scanner_type.add_argument(
        "--static",
        action="store_true",
        help="Perform static scanning"
    )
    
    scanner_type.add_argument(
        "--dynamic",
        action="store_true",
        help="Perform dynamic scanning"
    )
    
    scanner_type.add_argument(
        "--index",
        action="store_true",
        help="Refresh indexing cache"
    )
    
    scanner_type.add_argument(
        "--schedule",
        type=str,
        metavar="CONFIG_NAME",
        help="Schedule the scan to run at a specific time",
    )
    
    scanner_type.add_argument(
        "--delete",
        action="store_true",
        help="Delete configuration",
    )
    
    scanner_type.add_argument(
        "--dashboard",
        action="store_true",
        help="Specify the filetype that you want to scan (default=application)",
    )
    
    # ! ============================================= DYNAMIC MALWARE SCAN ====================================================

    # ~ DYNAMIC MALWARE ANALYSIS
    dynamic_scan_group = parser.add_mutually_exclusive_group()
    
    dynamic_scan_group.add_argument(
        "--virustotal",
        action="store_true",
        help="Utilise virustotal for dynamic malware scanning",
    )
    
    dynamic_scan_group.add_argument(
        "--clamav",
        action="store_true",
        help="Utilise clamAV for dynamic malware scanning",
    )
    
    # ! ============================================= STATIC MALWARE SCAN ====================================================

    # ~ STATIC MALWARE ANALYSIS
    static_scan_group = parser.add_mutually_exclusive_group()

    static_scan_group.add_argument(
        "--yara",
        action="store_true",
        help="Utilise YARA rules for static malware scanning"
    )

    static_scan_group.add_argument(
        "--md5",
        action="store_true",
        help="Utilise MD5 hash for static malware scanning"
    )

    static_scan_group.add_argument(
        "--sha1",
        action="store_true",
        help="Utilise SHA1 hash for static malware scanning"
    )

    static_scan_group.add_argument(
        "--sha256",
        action="store_true",
        help="Utilise SHA256 hash for static malware scanning"
    )

    # ! =================================================================================================

    args = parser.parse_args()

    # ! ============================================= CONFIG / SCHEDULE LOGIC ====================================================
    
    # ^ ADD CONFIGURATION
    if args.config is not None and args.delete is False:
        
        if args.time is not None or args.daily or args.monthly or args.hourly:
            
            print("REMOVE TIME RELATED FLAGS WHEN SAVING CONFIG")
            print("USE TIME RELATED FLAGS ONLY WITH SCHEDULE FLAG")
            print("EXAMPLE -> python runme.py --schedule example_config --time 14:30 --daily")
            sys.exit()
        
        # ~ FULL COMMAND
        full_command = " ".join(shlex.quote(arg) for arg in sys.argv)
        full_command = "python " + str(full_command)
        split_command = full_command.split(" ")

        split_command.pop()
        split_command.pop()

        full_command = " ".join(split_command)

        # ~ FILE PATH
        file_exists = os.path.exists("data.json")

        # ? FILE EXISTS, APPEND DATA TO FILE
        if file_exists:
            
            with open("data.json", "r") as json_file:
                json_data = json.load(json_file)
            
            config_name_list = []
            
            for temp in json_data["config"]:
                if temp["CONFIG"] == str(args.config):
                    print("CONFIG NAME ALREADY EXISTS, USE ANOTHER NAME")
                    sys.exit()
            
            json_data["config"].append({"CONFIG": str(args.config), "COMMAND": full_command})
            
            with open("data.json", "w") as json_file:
                json.dump(json_data, json_file, indent=4)

        # ? FILE DOES NOT EXIST, CREATE FILE AND ADD DATA
        else:

            json_data = {}
            json_data["config"] = []
            json_data["config"].append({"CONFIG": str(args.config), "COMMAND": full_command})

            with open("data.json", "w") as json_file:
                json.dump(json_data, json_file, indent=4)
    
    # ^ DELETE CONFIGURATION
    elif args.delete and args.config is not None:
        
        file_exists = os.path.exists("data.json")
        
        if file_exists:

            with open("data.json", "r") as json_file:
                json_data = json.load(json_file)
            
            # ~ CONFIG NOT FOUND
            flag = 0
            
            for temp in json_data["config"]:

                index = json_data["config"].index(temp)

                if temp["CONFIG"] == str(args.config):
                    
                    del json_data["config"][index]
                    flag = 1
            
            if flag == 0:
                
                print("CONFIG NAME DOES NOT EXIST")
                print("EXAMPLE -> python runme.py --static --sha256 --config example_config")
                sys.exit()
            
            with open("data.json", "w") as json_file:
                json.dump(json_data, json_file, indent=4)

    # ^ SCHEDULE CONFIGURATION
    elif (args.schedule is not None and args.time is not None) or args.hourly:
        
        if args.config is not None:
            print("REMOVE CONFIG FLAG WHEN SCHEDULING A TASK")
            print("USE CONFIG FLAG SEPARATELY WITH SCAN COMMAND")
            print("EXAMPLE -> python runme.py --static --sha256 --config example_config")
            sys.exit()

        if args.daily:
            frequency = "daily"

        elif args.monthly:
            frequency = "monthly"

        elif args.hourly:
            frequency = "hourly"
        
        else:
            print("PLEASE SPECIFY A FREQUENCY via args.daily, args.monthly, args.hourly flags")
            sys.exit()

        file_exists = os.path.exists("data.json")

        if file_exists:

            with open("data.json", "r") as json_file:
                json_data = json.load(json_file)
            
            # ~ CONFIG NOT FOUND
            flag = 0
            
            for temp in json_data["config"]:

                index = json_data["config"].index(temp)

                if temp["CONFIG"] == str(args.schedule):
                    
                    json_data["config"][index]["FREQUENCY"] = frequency
                    
                    if frequency != "hourly":
                        json_data["config"][index]["TIME"] = str(args.time)
                    
                    elif frequency == "hourly" and args.time is not None:
                        print("REMOVE TIME FLAG WHEN SCHEDULING HOURLY TASK")
                        print("EXAMPLE -> python runme.py --schedule example_config --hourly")
                        sys.exit()
                    
                    flag = 1
            
            # ~ CONFIG NOT FOUND
            if flag == 0:
                print("CONFIG NAME DOES NOT EXIST")
                print("CREATE A CONFIG TO MAP TIMING TO")
                print("EXAMPLE -> python runme.py --static --sha256 --config example_config")
                sys.exit()

            with open("data.json", "w") as json_file:
                json.dump(json_data, json_file, indent=4)

        else:

            print("CREATE A CONFIG TO MAP THIS SCHEDULE")
            print("EXAMPLE -> python runme.py --static --sha256 --config example_config")
            sys.exit()

    # ! ============================================= INDEX ====================================================
    
    elif args.config is None and args.index:
        
        if os.path.exists("filesystem.db"):
            os.remove("filesystem.db")
            
        if os.path.exists("filesystem.db-journal"):
            os.remove("filesystem.db-journal")

        create_table()
        
        run_identify(args.threads)

    # ! ============================================= STATIC SCAN ====================================================

    elif args.config is None and args.static:
        
        if args.yara:
            decision("YARA", args.type, args.processes)
            
        elif args.md5:
            decision("MD5", args.type, args.processes)
            
        elif args.sha1:
            decision("SHA1", args.type, args.processes)
            
        elif args.sha256:
            decision("SHA256", args.type, args.processes)
    
    elif args.config is None and args.dynamic:
        
        if args.virustotal:
            decision("VT", args.type, args.processes)
        
        elif args.clamav:
            decision("CLAMAV", args.type, args.processes)
    
    elif args.dashboard:
        print("DASHBOARD IS RUNNING ON PORT 8050")
        os.system("python dashboard.py")
        time.sleep(2)
        # result = subprocess.run(['python', 'dashboard.py'], capture_output=True, text=True)