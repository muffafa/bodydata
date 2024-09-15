import sqlite3
from flask import jsonify

def get_measurements():
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('''
        SELECT m.*, u.gender, 
               (strftime('%Y', 'now') - strftime('%Y', u.birthdate)) AS age
        FROM measurements m
        JOIN users u ON m.user_id = u.id
    ''')
    data = c.fetchall()
    conn.close()

    # Calculate body fat percentage
    result = []
    for row in data:
        user_id, date, weight, height, neck, waist, hip, gender, age = row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]
        bmi = weight / ((height / 100) ** 2)
        if gender == 'male':
            body_fat_percentage = (1.20 * bmi) + (0.23 * age) - 16.2
        elif gender == 'female':
            body_fat_percentage = (1.20 * bmi) + (0.23 * age) - 5.4
        else:
            body_fat_percentage = None  # Handle cases where gender is not specified
        result.append(row + (body_fat_percentage,))

    return jsonify(result)
