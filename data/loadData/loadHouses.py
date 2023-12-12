
import json

# Data format
# dict[houseId] = [personId, houseNum, zipcode, ForSale, salePrice, ForRent, rentPrice]

with open("../generateData/houses.json", "r") as houses_file:
    houses_data = json.load(houses_file)

# Extract the insert statements from the houses_data
insert_statements = []
for house_id, house_data in houses_data.items():
    person_id = house_data[0]
    zipcode = house_data[1]
    for_sale = house_data[2]
    sale_price = house_data[3]
    for_rent = house_data[4]
    rent_price = house_data[5]
    insert_statement = f"INSERT INTO Houses (ownerPersonID, zipcode, ForSale, salePrice, ForRent, rentPrice) VALUES ('{person_id}', '{zipcode}', {for_sale}, {sale_price}, {for_rent}, {rent_price});"
    insert_statements.append(insert_statement)

# Write the insert statements to the SQL file
with open("Houses_ddl.sql", "w") as sql_file:
    for statement in insert_statements:
        sql_file.write(statement + "\n")
