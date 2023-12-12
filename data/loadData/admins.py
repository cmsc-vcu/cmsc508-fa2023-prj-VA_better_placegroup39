import bcrypt
import json
import os
from dotenv import load_dotenv
import pymysql

# Load SQL config from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '../../src/.env')
load_dotenv(dotenv_path)

data = {}

# Generate random usernames
usernames = ["dawit", "donna", "aislin"]

# Create plain string password
password = "password123"

# Hash the password
hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Connect to SQL
db = pymysql.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

# Create a cursor
cursor = db.cursor()

# Insert usernames, email, and password into Admins table
for username in usernames:
    sql = "INSERT INTO Admins (username, password) VALUES (%s, %s)"
    values = (username, hashed_password)
    cursor.execute(sql, values)

# Commit the changes
db.commit()

# Close the cursor and connection
cursor.close()
db.close()
