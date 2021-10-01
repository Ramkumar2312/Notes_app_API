from flask import Flask,request
from flask import jsonify
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello world !"

@app.route('/add',methods=['POST'])
def add_data():
    data = request.get_json()
    note = data['note']
    connection = sqlite3.connect('notes.db')
    cursor = connection.cursor()
    insert_data = "INSERT INTO notes(note) VALUES(?)"
    cursor.execute(insert_data,(note,))
    connection.commit()
    connection.close()
    return f"Note : '{note}', added successfully"

@app.route('/display',methods=['GET'])
def display_data():
    connection = sqlite3.connect('notes.db')
    cursor = connection.cursor()
    select_all = "SELECT * FROM notes"
    cursor.execute(select_all)
    notes = cursor.fetchall()
    note_dict = {}
    for note in notes:
        note_dict[note[0]] = note
    connection.close()

    return jsonify(note_dict)

@app.route('/update',methods=['PUT'])
def update_data():
    data = request.get_json()
    _id = data['id']
    note = data['note']
    connection = sqlite3.connect('notes.db')
    cursor = connection.cursor()
    update_data_query = "UPDATE notes SET note = ? WHERE id = ?"
    cursor.execute(update_data_query,(note,_id))
    connection.commit()
    connection.close()

    return jsonify({"message":"note updated"})


@app.route('/delete',methods=['DELETE'])
def delete_data():
    data = request.get_json()
    _id = data['id']
    connection = sqlite3.connect('notes.db')
    cursor = connection.cursor()
    delete_note_query = "DELETE FROM notes WHERE id = ?"
    cursor.execute(delete_note_query,(_id,))
    connection.commit()
    connection.close()

    return jsonify({"message":"Note deleted"})






if __name__ == '__main__':
        app.run(port=5007,debug=True)