from app import app
from flask import render_template, flash, redirect, url_for, session, request
from app.forms import LoginForm
import sqlite3
from gevent import monkey
from flask_socketio import SocketIO, emit, join_room
from functools import wraps
import os

@app.route('/')
@app.route('/index')
def index():
    logo = os.path.join(app.config['static folder'], 'logo.jpg')
    return render_template('index.html', title='Home', logo=logo)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    logo = os.path.join(app.config['static folder'], 'logo.jpg')
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form, logo=logo)


@app.route('/about us')
def about_us():
    logo = os.path.join(app.config['static folder'], 'logo.jpg')
    return render_template('about_us.html', title='About Us', logo=logo)


@app.route('/search_for_a_team')
def search_for_a_team():
    logo = os.path.join(app.config['static folder'], 'logo.jpg')
    soccer = os.path.join(app.config['static folder'], 'soccer.png')
    basketball = os.path.join(app.config['static folder'], 'basketball.png')
    books = os.path.join(app.config['static folder'], 'books.png')
    cards = os.path.join(app.config['static folder'], 'cards.png')
    chess = os.path.join(app.config['static folder'], 'chess.png')
    knitting = os.path.join(app.config['static folder'], 'knitting.png')
    volleyball = os.path.join(app.config['static folder'], 'volleyball.png')
    return render_template('search_for_a_team.html', title='Search For A Team',
                           basketball=basketball, soccer=soccer, books=books, cards=cards, chess=chess,
                           knitting=knitting, volleyball=volleyball, logo=logo)


@app.route('/upcoming_events')
def upcoming_events():
    logo = os.path.join(app.config['static folder'], 'logo.jpg')
    return render_template('upcoming_events.html', title='chat', logo=logo)

@app.route('/geolocation')
def geolocation():
    logo = os.path.join(app.config['static folder'], 'logo.jpg')
    return render_template('geolocation.html', title='geolocation', logo=logo)

@app.route('/list')
def list():
    logo = os.path.join(app.config['static folder'], 'logo.jpg')
    con = sqlite3.connect("students.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("select * from students")

    rows = cur.fetchall()
    return render_template("list.html", rows=rows, logo=logo)

@app.route('/enternew')
def new_student():
    logo = os.path.join(app.config['static folder'], 'logo.jpg')
    return render_template('student.html', logo=logo)


@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         nm = request.form['nm']
         activity = request.form['activity']
         city = request.form['city']
         online = request.form['online']

         with sqlite3.connect("students.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO students (name,activity,city,online)VALUES (?,?,?,?)",(nm,activity,city,online) )

            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"

      finally:
         return render_template("result.html",msg = msg)
         con.close()