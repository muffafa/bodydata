import sqlite3
from flask import jsonify

def get_last_measurement():
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('''
        SELECT weight, height, neck, waist, hip
        FROM measurements
        ORDER BY id DESC
        LIMIT 1
    ''')
    last_measurement = c.fetchone()
    conn.close()
    return jsonify(last_measurement)
