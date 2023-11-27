import json
dict1 = {}
import random
for i in range(100):
    populationNumber = random.randint(0, 200000)
    diversity = f"{random.randint(0, 100)}%"
    zipcode = random.randint(20101 ,24658)
    youthPercent = f"{random.randint(0,100)}%"
    dict1[zipcode] = [diversity, populationNumber, youthPercent]

outfile = open("population.json", "w")
json.dump(dict1, outfile, indent = 6)