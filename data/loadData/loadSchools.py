import json

# Data type
# dict1[schoolID] = [schoolName, numberOfTeachers, diversity, quality, zipcode]

with open("../generateData/schools.json", "r") as schools_file:
    schools_data = json.load(schools_file)

# Extract the insert statements from the schools_data
insert_statements = []
for school_id, school_data in schools_data.items():
    school_name = school_data[0]
    number_of_teachers = school_data[1]
    diversity = school_data[2].replace("%", "")
    quality = f'{school_data[3]}'
    zipcode = school_data[4]
    insert_statement = f"INSERT INTO Schools (schoolName, numberOfTeachers, diversityPercentage, quality, zipcode) VALUES ('{school_name}', {number_of_teachers}, {diversity}, '{quality}', '{zipcode}');"
    insert_statements.append(insert_statement)

# Write the insert statements to the SQL file
with open("Schools_ddl.sql", "w") as sql_file:
    for statement in insert_statements:
        sql_file.write(statement + "\n")
