import pymysql
import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

connection = pymysql.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME')
)


@app.route("/")
def index():
    return "Hello World"

@app.route('/stats/')
def get_stats():
    zipcode = request.args.get('zipcode')
    # Perform statistics calculation based on the provided zipcode
    # ...
    return f'Statistics for zipcode: {zipcode}'

@app.route("/api/crimes")
def get_crimes():
    zipcode = request.args.get('zipcode')
    crimeType = request.args.get('type')
    data = {}
    if crimeType: 
        # Count all the crimes of the specified crimeType by the zipcode
        query = f"SELECT crimeType, COUNT(*) AS count FROM Crimes WHERE zipcode = '{zipcode}' AND LOWER(crimeType) = LOWER('{crimeType}') GROUP BY crimeType"
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
        # Return the counts of each crime in a single JSON format
        if result:
            data = {'crimeType': result['crimeType'], 'count': result['count']}
        else:
            data = {'crimeType': crimeType, 'count': 0}
    else:
        with connection.cursor() as cursor:
            # SQL query
            sql = f"SELECT zipcode, crimeType, COUNT(*) as crimeCount FROM Crimes WHERE zipcode = '{zipcode}' GROUP BY zipcode, crimeType "
            cursor.execute(sql)
            results = cursor.fetchall()

            for row in results:
                zipcode, crime_type, count = row
                if zipcode not in data:
                    data[zipcode] = {}
                data[zipcode][crime_type] = count
        

    return jsonify(data)

@app.route('/api/data')
def get_data():
    data = {'name': 'John Doe', 'age': 25}
    return data

if __name__ == '__main__':
    app.run(debug=True)

    

@app.route('/api/data')
def get_data():
    data = {'name': 'John Doe', 'age': 25}
    return data

if __name__ == '__main__':
    app.run(debug=True)
