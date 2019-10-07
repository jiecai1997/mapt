CREATE TABLE Flights
(fid INTEGER PRIMARY KEY,
tid INTEGER NOT NULL REFERENCES Trips.tid,
airline_iata CHAR(2) REFERENCES Airlines.iata, 
flight_num INTEGER CHECK (flight_num > 0),
depart_iata CHAR(3) NOT NULL REFERENCES Airports.iata,
arrival_iata CHAR(3) NOT NULL REFERENCES Airports.iata,
depart_datetime DATE NOT NULL,
arrival_datetime DATE NOT NULL,
duration INTEGER NOT NULL CHECK (duration > 0),
mileage INTEGER NOT NULL CHECK (mileage > 0));

CREATE TABLE Airlines
(iata CHAR(2) NOT NULL PRIMARY KEY,
name VARCHAR(50) NOT NULL);

CREATE TABLE Airports
(iata CHAR(3) NOT NULL PRIMARY KEY,
name VARCHAR(75) NOT NULL, 
city VARCHAR(75) NOT NULL,
country VARCHAR(50) NOT NULL,
longitude FLOAT NOT NULL CHECK (longitude >= -180 AND longitude <= 180), 
latitude FLOAT NOT NULL CHECK (latitude >= -90 AND latitude <= 90), 
time_zone VARCHAR(60) NOT NULL,
dst CHAR(1) NOT NULL CHECK (dst IN ('E', 'A', 'S', 'O', 'Z', 'N', 'U')));

CREATE TABLE Users
(uid INTEGER NOT NULL PRIMARY KEY, 
email VARCHAR(50) NOT NULL UNIQUE CHECK (email LIKE '%_@_%._%'), 
password VARCHAR(50) NOT NULL);

CREATE TABLE Trips
(tid INTEGER NOT NULL PRIMARY KEY,
uid REFERENCES Users.uid,
trip_name VARCHAR(30));


INSERT INTO USER VALUES (0, 'sqllover@duke.edu', 'encryptedpassword');
INSERT INTO USER VALUES (1, 'ra4ever@duke.edu', 'otherpassword');

INSERT INTO FLIGHTS VALUES(3, 2, 'ASA', 0922, 'SEA', 'BWI', '20190727 08:00:00 AM', '20190727 4:15:00 PM', 315, 2335); 
INSERT INTO FLIGHTS VALUES(2, 1, 'DAL', 2220, 'IAD', 'SEA', '20190609 05:00:00 PM', '20190609 07:39:00 PM', 339, 2306); 
INSERT INTO FLIGHTS VALUES(1, 1, 'DAL', 2680, 'SEA', 'IAD', '20190605 10:45:00 PM', '20190606 06:07:00 AM', 339, 2306); 
INSERT INTO FLIGHTS VALUES(0, 0, 'DAL', 1253, 'RDU', 'SEA', '20190505 07:25:00 AM', '20190505 10:13:00 AM', 348, 2355); 

INSERT INTO TRIPS VALUES(0, 0, 'to internship');
INSERT INTO TRIPS VALUES(1, 1, 'graduation');
INSERT INTO TRIPS VALUES(0, 2, 'from internship');

INSERT INTO AIRLINES VALUES('DAL', 'Delta Air Lines');
INSERT INTO AIRLINES VALUES ('ASA', 'Alaska Airlines');

INSERT INTO AIRPORTS VALUES ('RDU', 'Raleigh Durham International Airport', 'Raleigh-Durham', 'USA', 35.8776, -78.7875, 'America/ New_York', 'A');
INSERT INTO AIRPORTS VALUES ('IAD', 'Washington Dulles International Airport', 'Washington, DC', 'USA', 38.9445, -77.4558, 'America/ New_York', 'A');
INSERT INTO AIRPORTS VALUES ('SEA', 'Seattle Tacoma International Airport', 'Seattle', 'USA', 47.4490, -122.309, 'America/ Los_Angeles', 'A');
INSERT INTO AIRPORTS VALUES ('BWI', 'Baltimore/Washington International Thurgood Marshall Airport', 'Baltimore', 'USA', 39.1754, -76.6683, 'America/ New_York', 'A');



