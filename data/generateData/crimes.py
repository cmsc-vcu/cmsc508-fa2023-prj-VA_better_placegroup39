import random
# 0 to 5
crimes = [["Grand Theft", 1], ["Larceny", 1], ["Arson", 4], ["Shoplifting", 0], ["Armed Robbery", 5], ["Robbery", 2]]
def generateCrimeData(fullName):
    crime = crimes[random.randint(0,5)]
    typeOfCrime = crime[0]
    severity = crime[1]
    zipcode = random.randint(20101 ,24658)
    return [fullName, typeOfCrime, severity, zipcode]

