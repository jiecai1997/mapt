CREATE EXTENSION pgcrypto; 

CREATE TABLE Users
(uid INTEGER NOT NULL PRIMARY KEY, 
email VARCHAR(50) NOT NULL UNIQUE CHECK (email LIKE '%_@_%._%'), 
password VARCHAR(60) NOT NULL,
public BOOLEAN NOT NULL,
username VARCHAR(50) NOT NULL UNIQUE);

CREATE TABLE Trips
(tid INTEGER NOT NULL PRIMARY KEY,
uid INTEGER REFERENCES Users(uid) ON DELETE CASCADE,
trip_name VARCHAR(30));

CREATE TABLE Airlines
(iata CHAR(2) NOT NULL PRIMARY KEY,
name VARCHAR(50) NOT NULL);

CREATE TABLE Airports
(iata CHAR(3) NOT NULL PRIMARY KEY,
name VARCHAR(75) NOT NULL, 
city VARCHAR(75) NOT NULL,
country VARCHAR(50) NOT NULL,
latitude FLOAT NOT NULL CHECK (latitude >= -90 AND latitude <= 90), 
longitude FLOAT NOT NULL CHECK (longitude >= -180 AND longitude <= 180), 
time_zone VARCHAR(60) NOT NULL,
dst CHAR(1) NOT NULL CHECK (dst IN ('E', 'A', 'S', 'O', 'Z', 'N', 'U')));

CREATE TABLE Flights
(fid INTEGER PRIMARY KEY,
tid INTEGER NOT NULL REFERENCES Trips(tid) ON DELETE CASCADE,
airline_iata CHAR(2) REFERENCES Airlines(iata), 
flight_num INTEGER CHECK (flight_num > 0),
depart_iata CHAR(3) NOT NULL REFERENCES Airports(iata) ON DELETE CASCADE,
arrival_iata CHAR(3) NOT NULL REFERENCES Airports(iata) ON DELETE CASCADE,
depart_datetime DATE NOT NULL,
arrival_datetime DATE NOT NULL,
duration INTEGER NOT NULL CHECK (duration > 0),
mileage INTEGER NOT NULL CHECK (mileage > 0));

CREATE TABLE Details
(did INTEGER PRIMARY KEY,
tid INTEGER NOT NULL REFERENCES Trips(tid) ON DELETE CASCADE,
airport_iata CHAR(3) NOT NULL REFERENCES Airports(iata) ON DELETE CASCADE,
note VARCHAR(280) NOT NULL);


CREATE FUNCTION TF_Detail_not_visited_airportiata() RETURNS TRIGGER AS $$
BEGIN
  IF NEW.airport_iata NOT IN (SELECT depart_iata 
				FROM Flights
				WHERE NEW.tid=Flights.tid 
		     	  UNION
			  SELECT arrival_iata
				FROM Flights
				WHERE NEW.tid=Flights.tid) THEN
	RAISE EXCEPTION 'cannot write a detail for an airport not visited on this trip';
	END If;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER TG_Detail_not_visited_airportiata
  BEFORE INSERT OR UPDATE ON Details
  FOR EACH ROW
  EXECUTE PROCEDURE TF_Detail_not_visited_airportiata();


INSERT INTO Users VALUES (0, 'sqllover@duke.edu', crypt('password', gen_salt('bf')));
INSERT INTO Users VALUES (1, 'ra4ever@duke.edu', crypt('otherpassword', gen_salt('bf')));

INSERT INTO Trips VALUES(0, 0, 'to internship');
INSERT INTO Trips VALUES(1, 1, 'graduation');
INSERT INTO Trips VALUES(2, 0, 'from internship');


INSERT INTO Airlines VALUES('DL', 'Delta Air Lines');
INSERT INTO Airlines VALUES ('AS', 'Alaska Airlines');

INSERT INTO Airports VALUES ('RDU', 'Raleigh Durham International Airport', 'Raleigh-Durham', 'USA', 35.8776, -78.7875, 'America/ New_York', 'A');
INSERT INTO Airports VALUES ('IAD', 'Washington Dulles International Airport', 'Washington, DC', 'USA', 38.9445, -77.4558, 'America/ New_York', 'A');
INSERT INTO Airports VALUES ('SEA', 'Seattle Tacoma International Airport', 'Seattle', 'USA', 47.4490, -122.309, 'America/ Los_Angeles', 'A');
INSERT INTO Airports VALUES ('BWI', 'Baltimore/Washington International Thurgood Marshall Airport', 'Baltimore', 'USA', 39.1754, -76.6683, 'America/ New_York', 'A');

INSERT INTO Flights VALUES(3, 2, 'AS', 0922, 'SEA', 'BWI', '20190727 08:00:00 AM', '20190727 4:15:00 PM', 315, 2335); 
INSERT INTO Flights VALUES(2, 1, 'DL', 2220, 'IAD', 'SEA', '20190609 05:00:00 PM', '20190609 07:39:00 PM', 339, 2306); 
INSERT INTO Flights VALUES(1, 1, 'DL', 2680, 'SEA', 'IAD', '20190605 10:45:00 PM', '20190606 06:07:00 AM', 339, 2306); 
INSERT INTO Flights VALUES(0, 0, 'DL', 1253, 'RDU', 'SEA', '20190505 07:25:00 AM', '20190505 10:13:00 AM', 348, 2355); 

INSERT INTO Details VALUES(1, 1, 'IAD', 'Best place to get boba is TeaDM');
INSERT INTO Details VALUES(0, 1, 'IAD', 'Lots of cool museums to go to!');

