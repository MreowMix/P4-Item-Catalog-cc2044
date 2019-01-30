#!/usr/bin/env python

from flask import Flask, render_template, request
from flask import redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Brand, Snowboard, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Snowboard Brands Application"

engine = create_engine('sqlite:///brandsnowboard.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


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

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
                                'Current user is already connected.'), 200)
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

    # see if user exists, if it doesn't make a new one
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
    output += ' " style = "width: 300px; height: 300px;'
    output += 'border-radius: 150px;-webkit-border-radius: 150px;'
    output += '-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# JSON ENDPOINT
@app.route('/brands/<int:brand_id>/JSON')
def brandJSON(brand_id):
    brand = session.query(Brand).filter_by(id=brand_id).one()
    snowboard = session.query(Snowboard).filter_by(brand_id=brand_id).all()
    return jsonify(Snowboard=[i.serialize for i in snowboard])


@app.route('/brands/<int:brand_id>/snowboard/<int:snowboard_id>/JSON')
def snowboardJSON(brand_id, snowboard_id):
    snowboard = session.query(Snowboard).filter_by(id=snowboard_id).one()
    return jsonify(Snowboard=snowboard.serialize)


# Returns a list of all snowboard brands
@app.route('/')
@app.route('/brands')
def showAllBrands():
    brand = session.query(Brand).all()
    return render_template('main.html', brand=brand)


# Returns all snowboards for the particular brand
@app.route('/brands/<int:brand_id>/snowboard')
def showSnowboard(brand_id):
    brand = session.query(Brand).filter_by(id=brand_id).one()
    snowboard = session.query(Snowboard).filter_by(brand_id=brand_id)
    return render_template('snowboard.html', brand=brand,
                           snowboard=snowboard, brand_id=brand_id)


# Create new snowboard for the particular brand
@app.route('/brands/<int:brand_id>/snowboard/new', methods=['GET', 'POST'])
def newSnowboard(brand_id):
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newSnowboard = Snowboard(
            name=request.form['name'],
            style=request.form['style'],
            brand_id=brand_id,
            user_id=login_session['user_id'])
        session.add(newSnowboard)
        session.commit()
        flash("New Snowboard created!")
        return redirect(url_for('showSnowboard', brand_id=brand_id))
    else:
        return render_template('newSnowboard.html', brand_id=brand_id)


# Edit existing snowboard for the particular brand
@app.route('/brands/<int:brand_id>/snowboard/<int:snowboard_id>/edit',
           methods=['GET', 'POST'])
def editSnowboard(brand_id, snowboard_id):
    editedItem = session.query(Snowboard).filter_by(id=snowboard_id).one()
    creator = getUserInfo(editedItem.user_id)
    user = getUserInfo(login_session['user_id'])
    if creator.id != login_session['user_id']:
        flash("You cannot edit this Snowboard. " +
              "This belongs to %s" % creator.name)
        return redirect(url_for('showSnowboard', brand_id=brand_id))
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['name']:
            editedItem.style = request.form['style']
        session.add(editedItem)
        session.commit()
        flash("Snowboard has been edited!")
        return redirect(url_for('showSnowboard', brand_id=brand_id))
    else:
        return render_template('editSnowboard.html', brand_id=brand_id,
                               snowboard_id=snowboard_id,
                               snowboard=editedItem)


# Delete existing snowboard for the particular brand
@app.route('/brands/<int:brand_id>/snowboard/<int:snowboard_id>/delete',
           methods=['GET', 'POST'])
def deleteSnowboard(brand_id, snowboard_id):
    itemToDelete = session.query(Snowboard).filter_by(id=snowboard_id).one()
    creator = getUserInfo(itemToDelete.user_id)
    user = getUserInfo(login_session['user_id'])
    if creator.id != login_session['user_id']:
        flash("You cannot edit this Snowboard. " +
              "This belongs to %s" % creator.name)
        return redirect(url_for('showSnowboard', brand_id=brand_id))
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Snowboard has been deleted!")
        return redirect(url_for('showSnowboard', brand_id=brand_id))
    else:
        return render_template('deleteSnowboard.html', brand_id=brand_id,
                               snowboard_id=snowboard_id,
                               snowboard=itemToDelete)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
