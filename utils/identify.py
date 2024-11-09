import concurrent.futures
import filetype
import os
import sqlite3
import time
import mimetypes

import yaml

from utils.mime_backend import mime_backend
mimetypes.init()

def identify(filename):
    
    sqliteConnection = sqlite3.connect('filesystem.db')
    cursor = sqliteConnection.cursor()
    
    try:
        try:
            kind = mimetypes.guess(filename)[0]
        except:
            kind = mime_backend(filename)
            
        if kind is None:
            kind = mime_backend(filename)
            category = str(kind).split("/")[0]
            file_ext = str(kind).split("/")[1]
            sql_command = "INSERT INTO filesystem (filetype, fullpath) VALUES (?,?,?,?)"
            file_ext = filename.split(".")[-1]
            data = (file_ext, category, file_mime, filename)
            # print('----------------')
            # print("File extension: ", file_ext)
            # print("File name: %s" % file)
        else:
            sql_command = "INSERT INTO filesystem (filetype, category, mime, fullpath) VALUES (?,?,?,?)"
            file_mime = kind
            category = str(kind).split("/")[0]
            file_ext = str(kind).split("/")[1]
            data = (file_ext, category, file_mime, filename)
            # print('----------------')
            # print('File extension: %s' % kind.extension)
            # print('File MIME type: %s' % kind.mime)
            # print('File name: %s' % file)

    except Exception as e:
        sql_command = "INSERT INTO filesystem (filetype, fullpath) VALUES (?,?)"
        file_ext = filename.split(".")[-1]
        data = (file_ext, filename)
        # print(e)
        # print("File extension: ", file.split(".")[-1])
        # print("File name: %s" % file)
    
    cursor.execute(sql_command, data)
    sqliteConnection.commit()
    cursor.close()

def checkme(EXCLUDE, root):
    for check in EXCLUDE:
        if check in root:
            return True
    
    return False

def run_identify(threads=10):
    
    with open("config.yml") as f:
        config = yaml.safe_load(f)

    HOMES = config['include_dirs']
    EXCLUDE = config['exclude_dirs']
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        
        for HOME in HOMES:
        
            for root, dirs, files in os.walk(HOME):
                
                if len(EXCLUDE) > 0:
                    status = checkme(EXCLUDE, root)
                    
                    if status == True:
                        continue

                for file in files:
                    file_path = os.path.join(root, file)
                    if len(file.split(".")) > 1:
                        executor.submit(identify, file_path)
