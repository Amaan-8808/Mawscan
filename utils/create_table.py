import sqlite3

def create_table():
    
    sqliteConnection = sqlite3.connect('filesystem.db')
    cursor = sqliteConnection.cursor()
    sql_command = "CREATE TABLE filesystem (id INTEGER PRIMARY KEY AUTOINCREMENT, filetype CHAR(25) NOT NULL, category VARCHAR(255), mime VARCHAR(255), fullpath VARCHAR(255) NOT NULL);"
    cursor.execute(sql_command)
    sqliteConnection.commit()
    sqliteConnection.close()
