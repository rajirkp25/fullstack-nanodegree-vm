from flask import Flask, request, redirect, url_for, flash, jsonify, Session
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from flask import session as login_session, make_response
from flask.templating import render_template
from database_setup import Category, CategoryItem, User, Base
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import json
import string
import random
import httplib2
import requests

app = Flask(__name__)

APPLICATION_NAME = "Catalog Application"
# Connect to Database and create database session
engine = create_engine('sqlite:///bookcats.db',
                       connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
db_session = DBSession()

app.secret_key = 'secret_key'


@app.route('/test')
def renderTest():
        return render_template('test.html')  


@app.route('/')
def defaultPage():

    print('Home Page --')
    # return 'test'
    return render_template('home.html')


@app.route('/login')
def showLogin():
    '''Create anti-forgery state token'''
    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


# show all categories
@app.route('/catalog/')
def showCatalogs():
        username = request.cookies.get('catusername')
        useremail = request.cookies.get('catuseremail')
        print("user name -->", username)
        print("user useremail -->", useremail)
        
        cats = db_session.query(Category).order_by(asc(Category.name))
        return render_template('cats.html', categories=cats)


def getUserInfo(user_id):
    user = db_session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = db_session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    db_session.add(newUser)
    db_session.commit()
    user = db_session.query(User).filter_by(email=login_session['email']).one()
    return user.id


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
