
import copy
from cryptography.fernet import Fernet
import os
import base64

def encrypt_file(file_path, key):
    with open(file_path, 'rb') as f:
        data = f.read()
    
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data)
    
    with open(file_path + '.encrypted', 'wb') as f:
        f.write(encrypted_data)

def decrypt_file(encrypted_file_path, key):
    with open(encrypted_file_path, 'rb') as f:
        encrypted_data = f.read()
    
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data)
    
    # Removing the '.encrypted' extension
    decrypted_file_path = encrypted_file_path[:-10]  
    
    with open(decrypted_file_path, 'wb') as f:
        f.write(decrypted_data)

def rename_and_encrypt(file_path, new_name):
    # Rename the file
    os.rename(file_path, new_name)
    # Encrypt the renamed file
    # encrypt_file(new_name, key)

def base64_encode_string(input_string):
    # Convert string to bytes
    input_bytes = input_string.encode('utf-8')
    
    # Encode bytes to Base64
    encoded_bytes = base64.b64encode(input_bytes)
    
    # Convert Base64 bytes to string
    encoded_string = encoded_bytes.decode('utf-8')
    
    return encoded_string

def quarantine_report(detected_files):
    for path, row in detected_files:
        filename_list = row.split("/")
        # change name
        last_element = filename_list[-1]
        last_element_ext = last_element.split(".")[-1]
        new_last_element = base64_encode_string(last_element)
        new_last_element = new_last_element + ".enc" + ".bin"

        # new location
        new_filename_list = copy.deepcopy(filename_list)
        new_filename_list.pop()
        new_filename_list.append(new_last_element)

        # join
        
        filename_loc = os.path.join(*filename_list)
        filename_loc = "/" + filename_loc
        new_filename_loc = os.path.join(*new_filename_list)
        new_filename_loc = "/" + new_filename_loc
        # key = "ODkpyRjVOa9B1WrVZbVIfe9iKFKSLZETPhn4plblRAY"
        # key = base64.b64encode(key.encode('utf-8'))
        rename_and_encrypt(filename_loc, new_filename_loc)