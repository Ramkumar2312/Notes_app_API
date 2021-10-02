import sqlite3

connection = sqlite3.connect('notes.db')
cursor = connection.cursor()

create_table_notes = "CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, " \
                     "note TEXT ," \
                     "sqltime TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)"

cursor.execute(create_table_notes)

create_table_users = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, " \
                     "username TEXT," \
                     "password TEXT)"

cursor.execute(create_table_users)

connection.commit()
connection.close()