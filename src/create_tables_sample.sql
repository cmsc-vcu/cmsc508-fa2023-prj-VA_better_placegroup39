
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
CREATE TABLE Education_system(
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
    police_coverage_grade varchar(255) not null,
    safety_rating varchar(255),
    foreign key(zipcode) references Zipcode (zipcode),
    primary key(zipcode)
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
    zipcode int not null,
    Population int,
    Diversity float,
    foreign key(zipcode) references Zipcode (zipcode),
    primary key(zipcode)
);



# Transportation
create table Transportation( 
    zipcode int not null,
    bike_routes int,
    HasLightTrains boolean, #T/F
    foreign key(zipcode) references Zipcode (zipcode),
    primary key(zipcode)
);


# House Market
create table House_Market( 
    zipcode int not null,
    avg_rent int,
    avg_price int,
    houses_4_sale int,
    foreign key(zipcode) references Zipcode (zipcode),
    primary key(zipcode)
);


# Section 
# Job Security
create table Job_Security( 
    zipcode int not null,
    open_jobs int,
    layoff_rate int,
    foreign key(zipcode) references Zipcode (zipcode),
    primary key(zipcode)
);
