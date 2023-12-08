
import json
import random

def generate_transportation_data():
    dict1 = {}
    boolean = [True, False]

    for route_id in range(100):
        

        # Randomly determine if it is a bike route or a light train route
        is_bike_route = random.choice(boolean)
        is_light_train_route = not is_bike_route  # Assuming a route can't be both
        
        starting_zipcode = 0
        ending_zipcode = 0
        # Generate starting and ending zipcodes
        if is_bike_route:
            starting_zipcode = random.randint(20101, 24658)
            ending_zipcode = starting_zipcode + random.randint(0,2)
        if is_light_train_route:
            starting_zipcode = random.randint(20101, 24658)
            ending_zipcode = starting_zipcode + random.randint(0,5)

        # Adding the generated data to the dictionary
        dict1[route_id] = [is_bike_route, is_light_train_route, starting_zipcode, ending_zipcode]

    return dict1

# Generate transportation data
transportation_data = generate_transportation_data()

# Writing the data to a JSON file
with open("transportation.json", "w") as f:
    json.dump(transportation_data, f, indent=4)