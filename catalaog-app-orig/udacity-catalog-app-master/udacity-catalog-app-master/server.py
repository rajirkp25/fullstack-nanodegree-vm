from flask import Flask, Session, render_template, request, redirect, jsonify, url_for, flash, send_from_directory
#from flask.ext.session import Session
#from sqlalchemy import create_engine, asc
#from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from database_setup import Category, CategoryItem, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
import urllib2
from functools import wraps

app = Flask(__name__)

sess = Session()

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog App"


# Connect to Database and create database session
#engine = create_engine('sqlite:///catalog.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///catalog.db'
db = SQLAlchemy(app)

app.secret_key = 'super_secret_key'

#Base.metadata.bind = engine

#DBSession = sessionmaker(bind=engine)
#session = DBSession()


@app.route('/login')
def showLogin():
    '''Create anti-forgery state token'''
    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]


    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout, let's strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ''' " style = "width: 300px; height: 300px;
    border-radius: 150px;-webkit-border-radius: 150px;
    -moz-border-radius: 150px;"> '''

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ''' " style = "width: 300px; height: 300px;
    border-radius: 150px;-webkit-border-radius: 150px;
    -moz-border-radius: 150px;"> '''
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    db.session.add(newUser)
    db.session.commit()
    user = db.session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = db.session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = db.session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in login_session:
            return f(*args, **kwargs)
        else:
            flash("You are not allowed to access there")
            return redirect('/login')
    return decorated_function

@app.route('/gdisconnect')
def gdisconnect():
    '''
    DISCONNECT - Revoke a current user's token and reset
    their login_session
    '''
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    print(access_token)
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    login_session.clear()
    return redirect('/catalog')

    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response

@app.route('/catalog.json')
def sendCatalogJSON():
    '''
    Send Catalog Data as JSON
    '''
    categories = []
    for c in db.session.query(Category).order_by(db.asc(Category.id)):
        items = db.session.query(CategoryItem).filter_by(category_id=c.id)
        category = {
            "id": c.id,
            "name": c.name,
            "items": [i.serialize for i in items]
        }
        categories.append(category)

    return jsonify(Categories=categories)

@app.route('/catalog/<string:item_name>.json')
def sendItemJSON(item_name):
    '''
    Send Item Data as JSON
    '''
    item = db.session.query(CategoryItem).filter_by(name=item_name).one()
    return jsonify(Item=item.serialize)

@app.route('/')
@app.route('/catalog/')
def showCategories():
    '''
    Display All Categories (Sidebar) and Latest Items (Main)
    Logged In: Add
    '''
    categories = db.session.query(Category).order_by(db.asc(Category.id))
    latest_items = db.session.query(CategoryItem)
    
    return render_template('categories.html', categories=categories, latest_items=latest_items)


@app.route('/catalog/<string:category_name>/items')
def showCategory(category_name):
    '''
    Display All Categories (Sidebar) and Category Items (Main)
    Logged In: Edit, Delete
    '''
    categories = db.session.query(Category).order_by(db.asc(Category.id))
    category = db.session.query(Category).filter_by(name=urllib2.unquote(category_name)).one()
    items = db.session.query(CategoryItem).filter_by(category_id=category.id)
    return render_template('category_item_list.html',
        categories=categories, items=items, category=category)

@app.route('/catalog/<string:category_name>/<string:item_name>')
def showItem(category_name, item_name):
    '''
    Display title and details about this item
    '''
    item = db.session.query(CategoryItem).filter_by(name=item_name).one()
    return render_template('category.html', item=item)

@app.route('/catalog/<string:item_name>/edit', methods=['GET', 'POST'])
@login_required
def editItem(item_name):
    '''
    GET: Display Edit Form
    POST: Update Item
    '''
    item = db.session.query(CategoryItem).filter_by(name=urllib2.unquote(item_name)).one()
    categories = db.session.query(Category)

    if item.user_id != login_session['user_id']:
        return """<script>function myFunction() {
        alert('You are not authorized to edit this item. Please create your own item in order to edit.');}
        </script><body onload='myFunction()''>"""
    
    if request.method == 'POST':
        item.name = request.form.get('name', item.name)
        item.description = request.form.get('description', item.description)
        item.category_id = request.form.get('category_id', item.category_id)

        db.session.add(item)
        db.session.commit()

        category = db.session.query(Category).filter_by(id=item.category_id).one()
        return redirect('/catalog/%s/%s' % (category.name, item.name))
    else:
        return render_template('edit-item.html', item=item, categories=categories)


@app.route('/catalog/<string:item_name>/delete', methods=['GET', 'POST'])
@login_required
def deleteItem(item_name):
    '''
    GET: Display Delete Confirmation Form
    POST: Delete Item
    '''
    item = db.session.query(CategoryItem).filter_by(name=urllib2.unquote(item_name)).one()

    if item.user_id != login_session['user_id']:
        return """<script>function myFunction() {
        alert('You are not authorized to delete this item. Please create your own item in order to delete.');}
        </script><body onload='myFunction()''>"""

    if request.method == 'POST':
        category = db.session.query(Category).filter_by(id=item.category_id).one()

        db.delete(item)
        db.session.commit()

        return redirect('/catalog/%s/items' % category.name)
    else:
        return render_template('delete-item.html', item=item)


@app.route('/catalog/add', methods=['GET', 'POST'])
@login_required
def addItem():
    '''
    GET: Display Add Form
    POST: Create New Item
    '''
    categories = db.session.query(Category)

    if request.method == 'POST':
        name = request.form.get('name', '')
        description = request.form.get('description', '')
        category_id = request.form.get('category_id', '')

        newItem = CategoryItem(name=name, description=description,
            category_id=category_id, user_id=login_session['user_id'])

        db.session.add(newItem)
        db.session.commit()

        return redirect('/catalog/%s/%s' % (newItem.category.name, newItem.name))
    else:
        return render_template('add-item.html', categories=categories)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)



