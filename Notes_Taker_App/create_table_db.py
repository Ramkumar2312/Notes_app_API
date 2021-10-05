import sqlite3

connection = sqlite3.connect('notes.db')
cursor = connection.cursor()

create_table_notes = "CREATE TABLE IF NOT EXISTS notes \
                    ( id INTEGER PRIMARY KEY, " \
                     "note TEXT ," \
                     "user_id INTEGER NOT NULL," \
                     "sqltime TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL," \
                     "FOREIGN KEY (user_id) REFERENCES users (id) ON UPDATE RESTRICT ON DELETE RESTRICT );"

cursor.execute(create_table_notes)

create_table_users = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, " \
                     "username TEXT," \
                     "password TEXT)"

cursor.execute(create_table_users)

connection.commit()
connection.close()

# ---------------------------------------
# connection = sqlite3.connect('notes.db')
# cursor = connection.cursor()
# user_insert = "INSERT INTO users (username,password) VALUES (? ,?)"
# # cursor.execute(user_insert, ("ronaldo", "rma123"))
# user_get = "SELECT * FROM users"
# u = cursor.execute(user_get).fetchall()
# print(u)
# notes_insert = "INSERT INTO notes (note,user_id) VALUES (? ,?)"
# # cursor.execute(notes_insert, ("first_note", "1"))
# notes_get = "SELECT * FROM notes"
# n = cursor.execute(user_get).fetchall()
# print(n)
# connection.commit()
# connection.close()