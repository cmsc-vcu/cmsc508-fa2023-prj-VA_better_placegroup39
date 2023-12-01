
# Drops all tables.  This section should be amended as new tables are added.

SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS Education_system;
DROP TABLE IF EXISTS Criminal_Activity;
DROP TABLE IF EXISTS Safety_Rating;
DROP TABLE IF EXISTS House_Market;
DROP TABLE IF EXISTS Job_Security;
# ... 
SET FOREIGN_KEY_CHECKS=1;



# zipcode
CREATE TABLE Zipcode(
    zipcode int not null,
    primary key(zipcode)
);


# Education System
CREATE TABLE Education_system(
    zipcode int not null,
    no_public_schools int not null,
    diversity float,
    foreign key(zipcode) references Zipcode (zipcode),
    primary key(zipcode)
);



# Criminal Activity
CREATE TABLE Criminal_Activity (
    zipcode int not null,
    crime_id int primary key,
    police_coverage_grade varchar(255) not null,
    safety_rating varchar(255),
    foreign key(zipcode) references Zipcode (zipcode),
);



# Safety Rating
CREATE TABLE Safety_Rating (
    record_id int primary key auto_increment,
    zipcode int not null,
    crime_type varchar(255),
    crime_activity_time varchar(255),
    severity_points int,
    foreign key(zipcode) references Zipcode (zipcode)
);



 
# Population
create table Population( 
    person_id int primary key, 
    age int,
    race varchar(255),
    networth int, 
    zipcode int not null,
);



# Transportation
create table Transportation( 
    zipcode int not null,
    bike_routes int,
    HasLightTrains boolean, 
    foreign key(zipcode) references Zipcode (zipcode),
    primary key(zipcode)
);


# House Market
create table House_Market( 
    house_id int primary key,
    zipcode int not null,
    rent_price int,
    sale_price int,
    for_sale boolean,
    for_rent boolean,
);


# Open Jobs
create table Job_openings( 
    job_id int primary,
    job_title varchar(255),
    zipcode int not null,
    salary int,
    actively_hiring boolean,
    date_posted date,    
);
