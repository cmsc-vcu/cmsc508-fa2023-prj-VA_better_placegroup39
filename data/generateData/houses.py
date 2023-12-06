import json
import random

def generateHouseData(personId):
    dict1 = {}
    
    ForSale = False
    ForRent = False
    salePrice = 0
    rentPrice = 0
    zipcode = random.randint(20101 ,24658)
    randomNum = random.randint(0,3)
    if randomNum > 2:
        return [personId, zipcode, ForSale, salePrice, ForRent, rentPrice]
    elif randomNum == 1:
        ForSale = True
        salePrice = random.randint(500000, 2000000)
    else:
        ForRent = True
        rentPrice = random.randint(800, 2300)
        
    return [personId, zipcode, ForSale, salePrice, ForRent, rentPrice]

