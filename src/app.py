import pymysql
import os
from flask import Flask, jsonify, request, render_template, session
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import bcrypt

app = Flask(__name__)


# Load environment variables from .env file
load_dotenv()

connection = pymysql.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME')
)

@app.route("/admin/login", methods=["GET", "POST"])
def admin_get():
    username = request.args.get('username')
    password = request.args.get('password')
    return jsonify({'authenticated': isAdmin(username, password)})

def isAdmin(username, password):
    # Check if the username exists in the Admins table
    query = f"SELECT * FROM Admins WHERE username = %s"
    with connection.cursor() as cursor:
        cursor.execute(query, (username,))
        result = cursor.fetchone()
    if result:
        print(result)
        # Verify if the passwords match
        hashed_password = result[2]
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            return True  # Redirect to an admin dashboard route
        else:
            # Passwords do not match
            return False
    else:
        # Username does not exist
        return False

@app.route("/")
def index():
    return "Hello World"

@app.route('/stats/')
def get_stats():
    zipcode = request.args.get('zipcode')
    # Perform statistics calculation based on the provided zipcode
    # ...
    return f'Statistics for zipcode: {zipcode}'

@app.route("/api/crimes", methods=["GET", "POST"])
def crimes():

    crimes = {
        "grand theft": 1,
        "larceny": 1,
        "arson": 4,
        "shoplifting": 0,
        "armed robbery": 5,
        "robbery": 2,
        "burglary": 3,
        "vandalism": 2,
        "assault": 4,
        "fraud": 1
    }
    name = request.args.get("name")
    crimeType = request.args.get("crimeType")
    
    date = request.args.get("date")
    zipcode = request.args.get('zipcode')
    username = request.form.get('username')
    password = request.form.get('password')
    if request.method == "POST":
        if isAdmin(username, password):
            severity = crimes.get(crimeType.lower(), 0)
            sql = f"INSERT INTO Crimes (fullName, crimeType, severity, date_of_crime, zipcode) VALUES ('{name}', '{crimeType}', '{severity}', '{date}', {zipcode});"
            with connection.cursor() as cursor:
                cursor.execute(sql)
                connection.commit()
                return jsonify({'code': 200, 'message': 'Successfully added crime'})
        else:
            return jsonify({'code': 401, 'message': 'Wrong Username and Password'})
        
    elif request.method == "GET":
        data = {}
        if crimeType: 
            severity = crimes.get(crimeType.lower(), 0)
            # Count all the crimes of the specified crimeType by the zipcode
            query = f"SELECT crimeType, COUNT(*) AS count FROM Crimes WHERE zipcode = '{zipcode}' AND LOWER(crimeType) = LOWER('{crimeType}') GROUP BY crimeType"
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchone()
            # Return the counts of each crime in a single JSON format
            if result:
                data = {'crimeType': crimeType, 'count': result[1]}
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

@app.route("/api/crimes/<id>", methods=["PUT", "DELETE"])
def changeCrimes(id):

    crimes = {
        "grand theft": 1,
        "larceny": 1,
        "arson": 4,
        "shoplifting": 0,
        "armed robbery": 5,
        "robbery": 2,
        "burglary": 3,
        "vandalism": 2,
        "assault": 4,
        "fraud": 1
    }

    name = request.args.get("name")
    crimeType = request.args.get("crimeType")
    severity = crimes[crimeType.lower()]
    date = request.args.get("date")
    username = request.form.get('username')
    password = request.form.get('password')
    if isAdmin(username, password):
        if request.method == "PUT":
            sql = f"UPDATE Crimes SET fullName = '{name}', crimeType = '{crimeType}', severity = '{severity}', date_of_crime = '{date}' WHERE crimeId = {id};"
            with connection.cursor() as cursor:
                cursor.execute(sql)
                connection.commit()
                return jsonify({'code': 200, 'message': 'Successfully updated crime'})
        if request.method == "DELETE":
            sql = f"DELETE FROM Crimes WHERE crimeId = {id};"
            with connection.cursor() as cursor:
                cursor.execute(sql)
                connection.commit()
                return jsonify({'code': 200, 'message': 'Successfully deleted crime'})
    else:
        
        return jsonify({'code': 401, 'message': 'Wrong Username and Password'})

        
@app.route("/api/houses/", methods=["GET", "POST"])
def houses():
    username = request.form.get('username')
    password = request.form.get('password')
    zipcode = request.args.get('zipcode')
    rent = request.args.get('rent')
    sale = request.args.get('sale')
    price = request.args.get('price')
    minPrice = request.args.get('minPrice')
    maxPrice = request.args.get('maxPrice')
    if request.method == "POST":
        if isAdmin(username, password):
            if rent:
                sql = f"INSERT INTO Houses (zipcode, ForSale, salePrice, ForRent, rentPrice) VALUES ({zipcode}, False, 0, True, {price});"
            elif sale:
                sql = f"INSERT INTO Houses (zipcode, ForSale, salePrice, ForRent, rentPrice) VALUES ({zipcode}, True, {price}, False, 0);"
            else:
                sql = f"INSERT INTO Houses (zipcode, ForSale, salePrice, ForRent, rentPrice) VALUES ({zipcode}, False, 0, False, 0);"
            with connection.cursor() as cursor:
                cursor.execute(sql)
                connection.commit()
                return jsonify({'code': 200, 'message': 'Successfully added crime'})
        else:
            return jsonify({'code': 401, 'message': 'Wrong Username and Password'})

    if request.method == "GET":
        data = {}
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
        query += f" WHERE zipcode = \"{zipcode}\""
    if actively_hiring:
        query += f" AND actively_hiring = 1"

    with connection.cursor() as cursor:
        cursor.execute(query)
        print(query)
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

        elif is_light_train_route:
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
 

@app.route("/api/population", methods=["GET"])
def get_population():
    data = {}
    zipcode = request.args.get('zipcode')
    min_age = request.args.get('minAge')
    max_age = request.args.get('maxAge')
    ethnicity = request.args.get('ethnicity')
    diversity = request.args.get('diversity')

    # Use a WHERE clause in the SQL query based on the provided parameters
    where_conditions = []

    if zipcode:
        where_conditions.append(f"zipcode = {zipcode}")
    if min_age:
        where_conditions.append(f"age >= {min_age}")
    if max_age:
        where_conditions.append(f"age <= {max_age}")
    if ethnicity:
        where_conditions.append(f"ethnicity = '{ethnicity}'")
    where_clause = " AND ".join(where_conditions)       
    # Debugging information

    with connection.cursor() as cursor:
        # SQL query to retrieve population data based on the provided parameters
        sql = "SELECT COUNT(*) FROM Peoples"
        if where_clause:
            sql += f" WHERE {where_clause}"

        # Debugging information
        print(f"Executing SQL query: {sql}")

        cursor.execute(sql)
        population_data = cursor.fetchone()[0]
    
    if diversity and ethnicity:
        with connection.cursor() as cursor:
            sql = f"SELECT COUNT(*) FROM Peoples WHERE zipcode = {zipcode}"
            cursor.execute(sql)
            total_population= cursor.fetchone()[0]
            diversityRate = round((population_data/total_population) * 100, 2)
            return jsonify({'diversityRate': f'{diversityRate}% {ethnicity}'})


    if population_data == {}:
        population_data = 0
    return jsonify({'total population': population_data})

# Example API calls:
# http://127.0.0.1:5000/api/population?zipcode=24331&minAge=20&maxAge=30&ethnicity=Asian
# http://127.0.0.1:5000/api/population?zipcode=24331&minAge=25
# http://127.0.0.1:5000/api/population?maxAge=40&ethnicity=AfricanAmerican



if __name__ == "__main__":
    app.run(debug=True)
