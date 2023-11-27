import json
dict1 = {}
import random
boolean = [True, False]
for i in range(100):
    bikeRoutes = random.randint(0, 50)
    hasLightTrains = boolean[random.randint(0,1)]
    zipcode = random.randint(20101 ,24658)
    dict1[zipcode] = [bikeRoutes, hasLightTrains]

outfile = open("transportation.json", "w")
json.dump(dict1, outfile, indent = 6)