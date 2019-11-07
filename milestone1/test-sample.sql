-- QUERIES
-- Whether or not a given username, password combination is valid
SELECT uid --right password
FROM Users
WHERE email = 'ra4ever@duke.edu' AND password = crypt('otherpassword', password);
SELECT uid --wrong password
FROM Users
WHERE email = 'ra4ever@duke.edu' AND password = crypt('incorrectpassword', password);

-- Airlines whose name or abbreviation contain some substring
SELECT *
FROM Airlines
WHERE name LIKE '%Delta%'
OR iata LIKE '%Delta%';

-- Airports whose name or abbreviation contain some substring
SELECT *
FROM Airports
WHERE name LIKE '%Dulles%'
OR iata LIKE '%Dulles%';

-- Flights matching a user
SELECT *
FROM Trips NATURAL JOIN Flights
WHERE uid = 0;

-- Flights belonging to a user and matching a certain trip name
SELECT *
FROM Trips NATURAL JOIN Flights
WHERE uid = 1
AND Trips.trip_name LIKE '%grad%';

-- All flights for a given user over a given timespan
SELECT *
FROM Trips NATURAL JOIN Flights
WHERE uid = 0
AND depart_datetime >= DATE('2019-01-01')
AND arrival_datetime <= DATE('2019-06-01');

-- Total distance and duration for a given user for all trips
SELECT trip_name, SUM(mileage), SUM(duration)
FROM Trips NATURAL JOIN Flights
WHERE uid = 0
GROUP BY tid;

-- Total distance and duration for a given user for a given timespan
SELECT SUM(mileage), SUM(duration)
FROM Trips NATURAL JOIN Flights
WHERE uid = 0
AND depart_datetime >= DATE('2019-01-01')
AND arrival_datetime <= DATE('2019-06-01');

-- Flights from/to a certain airport/city
WITH Depart_airport AS(
	SELECT * FROM airports
),
Arrival_airport AS(
	SELECT * FROM airports
)
SELECT Flights.*
FROM Trips NATURAL JOIN Flights
JOIN Depart_airport ON Depart_Airport.iata = Flights.depart_iata
JOIN Arrival_airport ON Arrival_airport.iata = Flights.arrival_iata
WHERE
(Depart_airport.iata LIKE '%SEA%'
OR Depart_airport.name LIKE '%SEA%'
OR Depart_airport.city LIKE '%SEA%'
OR Arrival_airport.iata LIKE '%Baltimore%'
OR Arrival_airport.name LIKE '%Baltimore%'
OR Arrival_airport.city LIKE '%Baltimore%')
AND uid = 0;

-- Trips that contain a certain airport/city
WITH Depart_airport AS(
	SELECT * FROM airports
),
Arrival_airport AS(
	SELECT * FROM airports
),
Relevant_flights AS(
SELECT tid
FROM Flights
JOIN Airports Depart_airport ON Depart_Airport.iata = Flights.depart_iata
	JOIN Airports Arrival_airport ON Arrival_airport.iata = Flights.arrival_iata
WHERE
(Depart_airport.iata LIKE '%SEA%'
OR Depart_airport.name LIKE '%SEA%'
OR Depart_airport.city LIKE '%SEA%'
OR Arrival_airport.iata LIKE '%SEA%'
OR Arrival_airport.name LIKE '%SEA%'
OR Arrival_airport.city LIKE '%SEA%')
)
SELECT tid, trip_name
FROM Trips NATURAL JOIN Relevant_flights
WHERE uid = 0;

-- Details from a trip
SELECT airport_iata, note
FROM trips NATURAL JOIN Details
WHERE uid = 0
AND tid = 0;

-- Details from an airport
SELECT trip_name, note
FROM trips NATURAL JOIN Details
WHERE uid = 1
AND airport_iata = 'IAD';

-- MODIFICATIONS
-- Users changing flight info
SELECT * FROM flights; --before
UPDATE Flights
SET flight_num = 1234 --can also change other attributes
WHERE fid = 0;
SELECT * FROM flights; --after

-- Users inserting/deleting flights from past trips
DELETE FROM Flights
WHERE fid = 0;
SELECT * FROM flights;
INSERT INTO Flights VALUES(0, 0, 'DL', 1253, 'RDU', 'SEA', '20190505 07:25:00 AM', '20190505 10:13:00 AM', 348, 2355); -- revert

-- User changing email and/or password
SELECT * FROM Users; --before
UPDATE Users
SET email = 'mongolover@duke.edu', password = crypt('newpassword', gen_salt('bf'))
WHERE uid = 0;
SELECT * FROM Users; --after

-- User deleting entire account
DELETE FROM Users
WHERE uid = 0;
SELECT * FROM Users; --after
SELECT * FROM Flights; --after (shows cascade)
INSERT INTO Users VALUES (0, 'sqllover@duke.edu', crypt('password', gen_salt('bf'))); --revert
INSERT INTO Trips VALUES(0, 0, 'to internship'); --revert
INSERT INTO Trips VALUES(2, 0, 'from internship'); --revert
INSERT INTO Flights VALUES(0, 0, 'DL', 1253, 'RDU', 'SEA', '20190505 07:25:00 AM', '20190505 10:13:00 AM', 348, 2355); --revert
INSERT INTO Flights VALUES(3, 2, 'AS', 0922, 'SEA', 'BWI', '20190727 08:00:00 AM', '20190727 4:15:00 PM', 315, 2335); --revert
