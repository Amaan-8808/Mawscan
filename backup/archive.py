# from identify import run_identify
# from create_table import create_table
# from testyara import logic
import sqlite3
import os
import logging
import yara
from concurrent.futures import ProcessPoolExecutor
import time
import sys
import concurrent.futures
import filetype
from dotenv import dotenv_values

def identify(file):

    try:
        kind = filetype.guess(file)
        if kind is None:
            file_ext = file.split(".")[-1]
            # print('----------------')
            # print("File extension: ", file_ext)
            # print("File name: %s" % file)
        else:
            file_ext = kind.extension
            # print('----------------')
            # print('File extension: %s' % kind.extension)
            # print('File MIME type: %s' % kind.mime)
            # print('File name: %s' % file)

    except Exception as e:
        file_ext = file.split(".")[-1]
        # print(e)
        # print("File extension: ", file.split(".")[-1])
        # print("File name: %s" % file)
    
    # Insert into the database
    sqliteConnection = sqlite3.connect('filesystem.db')
    cursor = sqliteConnection.cursor()
    data = (file_ext, file)
    sql_command = "INSERT INTO filesystem (filetype, fullpath) VALUES (?,?)"
    cursor.execute(sql_command, data)
    sqliteConnection.commit()
    cursor.close()

def run_identify():
    config = dotenv_values(".env")
    HOME = config['HOME']
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        for root, dirs, files in os.walk(HOME):
            for file in files:
                file_path = os.path.join(root, file)
                if len(file.split(".")) > 1:
                    executor.submit(identify, file_path)

def create_table():
    
    sqliteConnection = sqlite3.connect('filesystem.db')
    cursor = sqliteConnection.cursor()
    sql_command = "CREATE TABLE filesystem (id INTEGER PRIMARY KEY AUTOINCREMENT, filetype CHAR(25) NOT NULL, fullpath VARCHAR(255) NOT NULL);"
    cursor.execute(sql_command)
    sqliteConnection.commit()
    sqliteConnection.close()

def scanner(root, row, file, logger1, logger2):

    rule = yara.compile(os.path.join(root, file))    
    logger1.info("Scanning File - %s",str(row))
    
    try:
        matches = rule.match(row)
        if matches and (".yara" not in row or ".yar" not in row):
            print("==>","\t",matches," <==> ",row, " <==> ",file)
    except Exception as e:
        logger2.error(e)

def logic():

    start_time = time.time()

    logger1 = logging.getLogger('logger1')
    logger1.setLevel(logging.INFO)
    file_handler1 = logging.FileHandler(os.path.join('logs','app.log'), mode='w')
    logger1.addHandler(file_handler1)

    logger2 = logging.getLogger('logger2')
    logger2.setLevel(logging.ERROR)
    file_handler2 = logging.FileHandler(os.path.join('logs','error.log'), mode='w')
    logger2.addHandler(file_handler2)

    conn = sqlite3.connect('filesystem.db')
    try:
        cursor = conn.execute("SELECT fullpath FROM filesystem WHERE filetype==\"exe\"")
    except sqlite3.OperationalError as e:
        print('\n#=#=#=#=#=#=#=#=#=#=#=#')
        logger2.error("The CREATE TABLE operation failed")
        logger2.error("Delete generated files (logs and db)")
        logger2.error("Retry running the files")
        logger2.error("If this consistently fails then manually run `create_table.py`")
        print("AN ERROR OCCURRED - PLEASE CHECK `error.log` TO DEBUG THE ERROR")
        print('#=#=#=#=#=#=#=#=#=#=#=#')
        sys.exit()

    rows = cursor.fetchall()
    
    config = dotenv_values(".env")
    RULES = config['RULES']

    for root, dirs, files in os.walk(RULES):

        for file in files:
            
            if ".yara" in file or ".yar" in file:
                with ProcessPoolExecutor(max_workers=10) as executor:
                    futures = [executor.submit(scanner, root, row[0], file, logger1, logger2) for row in rows]

                    for future in futures:
                        result = future.result()

                
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':

    flag = 1

    if os.path.exists('filesystem.db'):
        flag = 0

    if flag == 1:
        create_table()

        print('\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#')
        print('''
  _____ _   _ _____  ________   _______ _   _  _____     ______ _____ _      ______  _____ 
|_   _| \ | |  __ \|  ____\ \ / |_   _| \ | |/ ____|   |  ____|_   _| |    |  ____|/ ____|
  | | |  \| | |  | | |__   \ V /  | | |  \| | |  __    | |__    | | | |    | |__  | (___  
  | | | . ` | |  | |  __|   > <   | | | . ` | | |_ |   |  __|   | | | |    |  __|  \___ \ 
 _| |_| |\  | |__| | |____ / . \ _| |_| |\  | |__| |   | |     _| |_| |____| |____ ____) |
|_____|_| \_|_____/|______/_/ \_|_____|_| \_|\_____|   |_|    |_____|______|______|_____/ 

        ''')
        print('#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#\n')

        run_identify()
    
    print('\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#')
    print('''
   _____  _____          _   _ _   _ _____ _   _  _____ 
  / ____|/ ____|   /\   | \ | | \ | |_   _| \ | |/ ____|
 | (___ | |       /  \  |  \| |  \| | | | |  \| | |  __ 
  \___ \| |      / /\ \ | . ` | . ` | | | | . ` | | |_ |
  ____) | |____ / ____ \| |\  | |\  |_| |_| |\  | |__| |
 |_____/ \_____/_/    \_|_| \_|_| \_|_____|_| \_|\_____|

''')
    print('#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#\n')
    logic()