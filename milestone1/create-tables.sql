CREATE TABLE Flights
(fid INTEGER PRIMARY KEY,
tid INTEGER NOT NULL REFERENCES Trips.tid,
flight_airline CHAR(3) REFERENCES Airlines.iata_code, 
flight_num INTEGER,
depart_aid CHAR(3) NOT NULL REFERENCES Airports.iata_code,
arrival_aid CHAR(4) NOT NULL REFERENCES Airports.iata_code,
depart_datetime DATE NOT NULL,
arrival_datetime DATE NOT NULL,
duration INTEGER NOT NULL,
mileage INTEGER NOT NULL);

CREATE TABLE Airlines
(iata_code CHAR(2) NOT NULL PRIMARY KEY,
al_name VARCHAR(50) NOT NULL);

CREATE TABLE Airports
(iata_code CHAR(3) NOT NULL PRIMARY KEY,
name VARCHAR(75) NOT NULL, 
city VARCHAR(75) NOT NULL,
country VARCHAR(50) NOT NULL,
longitude FLOAT NOT NULL, 
latitude FLOAT NOT NULL, 
time_zone VARCHAR(5) NOT NULL,
dst CHAR(1) NOT NULL IN ('E', 'A', 'S', 'O', 'Z', 'N', 'U'));

CREATE TABLE Users
(uid INTEGER NOT NULL PRIMARY KEY, 
email VARCHAR(50) NOT NULL UNIQUE, 
password VARCHAR(50) NOT NULL);

CREATE TABLE Trips
(tid INTEGER NOT NULL PRIMARY KEY,
uid REFERENCES Users.uid,
trip_name VARCHAR(30));


INSERT INTO USER VALUES (0, 'sqllover@duke.edu', 'encryptedpassword');
INSERT INTO USER VALUES (1, 'ra4ever@duke.edu', 'otherpassword');

INSERT INTO FLIGHTS VALUES(3, 2, 'ASA', 0922, 'SEA', 'BWI', '20190727 8:00:00 AM', '20190727 4:15:00 PM', 315, 2335); 




