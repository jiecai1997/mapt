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

    airline_csv = './app/csv/Airlines.csv'
    with open(airline_csv) as file_handler:
        csv = [row for row in reader(file_handler) if any(row)]
        for c in csv:
            cur.execute("INSERT INTO airlines (iata, name) VALUES (?,?)",(c[1], c[0]))

    airports_csv = './app/csv/Airports.csv'
    with open(airports_csv) as file_handler:
        csv = [row for row in reader(file_handler) if any(row)]
        headers = csv.pop(0)
        for c in csv:
            cur.execute("INSERT INTO airports (iata, name, city, country, latitude, longitude, time_zone, dst) VALUES (?,?,?,?,?,?,?,?)",(c[0], c[1], c[2], c[3], c[4], c[5], c[9], c[8]))

    con.commit()
    cur.close()
