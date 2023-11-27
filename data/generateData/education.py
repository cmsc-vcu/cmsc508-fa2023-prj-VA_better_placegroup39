import json
import names
dict1 = {}
import random
Qualities = ["A", "B", "C", "D", "E", "F"]
typesOfSchools = ["Elementary School", "Middle School", "High School"]
for i in range(100):
    schoolName = f"{names.get_first_name()} {typesOfSchools[random.randint(0,2)]}"
    numberOfTeachers = random.randint(0, 500)
    diversity = f"{random.randint(0,100)}%"
    quality = Qualities[random.randint(0,5)]
    zipcode = random.randint(20101 ,24658)
    schoolID = f"School_{i}"
    dict1[schoolID] = [schoolName, numberOfTeachers, diversity, quality, zipcode]

outfile = open("education.json", "w")
json.dump(dict1, outfile, indent = 6)