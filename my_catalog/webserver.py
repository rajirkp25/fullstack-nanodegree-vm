from flask import Flask, request, redirect, url_for, flash, jsonify, Session
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from flask.templating import render_template
from database_setup import Category, CategoryItem, User, Base
import json

app = Flask(__name__)

APPLICATION_NAME = "Catalog Application"
# Connect to Database and create database session
engine = create_engine('sqlite:///bookcats.db',
                       connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/test')
def renderTest():
        return render_template('test.html')  


@app.route('/')
def defaultPage():

    print('Home Page')
    # return 'test'

    return render_template('home.html')


# show all categories
@app.route('/catalog/')
def showCatalogs():
        cats = session.query(Category).order_by(asc(Category.name))
        return render_template('categories.html', categories=cats)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
