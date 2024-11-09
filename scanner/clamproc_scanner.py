import clamd
import psutil

cd = clamd.ClamdUnixSocket()

def scan_process(process):

    try:
        # Get the process memory dump
        mem_dump = process.memory_maps()[0].mem_file.read_bytes()

        # Scan the memory dump with ClamAV
        result = cd.instream(mem_dump)

        if result['stream'][0] == 'OK':
            return False, result['stream'][1]
        else:
            return True, result['stream'][1]
    except Exception as e:
        return False, str(e)

def scan_running_processes():
    infected_processes = []
    for process in psutil.process_iter(['name', 'pid', 'memory_maps']):
        is_infected, result = scan_process(process)
        if is_infected:
            infected_processes.append((process.info['name'], process.info['pid'], result))
    return infected_processes

# infected_processes = scan_running_processes()
# if infected_processes:
#     print("Infected processes:")
#     for process_name, process_id, result in infected_processes:
#         print(f"  Process: {process_name} (PID: {process_id}), Result: {result}")
# else:
#     print("No infected processes found.")