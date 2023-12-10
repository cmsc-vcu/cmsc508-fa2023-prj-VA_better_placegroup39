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
def get_houses():
    
    data = {}
    zipcode = request.args.get('zipcode')
    rent = request.args.get('rent')
    sale = request.args.get('sale')
    minPrice = request.args.get('minPrice')
    maxPrice = request.args.get('maxPrice')

    # Use a WHERE clause in the SQL query based on the provided parameters
    where_conditions = []

    if zipcode:
        where_conditions.append(f"zipcode = '{zipcode}'")
    if rent is not None:
        where_conditions.append(f"ForRent = 1")
        if minPrice:
            where_conditions.append(f"rentPrice >= {minPrice}")
        if maxPrice:
            where_conditions.append(f"rentPrice <= {maxPrice}")
    if sale is not None:
        where_conditions.append(f"ForSale = 1")
        if minPrice:
            where_conditions.append(f"salePrice >= {minPrice}")
        if maxPrice:
            where_conditions.append(f"salePrice <= {maxPrice}")

    where_clause = " AND ".join(where_conditions)

    

    sql = f"SELECT * FROM Houses"
    if where_clause:
        sql += f" WHERE {where_clause}"
    with connection.cursor() as cursor:
        # SQL query to retrieve houses based on the provided parameters

        cursor.execute(sql)
        houses = cursor.fetchall()
        print(houses)
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

# http://127.0.0.1:5000/api/schools?zipcode=24331&quality=F&maxNumberOfTeachers=200
# http://127.0.0.1:5000/api/schools?zipcode=24331&quality=F&minNumberOfTeachers=100


@app.route("/api/jobs", methods=["GET"])
def get_open_jobs():
    zipcode = request.args.get('zipcode')
    count = request.args.get('count')
    actively_hiring = request.args.get('actively_hiring')

    query = "SELECT * FROM OpenJobs"
    if count:
        query = "SELECT COUNT(*) FROM OpenJobs"
    if zipcode:
        query += f" WHERE zipcode = '{zipcode}'"
    if actively_hiring:
        query += f" AND actively_hiring = 1"

    with connection.cursor() as cursor:
        cursor.execute(query)
        if actively_hiring:
            result = cursor.fetchone()[0]
            return jsonify({"total_actively_hiring_jobs" : result})
        if count:
            result = cursor.fetchone()[0]
            return jsonify({"total_open_jobs": result})
        else:
            result = cursor.fetchall()
            return jsonify(result)



@app.route("/api/transportation", methods=["GET"])
def get_transportation():
    try:
        # Retrieve parameters from the request
        zipcode = request.args.get('zipcode')
        is_bike_route = request.args.get('isBikeRoute')
        is_light_train_route = request.args.get('isLightTrainRoute')


        # Use a WHERE clause in the SQL query based on the provided parameters
        where_conditions = []
        where_params = []

        if zipcode:
            # Check if there is any route where the provided zipcode falls between startingZipcode and endingZipcode
            where_conditions.append("(startingZipcode <= %s AND endingZipcode >= %s)")
            where_params.extend([zipcode, zipcode])

        if is_bike_route:
            where_conditions.append("isBikeRoute = %s")
            where_params.append(is_bike_route)

        if is_light_train_route:
            where_conditions.append("isLightTrainRoute = %s")
            where_params.append(is_light_train_route)

        where_clause = " AND ".join(where_conditions)
        print(f"Generated SQL query: SELECT * FROM Transportation WHERE {where_clause}")


        with connection.cursor() as cursor:
            sql = "SELECT * FROM Transportation"
            if where_clause:
                sql += f" WHERE {where_clause}"

            print(f"Executing SQL query: {sql}")

            # Use parameterized query for safety
            cursor.execute(sql, where_params)
            transportation = cursor.fetchall()
            print(transportation)


            data = {}
            for route in transportation:
                route_id, is_bike_route, is_light_train_route, starting_zipcode, ending_zipcode = route
                data[route_id] = {
                    'isBikeRoute': bool(is_bike_route),
                    'isLightTrainRoute': bool(is_light_train_route),
                    'startingZipcode': starting_zipcode,
                    'endingZipcode': ending_zipcode
                }
           
        return jsonify(data)


    except Exception as e:
        return jsonify({'error': str(e)}), 500


# http://127.0.0.1:5000/api/transportation?zipcode=21983&isBikeRoute=0
 
   


if __name__ == "__main__":
    app.run(debug=True)