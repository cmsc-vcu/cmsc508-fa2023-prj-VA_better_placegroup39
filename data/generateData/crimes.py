import random
from datetime import datetime

# Expanded list of crimes with severity points (0 to 5)
crimes = [
    ["Grand Theft", 1], ["Larceny", 1], ["Arson", 4], ["Shoplifting", 0], 
    ["Armed Robbery", 5], ["Robbery", 2], ["Burglary", 3], ["Vandalism", 2], 
    ["Assault", 4], ["Fraud", 1]
]

def generate_random_date(start_year=2010, end_year=2023):
    # Generate a random date within the specified range
    year = random.randint(start_year, end_year)
    month = random.randint(1, 12)
    day = random.randint(1, 28)  # To avoid issues with February
    return datetime(year, month, day).strftime("%Y-%m-%d")

def generateCrimeData(fullName):
    
    crime = crimes[random.randint(0, len(crimes)-1)]
    typeOfCrime = crime[0]
    severity = crime[1]
    zipcode = random.randint(20101, 24658)
    date_of_crime = generate_random_date()
    return [fullName, typeOfCrime, severity, zipcode, date_of_crime]

