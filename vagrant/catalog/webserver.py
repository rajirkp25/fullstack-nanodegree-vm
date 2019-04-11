from flask import Flask, request, redirect, url_for, flash, jsonify, Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask.templating import render_template
import json

app = Flask(__name__)

sess = Session()

APPLICATION_NAME = "Catalog Application"


@app.route('/')
def defaultPage():

    print('Home Page')
    # return 'test'

    return render_template('home.html')


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
