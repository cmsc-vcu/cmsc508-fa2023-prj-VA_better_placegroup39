
# Drops all tables.  This section should be amended as new tables are added.

SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS Schools;
DROP TABLE IF EXISTS Crimes;
DROP TABLE IF EXISTS Peoples;
DROP TABLE IF EXISTS Transportation;
DROP TABLE IF EXISTS Houses;
DROP TABLE IF EXISTS OpenJobs;

SET FOREIGN_KEY_CHECKS=1;


# Schools
-- schoolId, school_name, number_of_teachers, diversity, quality, zipcode
CREATE TABLE Schools (
    schoolId INT PRIMARY KEY,
    schoolName VARCHAR(255),
    numberOfTeachers INT,
    diversityPercentage DECIMAL,
    quality char,
    zipcode INT
);

# Crimes
-- (crimeId, fullName, typeOfCrime, severity, zipcode, date_of_crime)
CREATE TABLE Crimes (
    crimeId INT PRIMARY KEY,
    fullName VARCHAR(255),
    crimeType VARCHAR(255),
    severity VARCHAR(255),
    zipcode INT,
    date_of_crime DATE
);

# Peoples
-- # Population aggregate data
CREATE TABLE Peoples (
    personId INT PRIMARY KEY,
    name VARCHAR(255),
    salary INT,
    age INT,
    ethnicity VARCHAR(255),
    zipcode INT
);


# Transportation
CREATE TABLE Transportation (
    routeId VARCHAR(255) PRIMARY KEY,
    isBikeRoute BOOLEAN,
    isLightTrainRoute BOOLEAN,
    startingZipcode INT,
    endingZipcode INT
);

# Houses
-- house_id, person_id, house_num, zipcode, ForSale, salePrice, ForRent, rentPrice
CREATE TABLE Houses (
    houseId INT PRIMARY KEY,
    ownerPersonId INT,
    house_num INT,
    zipcode INT,
    ForSale BOOLEAN,
    salePrice DECIMAL,
    ForRent BOOLEAN,
    rentPrice DECIMAL
);

# Open Jobs
-- jobId, company, date, salary, actively_hiring, zipcode
CREATE TABLE OpenJobs (
    jobId INT PRIMARY KEY,
    company VARCHAR(255),
    date DATE,
    salary INT,
    actively_hiring BOOLEAN,
    zipcode INT
);
