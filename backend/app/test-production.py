from pandas import DataFrame
import sqlite3 as sql

with sql.connect("app.db") as con:
    con.row_factory = sql.Row

    #Query 1 - Whether or not a given username, password combination is valid: right username
    cur = con.cursor()
    cur.execute("SELECT user.uid FROM user WHERE user.uid = 1 AND user.password = 'hello_password'")
    rows = cur.fetchall()
    df = DataFrame(rows)
    df.to_csv(r'./app/csv/01test.csv', index=False)
    cur.close()

    # Query 2 - Whether or not a given username, password combination is valid: wrong username
    cur = con.cursor()
    cur.execute("SELECT user.uid FROM user WHERE user.uid = 1 AND user.password = 'incorrect_password'")
    rows = cur.fetchall()
    df = DataFrame(rows)
    df.to_csv(r'./app/csv/02test.csv', index=False)
    cur.close()

    # Query 3 - Airlines whose name or abbreviation contain some substring
    cur = con.cursor()
    cur.execute("SELECT * FROM airline WHERE airline.name LIKE '%Delta%' OR airline.iata LIKE '%Delta'")
    rows = cur.fetchall()
    df = DataFrame(rows)
    df.to_csv(r'./app/csv/03test.csv', index=False)
    cur.close()

    # Query 4 - Airports whose name or abbreviation contain some substring
    cur = con.cursor()
    cur.execute("SELECT * FROM airport WHERE airport.name LIKE '%Dulles%' OR airport.iata LIKE '%Dulles'")
    rows = cur.fetchall()
    df = DataFrame(rows)
    df.to_csv(r'./app/csv/04test.csv',index=False)
    cur.close()

    # Query 5 - Flights matching a user
    cur = con.cursor()
    cur.execute("SELECT * FROM trip NATURAL JOIN flight WHERE uid=0")
    rows = cur.fetchall()
    df = DataFrame(rows)
    df.to_csv(r'./app/csv/05test.csv', index=False)
    cur.close()

    # Query 6 - Flights belonging to a user and matching a certain trip name
    cur = con.cursor()
    cur.execute("SELECT * FROM trip NATURAL JOIN flight WHERE uid=1 and trip_name LIKE '%grad%'")
    rows = cur.fetchall()
    df = DataFrame(rows)
    df.to_csv(r'./app/csv/06test.csv', index=False)
    cur.close()

    # Query 7 - All flights for a given user over a given timespan
    cur = con.cursor()
    cur.execute("""
    SELECT *
    FROM trip NATURAL JOIN flight
    WHERE uid = 0
    AND depart_datetime >= '20190101 00:00:00 AM'
    AND arrival_datetime <= '20190601 11:59:59 PM'
    """)
    rows = cur.fetchall()
    df = DataFrame(rows)
    df.to_csv(r'./app/csv/07test.csv', index=False)
    cur.close()

    # Query 8 - Total distance and duration for a given user for all trips
    cur = con.cursor()
    cur.execute("SELECT trip_name, SUM(mileage), SUM(duration) FROM trip NATURAL JOIN flight WHERE uid=0 GROUP BY tid")
    rows = cur.fetchall()
    df = DataFrame(rows)
    df.to_csv(r'./app/csv/08test.csv', index=False)
    cur.close()

    #Query 9 - Total distance and duration for a given user for a given timespan
    cur = con.cursor()
    cur.execute("""
    SELECT SUM(mileage), SUM(duration)
    FROM trip NATURAL JOIN flights
    WHERE uid = 0
    AND depart_datetime >= '20190101 00:00:00 AM'
    AND arrival_datetime <= '20190601 11:59:59 PM'
    """)
    rows = cur.fetchall()
    df = DataFrame(rows)
    df.to_csv(r'./app/csv/09test.csv', index=False)
    cur.close()

    #Query 10 - Flights from/to a certain airport/city DOESNT WORK
    cur = con.cursor()
    cur.execute("""
    WITH Depart_airport AS(
    	SELECT * FROM airport
    ),
    Arrival_airport AS(
    	SELECT * FROM airport
    )
    SELECT flight.*
    FROM trip NATURAL JOIN flights
    JOIN Depart_airport ON Depart_Airport.iata = flights.depart_iata
    JOIN Arrival_airport ON Arrival_airport.iata = flights.arrival_iata
    WHERE
    (Depart_airport.iata LIKE '%SEA%'
    OR Depart_airport.name LIKE '%SEA%'
    OR Depart_airport.city LIKE '%SEA%'
    OR Arrival_airport.iata LIKE '%Baltimore%'
    OR Arrival_airport.name LIKE '%Baltimore%'
    OR Arrival_airport.city LIKE '%Baltimore%')
    AND uid = 0
    """)
    rows = cur.fetchall()
    df = DataFrame(rows)
    df.to_csv(r'./app/csv/10test.csv',index=False)
    cur.close()

    #Query 11 - Trips that contain a certain airport/city
    cur = con.cursor()
    cur.execute("""
    WITH Depart_airport AS(
    	SELECT * FROM airport
    ),
    Arrival_airport AS(
    	SELECT * FROM airport
    ),
    Relevant_flights AS(
    SELECT tid
    FROM flight
    JOIN airport Depart_airport ON Depart_Airport.iata = flight.depart_iata
    	JOIN airport Arrival_airport ON Arrival_airport.iata = flight.arrival_iata
    WHERE
    (Depart_airport.iata LIKE '%SEA%'
    OR Depart_airport.name LIKE '%SEA%'
    OR Depart_airport.city LIKE '%SEA%'
    OR Arrival_airport.iata LIKE '%SEA%'
    OR Arrival_airport.name LIKE '%SEA%'
    OR Arrival_airport.city LIKE '%SEA%')
    )
    SELECT tid, trip_name
    FROM trip NATURAL JOIN Relevant_flights
    WHERE uid = 0
    """)
    rows = cur.fetchall()
    df = DataFrame(rows)
    df.to_csv(r'./app/csv/11test.csv',index=False)
    cur.close()

    #Query 12 - Details from a trip
    cur = con.cursor()
    cur.execute('SELECT iata, note FROM trip NATURAL JOIN Detail WHERE uid = 0 AND tid = 0')
    rows = cur.fetchall()
    df = DataFrame(rows)
    df.to_csv(r'./app/csv/12test.csv',index=False)
    cur.close()

    #Query 13 - Details from an Airport
    cur = con.cursor()
    cur.execute("SELECT trip_name, note FROM trip NATURAL JOIN Detail WHERE uid = 1 AND iata = 'IAD'")
    rows = cur.fetchall()
    df = DataFrame(rows)
    df.to_csv(r'./app/csv/13test.csv',index=False)
    cur.close()

    #Query 14 - Users changing flight info
    cur = con.cursor()
    cur.execute("SELECT * FROM flight")
    rows = cur.fetchall()
    df = DataFrame(rows)
    df.to_csv(r'./app/csv/14testpart1.csv',index=False)
    cur.close()
    cur = con.cursor()
    cur.execute("UPDATE Flight SET flight_num = 1234 WHERE fid = 0")
    cur.execute("SELECT * FROM flight")
    rows = cur.fetchall()
    df = DataFrame(rows)
    df.to_csv(r'./app/csv/14testpart2.csv',index=False)
    cur.close()

    #Query 15 - Users inserting/deleting flights from past trips
    cur = con.cursor()
    cur.execute("DELETE FROM Flight WHERE fid = 0")
    cur.execute("SELECT * FROM Flight")
    rows = cur.fetchall()
    df = DataFrame(rows)
    df.to_csv(r'./app/csv/15.csv',index=False)
    cur.execute("DELETE FROM Flight WHERE fid = 0")
    cur.close()
    cur = con.cursor()
    cur.execute("INSERT INTO Flight VALUES(0, 0, 'DL', 1253, 'RDU', 'SEA', '20190505 07:25:00 AM', '20190505 10:13:00 AM', 348, 2355")
    cur.close()

    #Query 16 - User changing email and/or password
    cur = con.cursor()
    cur.execute("SELECT * FROM user")
    rows = cur.fetchall()
    df = DataFrame(rows)
    df.to_csv(r'./app/csv/16testpart1.csv',index=False)
    cur.close()
    cur = con.cursor()
    cur.execute("UPDATE user SET email = 'mongolover@duke.edu', password = 'newpassword' WHERE uid = 0")
    cur.execute("SELECT * FROM user")
    rows = cur.fetchall()
    df = DataFrame(rows)
    df.to_csv(r'./app/csv/16testpart2.csv',index=False)
    cur.close()

    #Query 17 - User deleting account
    cur = con.cursor()
    cur.execute("DELETE FROM User WHERE uid = 0")
    cur.execute("SELECT * FROM User")
    #Cascade not implemented yet
    rows = cur.fetchall()
    df = DataFrame(rows)
    df.to_csv(r'./app/csv/17.csv',index=False)
    cur.execute("INSERT INTO User VALUES (0, 'sqllover','sqllover@duke.edu', 'password',1)")
    cur.close()
