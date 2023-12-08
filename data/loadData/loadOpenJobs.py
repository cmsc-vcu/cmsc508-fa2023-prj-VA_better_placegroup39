import json
import json

insert_statements = []

# Load the openJobs.json file
with open("../generateData/openJobs.json", "r") as open_jobs_file:
    open_jobs_data = json.load(open_jobs_file)

# Modify the for statement based on the data type
for job_id, job_data in open_jobs_data.items():
    company = job_data[0]
    date = job_data[1]
    salary = job_data[2]
    actively_hiring = job_data[3]
    zipcode = job_data[4]
    insert_statement = f'INSERT INTO OpenJobs (jobId, company, date, salary, actively_hiring, zipcode) VALUES ({job_id}, "{company}", "{date}", {salary}, {actively_hiring}, "{zipcode}");'
    insert_statements.append(insert_statement)

# Write the insert statements to the SQL file
with open("OpenJobs_ddl.sql", "w") as sql_file:
    for statement in insert_statements:
        sql_file.write(statement + "\n")
