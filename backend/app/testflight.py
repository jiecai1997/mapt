from flask import render_template, flash, redirect, url_for, session, request
from flask_login import login_user, current_user, logout_user, login_required
import sqlite3 as sql
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
import math
from datetime import datetime



with sql.connect("app.db") as con:
    con.row_factory = sql.Row
    cur = con.cursor()

    tid = cur.execute("INSERT INTO trip (uid, trip_name,color) VALUES (1,'1','blue')")
    tid = tid.lastrowid
    print(tid)
    con.commit()
    cur.close()
