-- Whether or not a given username, password combination is valid
SELECT uid
FROM Users
WHERE email = 'ra4ever@duke.edu' AND password = crypt('otherpassword', password);

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
SELECT *
FROM Flights 
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

--Trips that contain a certain airport/city
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
OR Arrival_airport.iata LIKE '%Baltimore%'
OR Arrival_airport.name LIKE '%Baltimore%'
OR Arrival_airport.city LIKE '%Baltimore%')
AND uid = 0;
)
SELECT Trips.*
FROM Trips JOIN Relevant_flight_trips ON Trips.tid = Relevant_flights.tid;


