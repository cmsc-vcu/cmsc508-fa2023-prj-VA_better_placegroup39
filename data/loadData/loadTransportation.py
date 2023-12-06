import json

# Load the JSON data
with open('../generateData/transportation.json', 'r') as file:
    data = json.load(file)

# Generate SQL INSERT statements
insert_statements = ""
for route_id, values in data.items():
    is_bike_route, is_light_train_route, starting_zipcode, ending_zipcode = values
    insert_statements += (f"INSERT INTO Transportation (routeId, isBikeRoute, isLightTrainRoute, startingZipcode, endingZipcode) VALUES ('{route_id}', {is_bike_route}, {is_light_train_route}, {starting_zipcode}, {ending_zipcode});\n")

with open("Transportation_ddl.sql", "w") as f:
    f.write(insert_statements)
