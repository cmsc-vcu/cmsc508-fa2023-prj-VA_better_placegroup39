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



@app.route("/api/houses/")
def get_houses_by_zipcode():
    data = {}
    zipcode = request.args.get('zipcode')
    rent = request.args.get('rent')
    min_rent_price = request.args.get('minRentPrice')
    max_rent_price = request.args.get('maxRentPrice')
    sale = request.args.get('sale')
    min_sale_price = request.args.get('minSalePrice')
    max_sale_price = request.args.get('maxSalePrice')

    # Use a WHERE clause in the SQL query based on the provided parameters
    where_conditions = []

    if zipcode:
        where_conditions.append(f"zipcode = '{zipcode}'")
    if rent is not None:
        where_conditions.append(f"ForRent = {rent}")
    if min_rent_price:
        where_conditions.append(f"rentPrice >= {min_rent_price}")
    if max_rent_price:
        where_conditions.append(f"rentPrice <= {max_rent_price}")
    if sale is not None:
        where_conditions.append(f"ForSale = {sale}")
    if min_sale_price:
        where_conditions.append(f"salePrice >= {min_sale_price}")
    if max_sale_price:
        where_conditions.append(f"salePrice <= {max_sale_price}")

    where_clause = " AND ".join(where_conditions)

    # Debugging information
    print(f"Generated SQL query: SELECT * FROM Houses WHERE {where_clause}")

    with connection.cursor() as cursor:
        # SQL query to retrieve houses based on the provided parameters
        sql = f"SELECT * FROM Houses"
        if where_clause:
            sql += f" WHERE {where_clause}"

        # Debugging information
        print(f"Executing SQL query: {sql}")

        cursor.execute(sql)
        houses = cursor.fetchall()

        for house in houses:
            house_id, owner_person_id, zipcode, for_sale, sale_price, for_rent, rent_price = house
            data[house_id] = {
                'ownerPersonId': owner_person_id,
                'zipcode': zipcode,
                'forSale': for_sale,
                'salePrice': float(sale_price) if sale_price is not None else None,
                'forRent': for_rent,
                'rentPrice': float(rent_price) if rent_price is not None else None
            }

    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)


# http://127.0.0.1:5000/api/houses/?zipcode=YOUR_ZIPCODE&rent=True&maxRentPrice=100000   
# If you want to make an API call to retrieve houses for a specific zipcode where forRent is true and rentPrice is less than 100000
#http://127.0.0.1:5000/api/houses/?zipcode=24059&rent=True&maxRentPrice=10000 
#http://127.0.0.1:5000/api/houses/?zipcode=22770&sale=True&maxSalePrice=10000000


@app.route("/api/schools", methods=["GET"])
def get_schools():
    data = {}
    zipcode = request.args.get('zipcode')
    school_name = request.args.get('schoolName')
    min_teachers = request.args.get('minNumberOfTeachers')
    max_teachers = request.args.get('maxNumberOfTeachers')
    min_diversity = request.args.get('minDiversity')
    max_diversity = request.args.get('maxDiversity')
    quality = request.args.get('quality')

    # Use a WHERE clause in the SQL query based on the provided parameters
    where_conditions = []

    if zipcode:
        where_conditions.append(f"zipcode = {zipcode}")
    if school_name:
        where_conditions.append(f"schoolName = '{school_name}'")
    if min_teachers:
        where_conditions.append(f"numberOfTeachers >= {min_teachers}")
    if max_teachers:
        where_conditions.append(f"numberOfTeachers <= {max_teachers}")
    if min_diversity:
        where_conditions.append(f"diversityPercentage >= {min_diversity}")
    if max_diversity:
        where_conditions.append(f"diversityPercentage <= {max_diversity}")
    if quality:
        where_conditions.append(f"quality = '{quality}'")

    where_clause = " AND ".join(where_conditions)

    # Debugging information
    print(f"Generated SQL query: SELECT * FROM Schools WHERE {where_clause}")

    with connection.cursor() as cursor:
        # SQL query to retrieve schools based on the provided parameters
        sql = f"SELECT * FROM Schools"
        if where_clause:
            sql += f" WHERE {where_clause}"

        # Debugging information
        print(f"Executing SQL query: {sql}")

        cursor.execute(sql)
        schools = cursor.fetchall()

        for school in schools:
            school_id, school_name, number_of_teachers, diversity_percentage, school_quality, school_zipcode = school
            data[school_id] = {
                'schoolName': school_name,
                'numberOfTeachers': number_of_teachers,
                'diversityPercentage': diversity_percentage,
                'quality': school_quality,
                'zipcode': school_zipcode
            }

    return jsonify(data)




if __name__ == "__main__":
    app.run(debug=True)



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
    
