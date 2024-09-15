import os
from flask import Flask, render_template
from add_data import add_measurement
from data_table import get_measurements
from data_graph import get_last_measurement
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database setup
def init_db():
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
def add_measurement_route():
    return add_measurement()

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
@app.route('/get_last_measurement', methods=['GET'])
def get_last_measurement_route():
    return get_last_measurement()
@app.route('/get_measurements', methods=['GET'])
def get_measurements_route():
    return get_measurements()

@app.route('/delete_measurement/<int:measurement_id>', methods=['DELETE'])
def delete_measurement(measurement_id):
    try:
        conn = sqlite3.connect('user_data.db')
        c = conn.cursor()
        c.execute('DELETE FROM measurements WHERE id = ?', (measurement_id,))
        conn.commit()
        response = jsonify({'status': 'Measurement deleted successfully'})
        status_code = 200
    except Exception as e:
        response = jsonify({'status': 'Error deleting measurement', 'error': str(e)})
        status_code = 500
    finally:
        conn.close()
    return response, status_code

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
