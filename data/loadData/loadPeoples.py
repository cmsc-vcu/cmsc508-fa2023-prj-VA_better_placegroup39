
import json

# Load the peoples.json file
with open("../generateData/peoples.json", "r") as peoples_file:
    peoples_data = json.load(peoples_file)

# Extract the insert statements from the peoples_data
insert_statements = []
for person_id, person_data in peoples_data.items():
    name = person_data[0]
    salary = person_data[1]
    age = person_data[2]
    race = person_data[3]
    zipcode = person_data[4]
    insert_statement = f"INSERT INTO Peoples (name, salary, age, ethnicity, zipcode) VALUES ('{name}', {salary}, {age}, '{race}', {zipcode});"
    insert_statements.append(insert_statement)

# Write the insert statements to the SQL file
with open("Peoples_ddl.sql", "w") as sql_file:
    for statement in insert_statements:
        sql_file.write(statement + "\n")
