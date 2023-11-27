import json
import names
import random
from datetime import datetime, timedelta


def generateCompanyNames():
    companies = []
    for i in range(50):
        companyName = names.get_first_name() + " LLC"
        companies.append(companyName)
    return companies

def generate_random_date():
    year = random.randint(2020, 2023)
    month = random.randint(1, 12)
    day = random.randint(1, 28)  # Choosing 28 to avoid complications with February
    return datetime(year, month, day).strftime('%Y-%m-%d')

def main():
    boolean = [True, False]
    dict1 = {}
    companies = generateCompanyNames()
    for jobId in range(100):
        company = companies[random.randint(0, 49)]
        salary = random.randint(50000, 350000)
        zipcode = random.randint(20101 ,24658)
        date = generate_random_date()
        activelyHiring = boolean[random.randint(0,1)]
        dict1[jobId] = [company, date, salary, activelyHiring, zipcode]

    outfile = open("openJobs.json", "w")
    json.dump(dict1, outfile, indent = 6)

if __name__ == "__main__":
    main()