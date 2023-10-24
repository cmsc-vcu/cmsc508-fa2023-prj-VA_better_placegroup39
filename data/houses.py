import json
dict1 = {}
import random
for i in range(100):
    ForSale = False
    ForRent = False
    salePrice = 0
    rentPrice = 0
    zipcode = random.randint(20101 ,24658)
    if random.random() > 0.5:
        ForSale = True
        salePrice = random.randint(500000, 2000000)
    else:
        ForRent = True
        rentPrice = random.randint(800, 2300)
    houseNum = f"House_{i}"
    dict1[houseNum] = [houseNum, zipcode, ForSale, salePrice, ForRent, rentPrice]

outfile = open("houses.json", "w")
json.dump(dict1, outfile, indent = 6)