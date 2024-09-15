from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database setup
def init_db():
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
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (nickname, gender, birthdate) VALUES (?, ?, ?)',
              (data['nickname'], data['gender'], data['birthdate']))
    conn.commit()
    conn.close()
    return jsonify({'status': 'User added successfully'})

@app.route('/add_measurement', methods=['POST'])
def add_measurement():
    data = request.json
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO measurements (user_id, date, weight, height, neck, waist, hip)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (data['user_id'], datetime.now().strftime('%Y-%m-%d'), data['weight'], data['height'],
          data['neck'], data['waist'], data['hip']))
    conn.commit()
    conn.close()
    return jsonify({'status': 'Measurement added successfully'})

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
