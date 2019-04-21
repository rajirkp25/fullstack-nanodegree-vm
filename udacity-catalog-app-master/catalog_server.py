from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base

# New imports for this step
from flask import session as login_session
import random
import string

app = Flask("Udacity Ctaalog Application")

# Connect to Database and create database session
engine = create_engine('sqlite:///catalog.db',
                       connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=32))
    login_session['state'] = state
    return "The current session state is %s" % login_session['state']

