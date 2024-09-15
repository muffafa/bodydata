from flask import request, jsonify
import sqlite3
from datetime import datetime

def add_measurement():
    data = request.json
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    user_id = data['user_id']
    gender = data['gender']
    age = data['age']
    c.execute('''
        INSERT INTO users (id, gender, birthdate)
        VALUES (?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET gender=excluded.gender, birthdate=excluded.birthdate
    ''', (user_id, gender, str(datetime.now().year - int(age)) + '-01-01'))
    c.execute('''
        INSERT INTO measurements (user_id, date, weight, height, neck, waist, hip)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, datetime.now().strftime('%Y-%m-%d'), data['weight'], data['height'],
          data['neck'], data['waist'], data['hip']))
    conn.commit()
    conn.close()
    print("Measurement added successfully.")
    return jsonify({'status': 'Measurement added successfully'})
