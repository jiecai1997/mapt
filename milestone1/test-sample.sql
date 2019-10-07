-- Whether or not a given username, password combination is valid
SELECT uid
FROM Users
WHERE email = ‘my_email’ AND password = crypt(‘my_password’, password);

-- Airlines whose name or abbreviation contain some substring
SELECT * 
FROM Airlines 
WHERE Airline.name LIKE ‘%my_substring%’
OR Airline.iata_code LIKE ‘%my_substring%’;

-- Airports whose name or abbreviation contain some substring
SELECT * 
FROM Airports 
WHERE Airports.name LIKE ‘%my_substring%’
OR Airports.iata_code LIKE ‘%my_substring%’;

-- Flights matching a user
SELECT *
FROM Trips JOIN Flights
WHERE uid = current_user.uid;

-- Flights belonging to a user and matching a certain trip name
SELECT *
FROM Trips JOIN Flights
WHERE uid = current_user.uid
AND Trips.trip_name LIKE ‘%my_substring%’;

-- All flights for a given user over a given timespan
SELECT *
FROM Trips JOIN Flights
WHERE uid = current_user.uid
AND depart_date >= DATE(my_substring1)
AND arrival_date <= DATE(my_substring2);

-- Total distance and duration for a given user for all trips
SELECT trip_name, SUM(mileage), SUM(duration)
FROM Trips JOIN Flights
WHERE uid = current_user.uid
GROUP BY tid;

-- Total distance and duration for a given user for a given timespan
SELECT SUM(mileage), SUM(duration)
FROM Trips JOIN Flights
WHERE uid = current_user.uid
AND depart_date >= DATE(my_substring1)
AND arrival_date <= DATE(my_substring2);

--Flights from/to a certain airport/country 
WITH Depart_airport AS(
	SELECT * FROM airports
),
Arrival_airport AS(
	SELECT * FROM airports
)
SELECT *
FROM Flights 
JOIN Depart_airport ON Flights.depart_iata
JOIN Arrival_airport ON Flights.arrival_iata
WHERE 
(Depart_airport.iata LIKE ‘%my_airport_iata%’ 
OR Arrival_airport.iata LIKE ‘%my_airport_iata%’
OR Depart_airport.name LIKE ‘%my_airport_name%’
OR Arrival_airport.name LIKE ‘%my_airport_name%’
OR Depart_airport.country LIKE ‘%my_airport_country%’
OR Arrival_airport.country LIKE ‘%my_airport_country%’)
AND uid = current_user.uid;

--Trips that contain a certain airport/country
WITH Depart_airport AS(
	SELECT * FROM airports
),
Arrival_airport AS(
	SELECT * FROM airports
),
Relevant_flights AS(
SELECT tid
FROM Flights 
JOIN Depart_airport ON Flights.depart_iata
	JOIN Arrival_airport ON Flights.arrival_iata
WHERE 
(Depart_airport.iata LIKE ‘%my_airport_iata%’ 
OR Arrival_airport.iata LIKE ‘%my_airport_iata%’
OR Depart_airport.name LIKE ‘%my_airport_name%’
OR Arrival_airport.name LIKE ‘%my_airport_name%’
OR Depart_airport.country LIKE ‘%my_airport_country%’
OR Arrival_airport.country LIKE ‘%my_airport_country%’)
AND uid = current_user.uid
)
SELECT Trips.*
FROM Trips JOIN Relevant_flight_trips ON Trips.tid = Relevant_flights.tid;


