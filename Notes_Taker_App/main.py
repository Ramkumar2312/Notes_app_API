from flask import Flask,request
from flask import jsonify
import sqlite3
# from flask_jwt import JWT,jwt_required

from flask_jwt_extended import JWTManager,jwt_required,get_jwt_identity,create_access_token
from security import authenticate,identity

app = Flask(__name__)
app.secret_key = "1234qwerty"

app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)
# jwt = JWT(app,authenticate,identity)

@app.route('/')
def home():
    return "Hello world !"

@app.route('/add',methods=['POST'])
@jwt_required()
def add_data():
    data = request.get_json()
    note = data['note']
    current_user = get_jwt_identity()
    user_id = current_user
    connection = sqlite3.connect('notes.db')
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    try :
        insert_data = "INSERT INTO notes(note,user_id) VALUES(?,?)"
        cursor.execute(insert_data,(note,user_id))
    except Exception as e:
        cursor.close()
        connection.close()
        return jsonify({'message':e.args})
    connection.commit()
    cursor.close()
    connection.close()
    return f"Note : '{note}', added successfully"



@app.route('/display',methods=['GET'])
@jwt_required()
def display_data():
    connection = sqlite3.connect('notes.db')
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    current_user = get_jwt_identity()
    print(current_user)
    try :
        select_all = "SELECT * FROM notes WHERE user_id=?"
        cursor.execute(select_all,(current_user,))
    except Exception as e:
        cursor.close()
        connection.close()
        return jsonify({'message': e.args})
    notes = cursor.fetchall()
    note_dict = {}
    for note in notes:
        note_dict[note[0]] = note
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify(note_dict)


@app.route('/update',methods=['PUT'])
@jwt_required()
def update_data():
    data = request.get_json()
    _id = data['id']
    note = data['note']

    connection = sqlite3.connect('notes.db')
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    try :
        update_data_query = "UPDATE notes SET note = ? WHERE id = ?"
        cursor.execute(update_data_query,(note,_id))
    except Exception as e:
        cursor.close()
        connection.close()
        return jsonify({'message': e.args})
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message":"note updated"})


@app.route('/delete',methods=['DELETE'])
@jwt_required()
def delete_data():
    data = request.get_json()
    current_user = get_jwt_identity()
    _id = data['id']
    user_id = current_user
    connection = sqlite3.connect('notes.db')
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    try :
        delete_note_query = "DELETE FROM notes WHERE id = ? and user_id = ?"
        cursor.execute(delete_note_query,(_id,user_id))
    except Exception as e:
        cursor.close()
        connection.close()
        return jsonify({'message': e.args})
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message":"Note deleted"})


@app.route('/get_users',methods=['GET'])
def get_users():
    # data = request.get_json()
    connection = sqlite3.connect('notes.db')
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    try :
        select_all_users = "SELECT * FROM users"
        cursor.execute(select_all_users)
    except Exception as e:
        cursor.close()
        connection.close()
        return jsonify({'message': e.args})
    users = cursor.fetchall()
    user_dict ={}
    for user in users:
        user_dict[user[0]] = user[1]
    cursor.close()
    connection.close()
    return jsonify(user_dict)


@app.route('/user_register',methods=['POST'])
def user_register():
    data = request.get_json()
    connection = sqlite3.connect('notes.db')
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    try :
        user_insert = "INSERT INTO users (username,password) VALUES (? ,?)"
        cursor.execute(user_insert, (data['username'], data['password']))
    except Exception as e:
        cursor.close()
        connection.close()
        return jsonify({'message': e.args})
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message": "user added successfully "})

@app.route('/delete_user',methods=['DELETE'])
def delete_user():
    data = request.get_json()
    _id = data['id']
    connection = sqlite3.connect('notes.db')
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    try :
        delete_user_query = "DELETE FROM users WHERE id = ?"
        cursor.execute(delete_user_query,(_id,))
    except Exception as e:
        cursor.close()
        connection.close()
        return jsonify({'message': e.args})
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"message":"User deleted"})

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    connection = sqlite3.connect('notes.db')
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    try :
        select_user = "SELECT * FROM users WHERE username=? and password=?"
        user = cursor.execute(select_user,(data['username'], data['password'])).fetchone()
        user_id = user[0]
    except Exception as e:
        cursor.close()
        connection.close()
        return jsonify({'message': e.args})

    if user is not None:

        access_token = create_access_token(identity=user_id)
        return jsonify(access_token=access_token)

if __name__ == '__main__':
        app.run(port=5007,debug=True)