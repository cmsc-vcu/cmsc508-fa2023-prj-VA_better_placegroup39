import json

# Load the JSON data
with open('../generateData/crimes.json', 'r') as file:
    data = json.load(file)

# Generate SQL INSERT statements
insert_statements = ""
for crime_id, values in data.items():
    fullName, typeOfCrime, severity, zipcode, date_of_crime = values
    insert_statements += f"INSERT INTO Crimes (fullName, crimeType, severity, zipcode, date_of_crime) VALUES ('{fullName}', '{typeOfCrime}', {severity}, {zipcode}, '{date_of_crime}');\n"

with open("Crimes_ddl.sql", "w") as f:
    f.write(insert_statements)