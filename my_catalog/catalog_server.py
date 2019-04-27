from flask import Flask, request, redirect, url_for, flash, jsonify, Session
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from flask import session as login_session, make_response
from flask.templating import render_template
from database_setup import Category, CategoryItem, User, Base
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError, OAuth2WebServerFlow
import json
import string
import random
import httplib2
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

CLIENT_SEC = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_secret']

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
@app.route('/home')
def defaultPage():
     '''Create anti-forgery state token'''
     user_name = login_session.get('username')
     print("user_name--", user_name)
     if user_name is None:
                state = ''.join(
                        random.choice(string.ascii_uppercase + string.digits) for x in range(32))
                login_session['state'] = state
                print("state --", state)
                print('Home Page --')
                # return 'test'
                return render_template('home.html', STATE=state)
     else:
             return render_template('cats.html')


@app.route('/gdisconnect')
def gdisconnect():
        print ("in gdisconnect")  
     # Only disconnect when a user is connected to app
        access_token = login_session.get('access_token')
        print(access_token)
        if access_token is None:
                login_session.clear()
                response = make_response(
                json.dumps('Current user not connected.'), 401)
                response.headers['Content-Type'] = 'application/json'
                return redirect('/')
        url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
        h = httplib2.Http()
        result = h.request(url, 'GET')[0]
        login_session.clear()
        return redirect('/')

        if result['status'] != '200':
                # hmmm wierd reason, the given token was invalid, woa security invasive
                print ("in token invalid") 
                response = make_response(
                json.dumps('Failed to revoke token for given user.'), 400)
                response.headers['Content-Type'] = 'application/json'
                return response


@app.route('/gconnect')
def gconnect():
        print ("in gconnect")
        # if user not in session then force login
        # Validate state token
        if 'code' not in request.args:
                if request.args.get('state') != login_session['state']:
                        response = make_response(json.dumps('Invalid state parameter.'), 401)
                        response.headers['Content-Type'] = 'application/json'
                        return response
                flow = flow_from_clientsecrets('client_secrets.json',
                           # client_secret='CLIENT_SEC',
                           scope='https://www.googleapis.com/auth/userinfo.email',
                           redirect_uri='http://localhost:5000/gconnect')               
        
        try:
                # Upgrade the authorization code into a credentials object
               # oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
               # flow = OAuth2WebServerFlow(client_id=CLIENT_ID,
                flow = flow_from_clientsecrets('client_secrets.json',
                           # client_secret='CLIENT_SEC',
                           scope='https://www.googleapis.com/auth/userinfo.email',
                           redirect_uri='http://localhost:5000/gconnect') 
                print("oauth flow--->", flow)
                # oauth_flow.redirect_uri = 'postmessage'
                auth_uri = flow.step1_get_authorize_url()
                if 'code' not in request.args:
                        print('code not in args')
                        auth_uri = flow.step1_get_authorize_url()
                        return redirect(auth_uri)
                else:
                        print('code in args')
                        auth_code = request.args.get('code')
                        print('getting creds...', auth_code)
                        credentials = flow.step2_exchange(auth_code)
                        # session['credentials'] = credentials.to_json()
                # code = request.args.get('code')
                print("auth_uri-->", auth_uri)
                print("code -->", auth_code)
                # credentials = flow.step2_exchange(code)
        except FlowExchangeError as e:
                response = make_response(
                json.dumps('Failed to upgrade the authorization code.' + format(str(e))), 401)
                response.headers['Content-Type'] = 'application/json'
                return response
        # Check that the access token is valid.
        access_token = credentials.access_token
        print("access_token ", access_token)
        url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
                % access_token)
        h = httplib2.Http()
        result = json.loads(h.request(url, 'GET')[1])
        # If there was an error in the access token info, abort.
        if result.get('error') is not None:
                response = make_response(json.dumps(result.get('error')), 500)
                response.headers['Content-Type'] = 'application/json'
                return response
            # Get user info
        userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        params = {'access_token': credentials.access_token, 'alt': 'json'}
        answer = requests.get(userinfo_url, params=params)

        data = answer.json()
        print("data ", data)

        login_session['id'] = data['id']
        login_session['email'] = data['email']
        login_session['picture'] = data['picture']
        login_session['username'] = data['email']

        print("login_session['name'] ", login_session['username'])

        # chk if user already exists in db

        user_id = getUserID(data['email'])
        if not user_id:
                user_id = createUser(login_session)
        login_session['user_id'] = user_id

        return render_template('cats.html')


# create user if doesnt exist
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], avatar=login_session['picture'], active=True, tokens=login_session['id'])
    db_session.add(newUser)
    db_session.commit()
    user = db_session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = db_session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = db_session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# show all categories
@app.route('/catalog/')
def showCatalogs():

        print("res ", request.values.get('res'))
        print("cat_id ", request.values.get('cat_id'))
       # print("user email in sowCatalogs ", login_session['email'])
        # if request.args.get('res') == True:
         #       print("Confirm delete, delete the catalog", request.args.get('cat_id'))
        cats = db_session.query(Category).order_by(asc(Category.name))
        return render_template('catalogs.html', categories=cats)


@app.route('/catalog/new/', methods=['GET', 'POST'])
def newCatalog():
    tile_color_list = ['bg-secondary', 'bg-primary', 'bg-success', 'bg-danger', 'bg-warning', 'bg-info', 'bg-dark']
    if request.method == 'POST':
            # add user info with catalog
        newCat = Category(name=request.form['catName'], description=request.form['catDescr'],
        tile=random.choice(tile_color_list))
        db_session.add(newCat)
        flash('New Book Category %s Successfully Created' % newCat.name)
       
        db_session.commit()
        return redirect(url_for('showCatalogs'))
    else:
        return render_template('newCatalog.html')


# edit a catalog
@app.route('/catalog/<int:cat_id>/edit/', methods=['GET', 'POST'])
def editCatalog(cat_id):
    print("editing catalog id %s", cat_id)
    editedCatalog = db_session.query(
        Category).filter_by(cat_id=cat_id).one()
    if request.method == 'POST':
        if request.form['catDescr']:
            editedCatalog.description = request.form['catDescr']
        
        db_session.add(editedCatalog)
        db_session.commit()  
      
        flash('Catalog Successfully Edited %s' % editedCatalog.name)
        return redirect(url_for('showCatalogs'))
    else:
        print("editing catalog name = ", editedCatalog.name)
        return render_template('editCatalog.html', category=editedCatalog)


# delete a catalog
@app.route('/catalog/<int:cat_id>/delete/', methods=['GET', 'POST'])
def deleteCatalog(cat_id):
    
    delCatalog = db_session.query(
        Category).filter_by(cat_id=cat_id).one()
    if request.method == 'POST':
        print("deleting catalog id %s", cat_id)    
        db_session.delete(delCatalog)
        db_session.commit()  
      
        flash('Catalog Successfully deleted %s' % delCatalog.name)
        return redirect(url_for('showCatalogs'))
    else:
        print("deleting catalog name = ", delCatalog.name)
        return render_template('deleteCatalog.html', cat=delCatalog)

 
# Json APIs to view catalogs
@app.route('/catalog/JSON')
def catalogsJSON():
    categories = db_session.query(Category).all()
    return jsonify(categories=[c.serialize for c in categories])


# show all catalog items
@app.route('/catalog/<int:cat_id>/')
def showCatalogItems(cat_id):

        print("cat id in showCatalogItems ", cat_id)
        cats = db_session.query(Category).filter_by(cat_id=cat_id).one()
        items = db_session.query(CategoryItem).filter_by(
        cat_id=cat_id).order_by(asc(CategoryItem.name))
        for i in items:
                print("book--> " , i , " " , i.name)
        return render_template('catalogItems.html', items=items, cats=cats)


# Add new Book
@app.route('/book/new/<int:cat_id>/', methods=['GET', 'POST'])
def newBook(cat_id):
    print('Adding new book in cat id %s' % cat_id)
    cats = db_session.query(Category).filter_by(cat_id=cat_id).one()
    if request.method == 'POST':
        print(request.form['name'])
        print(request.form['descr'])
        print(request.form['price'])
        print(request.form['author'])
        newBook = CategoryItem(cat_id=cat_id, name=request.form['name'], description=request.form['descr'], price=request.form['price'], author=request.form['author'])
        db_session.add(newBook)
        flash('New Book Category %s Successfully Created' % newBook.name)
       
        db_session.commit()
        return redirect(url_for('showCatalogItems', cat_id=cat_id))
    else:
        return render_template('newBook.html', cat_id=cat_id)


# edit a catalog item
@app.route('/catalog/<int:cat_id>/<int:item_id>/edit/', methods=['GET', 'POST'])
def editCatalogItem(cat_id, item_id):
    print("editing item id -->", item_id)
    # cats = db_session.query(Category).filter_by(cat_id=cat_id).one()
   
    editedCatalogItem = db_session.query(
        CategoryItem).filter_by(item_id=item_id).one()
    
    if request.method == 'POST':
        if request.form['ItemDescr']:
            editedCatalogItem.description = request.form['ItemDescr']
        if request.form['itemPrice']:
            editedCatalogItem.price = request.form['itemPrice']
        if request.form['itemRank']:
            editedCatalogItem.best_seller_rank = request.form['itemRank'] 
        
        db_session.add(editedCatalogItem)
        db_session.commit()  
        name = editedCatalogItem.name
        flash('Item Successfully Edited %s' % name)
        return redirect(url_for('showCatalogItems', cat_id=cat_id))
    else:
        print("editing item name = ", editedCatalogItem.name)
        return render_template('editItem.html', item=editedCatalogItem)


# delete a catalog item
@app.route('/catalog/<int:cat_id>/<int:item_id>/delete/', methods=['GET', 'POST'])
def deleteCatalogItem(cat_id, item_id):
    
    delCatalogItem = db_session.query(
        CategoryItem).filter_by(item_id=item_id).one()
    if request.method == 'POST':
        print("deleting item id %s", item_id)    
        db_session.delete(delCatalogItem)
        db_session.commit()  
      
        flash('Catalog Successfully deleted %s' % delCatalogItem.name)
        return redirect(url_for('showCatalogItems', cat_id=cat_id))
    else:
        print("deleting catalog name = ", delCatalogItem.name)
        return render_template('deleteCatalogItem.html',  item=delCatalogItem)


@app.route('/catalog/<int:cat_id>/books/JSON')
def catlogItemsJSON(cat_id):
    cats = db_session.query(Category).filter_by(cat_id=cat_id).one()
    items = db_session.query(CategoryItem).filter_by(
        cat_id=cat_id).all()
    return jsonify(CategoryItem=[i.serialize for i in items])


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
