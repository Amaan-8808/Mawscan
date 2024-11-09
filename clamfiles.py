import clamd
import os
from six import BytesIO

cd = clamd.ClamdUnixSocket()

def scan_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            file_data = file.read()
            result = cd.instream(BytesIO(file_data))
        if result['stream'][0] == 'OK':
            return False
        else:
            return True
    except Exception as e:
        return False, str(e)

def scan_directory(dir_path):
    infected_files = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)
            is_infected = scan_file(file_path)
            print("File Path: ", file_path)
            print("Is Infected: ", is_infected)
            print("-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-")
            if is_infected:
                infected_files.append(file_path)
    return infected_files

# file_path = 'config.yml'
# is_infected = scan_file(file_path)
# print(f'File {file_path} is infected: {is_infected}')

# TODO - ADD FLAG FOR PRINT ALL OR PRINT INFECTED
# TODO - ADD INFECTED FILES TO MALWARE REPORT
# TODO - INTEGRATE THIS WHOLE CODE WITH RUNME.PY

dir_path = '/home/aditya/Documents/GitHub/mawscan'
print("-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-")
infected_files = scan_directory(dir_path)
if infected_files:
    print(f'Infected files in {dir_path}:')
    for file_path, result in infected_files:
        print(f'  {file_path}: {result}')
else:
    print(f'No infected files found in {dir_path}')