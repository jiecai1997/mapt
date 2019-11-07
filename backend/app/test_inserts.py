from flask import render_template, flash, redirect, url_for, session, request
from flask_login import login_user, current_user, logout_user, login_required
import sqlite3 as sql
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
import csv as csv
from csv import reader


with sql.connect("app.db") as con:
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("INSERT INTO User VALUES (0, 'sqllover', 'sqllover@duke.edu', 'password', 1)")
    cur.execute("INSERT INTO User VALUES (1, 'ra4eva', 'ra4ever@duke.edu', 'hello_password', 1)")

    cur.execute("INSERT INTO Trips VALUES(0, 0, 'to internship')")
    cur.execute("INSERT INTO Trips VALUES(1, 1, 'graduation')")
    cur.execute("INSERT INTO Trips VALUES(2, 0, 'from internship')")

    cur.execute("INSERT INTO Flights VALUES(3, 2, 'AS', 0922, 'SEA', 'BWI', '20190727 08:00:00 AM', '20190727 4:15:00 PM', 315, 2335)")
    cur.execute("INSERT INTO Flights VALUES(2, 1, 'DL', 2220, 'IAD', 'SEA', '20190609 05:00:00 PM', '20190609 07:39:00 PM', 339, 2306)")
    cur.execute("INSERT INTO Flights VALUES(1, 1, 'DL', 2680, 'SEA', 'IAD', '20190605 10:45:00 PM', '20190606 06:07:00 AM', 339, 2306)")
    cur.execute("INSERT INTO Flights VALUES(0, 0, 'DL', 1253, 'RDU', 'SEA', '20190505 07:25:00 AM', '20190505 10:13:00 AM', 348, 2355)")

    cur.execute("INSERT INTO Details VALUES(1, 1, 'IAD', 'Best place to get boba is TeaDM')")
    cur.execute("INSERT INTO Details VALUES(0, 1, 'IAD', 'Lots of cool museums to go to!')")


    cur.execute("INSERT INTO Airlines VALUES ('AS', 'Alaska Airlines')")
    cur.execute("INSERT INTO Airports VALUES ('BWI','Baltimore/Washington International Thurgood Marshall Airport','Baltimore','United States',39.1754,-76.668297,'America/New_York','A')")
    cur.execute("INSERT INTO Airports VALUES ('SEA','Seattle Tacoma International Airport','Seattle','United States',47.449001,-122.308998,'America/Los_Angeles','A')")

    con.commit()
    cur.close()
