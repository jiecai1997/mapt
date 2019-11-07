from pandas import DataFrame
import sqlite3 as sql

with sql.connect("app.db") as con:
    con.row_factory = sql.Row

    # #Query 1 -
    # cur = con.cursor()
    # cur.execute("SELECT user.uid FROM user WHERE user.uid = 1 AND user.password = 'hello_password'")
    # rows = cur.fetchall()
    # df = DataFrame(rows)
    # df.to_csv(r'./app/csv/01test.csv', index=False)
    # cur.close()
    #
    # # Query 2 - Whether or not a given username, password combination is valid: right username
    # cur = con.cursor()
    # cur.execute("SELECT user.uid FROM user WHERE user.uid = 1 AND user.password = 'incorrect_password'")
    # rows = cur.fetchall()
    # df = DataFrame(rows)
    # df.to_csv(r'./app/csv/02test.csv', index=False)
    # cur.close()
    #
    # # Query 3 - Airlines whose name or abbreviation contain some substring
    # cur = con.cursor()
    # cur.execute("SELECT * FROM airlines WHERE airlines.name LIKE '%Delta%' OR airlines.iata LIKE '%Delta'")
    # rows = cur.fetchall()
    # df = DataFrame(rows)
    # df.to_csv(r'./app/csv/03test.csv', index=False)
    # cur.close()
    #
    # # Query 4 - Airports whose name or abbreviation contain some substring
    # cur = con.cursor()
    # cur.execute("SELECT * FROM airports WHERE airports.name LIKE '%Dulles%' OR airports.iata LIKE '%Dulles'")
    # rows = cur.fetchall()
    # df = DataFrame(rows)
    # df.to_csv(r'./app/csv/04test.csv',index=False)
    # cur.close()
    #
    # # Query 5 - Flights matching a user
    # cur = con.cursor()
    # cur.execute("SELECT * FROM trips NATURAL JOIN flights WHERE uid=0")
    # rows = cur.fetchall()
    # df = DataFrame(rows)
    # df.to_csv(r'./app/csv/05test.csv', index=False)
    # cur.close()
    #
    # # Query 6 - Flights belonging to a user and matching a certain trip name
    # cur = con.cursor()
    # cur.execute("SELECT * FROM trips NATURAL JOIN flights WHERE uid=1 and trip_name LIKE '%grad%'")
    # rows = cur.fetchall()
    # df = DataFrame(rows)
    # df.to_csv(r'./app/csv/06test.csv', index=False)
    # cur.close()

    # # Query 7 - All flights for a given user over a given timespan
    # cur = con.cursor()
    # cur.execute("""
    # SELECT *
    # FROM trips NATURAL JOIN flights
    # WHERE uid = 0
    # AND depart_datetime >= '20190101 00:00:00 AM'
    # AND arrival_datetime <= '20190601 11:59:59 PM'
    # """)
    # rows = cur.fetchall()
    # df = DataFrame(rows)
    # df.to_csv(r'./app/csv/07test.csv', index=False)
    # cur.close()
    #
    # # Query 8 - Total distance and duration for a given user for all trips
    # cur = con.cursor()
    # cur.execute("SELECT trip_name, SUM(mileage), SUM(duration) FROM trips NATURAL JOIN flights WHERE uid=0 GROUP BY tid")
    # rows = cur.fetchall()
    # df = DataFrame(rows)
    # df.to_csv(r'./app/csv/08test.csv', index=False)
    # cur.close()

    # #Query 9 - Total distance and duration for a given user for a given timespan
    # cur = con.cursor()
    # cur.execute("""
    # SELECT SUM(mileage), SUM(duration)
    # FROM trips NATURAL JOIN flights
    # WHERE uid = 0
    # AND depart_datetime >= '20190101 00:00:00 AM'
    # AND arrival_datetime <= '20190601 11:59:59 PM'
    # """)
    # rows = cur.fetchall()
    # df = DataFrame(rows)
    # df.to_csv(r'./app/csv/09test.csv', index=False)
    # cur.close()

    #Query 10 - Flights from/to a certain airport/city DOESNT WORK
    cur = con.cursor()
    cur.execute("""
    WITH Depart_airport AS(
    	SELECT * FROM airports
    ),
    Arrival_airport AS(
    	SELECT * FROM airports
    )
    SELECT flights.*
    FROM trips NATURAL JOIN flights
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
    	SELECT * FROM airports
    ),
    Arrival_airport AS(
    	SELECT * FROM airports
    ),
    Relevant_flights AS(
    SELECT tid
    FROM flights
    JOIN airports Depart_airport ON Depart_Airport.iata = flights.depart_iata
    	JOIN airports Arrival_airport ON Arrival_airport.iata = flights.arrival_iata
    WHERE
    (Depart_airport.iata LIKE '%SEA%'
    OR Depart_airport.name LIKE '%SEA%'
    OR Depart_airport.city LIKE '%SEA%'
    OR Arrival_airport.iata LIKE '%SEA%'
    OR Arrival_airport.name LIKE '%SEA%'
    OR Arrival_airport.city LIKE '%SEA%')
    )
    SELECT tid, trip_name
    FROM trips NATURAL JOIN Relevant_flights
    WHERE uid = 0
    """)
    rows = cur.fetchall()
    df = DataFrame(rows)
    df.to_csv(r'./app/csv/11test.csv',index=False)
    cur.close()

    # #Query 12 - Details from a trip
    # cur = con.cursor()
    # cur.execute('SELECT iata, note FROM trips NATURAL JOIN Details WHERE uid = 0 AND tid = 0')
    # rows = cur.fetchall()
    # df = DataFrame(rows)
    # df.to_csv(r'./app/csv/12test.csv',index=False)
    # cur.close()
    #
    # #Query 13 - Details from an Airport
    # cur = con.cursor()
    # cur.execute("SELECT trip_name, note FROM trips NATURAL JOIN Details WHERE uid = 1 AND iata = 'IAD'")
    # rows = cur.fetchall()
    # df = DataFrame(rows)
    # df.to_csv(r'./app/csv/13test.csv',index=False)
    # cur.close()


    cur = con.cursor()
    cur.execute("SELECT * FROM user WHERE user.uid = 1")
    rows = cur.fetchall()
    df = DataFrame(rows)
    df.to_csv(r'./app/csv/test.csv',header = ['UID','Email','Username','Password','Public'],index=False)
    cur.close()



# -- MODIFICATIONS
# -- Users changing flight info
# SELECT * FROM flights; --before
# UPDATE Flights
# SET flight_num = 1234 --can also change other attributes
# WHERE fid = 0;
# SELECT * FROM flights; --after
#
# -- Users inserting/deleting flights from past trips
# DELETE FROM Flights
# WHERE fid = 0;
# SELECT * FROM flights;
# INSERT INTO Flights VALUES(0, 0, 'DL', 1253, 'RDU', 'SEA', '20190505 07:25:00 AM', '20190505 10:13:00 AM', 348, 2355); -- revert
#
# -- User changing email and/or password
# SELECT * FROM Users; --before
# UPDATE Users
# SET email = 'mongolover@duke.edu', password = crypt('newpassword', gen_salt('bf'))
# WHERE uid = 0;
# SELECT * FROM Users; --after
#
# -- User deleting entire account
# DELETE FROM Users
# WHERE uid = 0;
# SELECT * FROM Users; --after
# SELECT * FROM Flights; --after (shows cascade)
# INSERT INTO Users VALUES (0, 'sqllover@duke.edu', crypt('password', gen_salt('bf'))); --revert
# INSERT INTO Trips VALUES(0, 0, 'to internship'); --revert
# INSERT INTO Trips VALUES(2, 0, 'from internship'); --revert
# INSERT INTO Flights VALUES(0, 0, 'DL', 1253, 'RDU', 'SEA', '20190505 07:25:00 AM', '20190505 10:13:00 AM', 348, 2355); --revert
# INSERT INTO Flights VALUES(3, 2, 'AS', 0922, 'SEA', 'BWI', '20190727 08:00:00 AM', '20190727 4:15:00 PM', 315, 2335); --revert
