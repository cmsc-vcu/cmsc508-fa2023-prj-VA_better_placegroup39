import names
import json
import math
import random
import houses
import crimes


dict1 = {}
crimeDict = {}
housesDict = {}

def main():
    crimeId = 0
    housesId = 0
    ethnicities = ["Caucasian", "Afican-American", "Latino", "Asian"]
    for personId in range(1000):
        name = names.get_full_name()
        ethnicity = ethnicities[random.randint(0,3)]
        zipcode = random.randint(20101 ,24658)
        age = random.randint(1,85)
        salary = 0
        if age > 17:
            salary = random.randint(0, 700000)
        dict1[personId] = [name, salary, age, ethnicity, zipcode]
        if personId % 10 == 0:
            randomNum = random.randint(1,10)
            crimeDict[crimeId] = crimes.generateCrimeData(math.floor(personId/randomNum))
            crimeId += 1
        if personId % 10 == 0:
            randomNum = random.randint(1,10)
            housesDict[housesId] = houses.generateHouseData(math.floor(personId/randomNum))
            housesId += 1


    outfile = open("population.json", "w")
    json.dump(dict1, outfile, indent = 6)

    crimeOutFile = open("crimes.json", "w")
    json.dump(crimeDict, crimeOutFile, indent = 6)

    outfile = open("houses.json", "w")
    json.dump(housesDict, outfile, indent = 6)

if __name__ == "__main__":
    main()
    print("Done")

