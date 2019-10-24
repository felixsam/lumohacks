from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_googlemaps import GoogleMaps
import sqlite3
import os

app = Flask(__name__)
app.config.from_object(Config)

app.config['static folder'] = os.path.join('static')

conn = sqlite3.connect('students.db')
print("Opened database successfully")


students = {
    ('John','Soccer','Vancouver','Yes'),
    ('Derek','Basketball','Vancouver','No'),
    ('Lily','Football','Vancouver','Yes'),
    ('Josh','Chess','Vancouver','Yes'),
    ('Keving','Knitting','Vancouver','Yes'),
    ('Kim','Reading','Vancouver','No'),
    ('Ryan','Soccer','Vancouver','Yes'),
    ('Henry','Reading','Vancouver','No'),
    ('Brian','Chess','Vancouver','Yes'),
    ('Kelly','Soccer','Vancouver','No')
}


with conn:

    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS students")
    cur.execute('CREATE TABLE students (name TEXT, activity TEXT, city TEXT, online TEXT)')
    cur.executemany("INSERT INTO students VALUES(?,?,?,?)", students)

print("Table created successfully")
conn.close()
print("Connection closed")

db = SQLAlchemy(app)
migrate = Migrate(app, db)
GoogleMaps(app)

from app import routes, models