from db_config import db

if db.is_connected():
    print("Database Connected Successfully!")
else:
    print("Connection Failed!")