import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Tharuni18@#",
    database="mental_health_system"
)

cursor = db.cursor()