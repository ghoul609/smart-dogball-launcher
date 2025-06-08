#!/usr/bin/env python3

import mysql.connector

def fetch_data():
    # Connect to MySQL
    conn = mysql.connector.connect(
        host='localhost',
        user='loic',
        password='*****',
        database='app'
    )

    cursor = conn.cursor()

    # Fetch all records from table 'app'
    cursor.execute("SELECT * FROM app")

    # Print records
    records = cursor.fetchall()            
    # Clean up
    cursor.close()
    conn.close()
    
    response = []
    for record in records:
        temp = list(record)
        if temp[2] == 1:
            temp[2] = "successvol"
        else:
            temp[2] = "onsuccessvol"
        response.append(temp)
    
    return response

def insert_data(speed_value: int, launched: str):
    # Connect to MySQL
    conn = mysql.connector.connect(
        host='localhost',
        user='loic',
        password='*****',
        database='app'
    )

    cursor = conn.cursor()

    # Fetch all records from table 'app'
    cursor.execute("INSERT INTO app (timestamp, speed, launched) VALUES (NOW(), "+speed_value+","+launched+");")
    conn.commit()
    # Clean up
    cursor.close()
    conn.close()
