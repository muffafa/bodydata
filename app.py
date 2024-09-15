import os
from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database setup
def init_db():
    if os.path.exists('user_data.db'):
        os.remove('user_data.db')
        print("Existing database removed.")
    print("Initializing database...")
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nickname TEXT,
            gender TEXT,
            birthdate TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS measurements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT,
            weight REAL,
            height REAL,
            neck REAL,
            waist REAL,
            hip REAL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    c.execute('''
        INSERT INTO users (nickname, gender, birthdate)
        VALUES ('standard_user', 'male', '2001-09-15')
    ''')
    conn.commit()
    print("Database initialized and default user added.")
    print("Database initialized.")
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_measurement', methods=['POST'])
def add_measurement():
    data = request.json
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('SELECT id FROM users WHERE nickname = ?', ('standard_user',))
    user_id = c.fetchone()[0]
    if user_id is not None:
        c.execute('''
            INSERT INTO measurements (user_id, date, weight, height, neck, waist)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, datetime.now().strftime('%Y-%m-%d'), data['weight'], data['height'],
              data['neck'], data['waist']))
    else:
        return jsonify({'status': 'Error: User not found'}), 400
    conn.commit()
    conn.close()
    print("Measurement added successfully.")
    return jsonify({'status': 'Measurement added successfully'})

@app.route('/calculate_male_23', methods=['GET'])
def calculate_male_23():
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('''
        SELECT m.*
        FROM measurements m
        JOIN users u ON m.user_id = u.id
        WHERE u.gender = 'male' AND
              strftime('%Y', 'now') - strftime('%Y', u.birthdate) = 23
    ''')
    data = c.fetchall()
    conn.close()
    print(f"Fetched data: {data}")
    return jsonify(data)
@app.route('/get_measurements', methods=['GET'])
def get_measurements():
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM measurements')
    data = c.fetchall()
    conn.close()
    return jsonify(data)

app.run(debug=True, use_reloader=False)
