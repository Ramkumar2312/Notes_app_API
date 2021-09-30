import sqlite3

connection = sqlite3.connect('notes.db')
cursor = connection.cursor()

create_table_notes = "CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, note TEXT)"

cursor.execute(create_table_notes)

connection.commit()
connection.close()