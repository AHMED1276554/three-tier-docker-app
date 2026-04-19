from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import time

app = Flask(__name__)
CORS(app)

# Wait for database to boot up
time.sleep(10)

def get_db_connection():
    return psycopg2.connect(
        host="database",
        database="appdb",
        user="postgres",
        password="postgres"
    )

# Create tables if they don't exist
conn = get_db_connection()
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT);')
cur.execute('CREATE TABLE IF NOT EXISTS notes (id SERIAL PRIMARY KEY, user_id INTEGER, content TEXT);')
conn.commit()
cur.close()
conn.close()

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (data['username'], data['password']))
        conn.commit()
        return jsonify({"message": "User created!"}), 201
    except:
        return jsonify({"message": "User already exists!"}), 400
    finally:
        cur.close()
        conn.close()

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id FROM users WHERE username = %s AND password = %s', (data['username'], data['password']))
    user = cur.fetchone()
    cur.close()
    conn.close()
    if user:
        return jsonify({"user_id": user[0]}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@app.route("/notes/<int:user_id>", methods=["GET", "POST"])
def manage_notes(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == "POST":
        content = request.json['content']
        cur.execute('INSERT INTO notes (user_id, content) VALUES (%s, %s)', (user_id, content))
        conn.commit()
    
    cur.execute('SELECT id, content FROM notes WHERE user_id = %s', (user_id,))
    notes = [{"id": row[0], "content": row[1]} for row in cur.fetchall()]
    cur.close()
    conn.close()
    return jsonify(notes)

@app.route("/notes/delete/<int:note_id>", methods=["DELETE"])
def delete_note(note_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM notes WHERE id = %s', (note_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Deleted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
