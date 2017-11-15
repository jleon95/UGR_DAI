# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, session, redirect, url_for
import shelve
import pymongo as pym
import json
app = Flask(__name__)

app.secret_key = "whatever"

@app.route('/login', methods = ['POST'])
def login():
    user = request.form['user']
    print(user)
    with shelve.open('users') as database:
        if user in database:
            session['user'] = user
            session['lastpages'] = []
            session['lastpages'].append('/')
            session['lastpages'].append('/')
            session['lastpages'].append('/')
            session.modified = True
    return redirect(url_for('index'))

@app.route('/logout', methods = ['POST'])
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/register', methods = ['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', username=None)
    else:
        username = request.form['newusername']
        name = request.form['newname']
        surname = request.form['newsurname']
        with shelve.open('users') as database:
            if username not in database:
                database[username] = {'name': name, 'surname': surname}
        return redirect(url_for('index'))

@app.route('/profile', methods = ['GET'])
def profile():
    username = session['user']
    database = shelve.open('users')
    name = database[username]['name']
    surname = database[username]['surname']
    database.close()
    return render_template('profile.html', username=username, name=name, surname=surname, \
        last1=session['lastpages'][2], last2=session['lastpages'][1],\
        last3=session['lastpages'][0])

@app.route('/change_info', methods = ['GET','POST'])
def change_info():
    if request.method == 'GET':
        database = shelve.open('users')
        name = database[session['user']]['name']
        surname = database[session['user']]['surname']
        database.close()
        return render_template('change_info.html', username=session['user'], name=name, surname=surname, \
            last1=session['lastpages'][2], last2=session['lastpages'][1],\
            last3=session['lastpages'][0])
    else:
        username = session['user']
        name = request.form['newname']
        surname = request.form['newsurname']
        with shelve.open('users') as database:
            database[username] = {'name': name, 'surname': surname}
        return redirect(url_for('change_info'))

@app.after_request
def store_visited_url(response):
    if 'lastpages' in session and response.mimetype == 'text/html':
        session['lastpages'].pop(0)
        session['lastpages'].append(request.url)
        session.modified = True
    return response

@app.route('/', methods = ['GET','POST'])
def index():
    if request.method == 'POST':
        if 'user' in session:
            return logout()
        else:
            return login()
    else:
        if 'user' in session:
            return render_template('index.html', username=session['user'],\
                last1=session['lastpages'][2], last2=session['lastpages'][1],\
                last3=session['lastpages'][0])
        else:
            return render_template('index.html', username=None)

@app.route('/ai', methods = ['GET', 'POST'])
def ai():
    if request.method == 'POST':
        if 'user' in session:
            return logout()
        else:
            return login()
    else:
        if 'user' in session:
            return render_template('ai.html', username=session['user'],\
                last1=session['lastpages'][2], last2=session['lastpages'][1],\
                last3=session['lastpages'][0])
        else:
            return render_template('ai.html', username=None)

# {'_id': ObjectId('5a01e121f516a44e1875e163'),
# 'address': {'street': '1St Ave', 'coord': [-73.985174, 40.727336], 'building': '130', 'zipcode': '10009'},
# 'cuisine': 'Bakery',
# 'grades': [{'date': datetime.datetime(2015, 1, 20, 0, 0), 'grade': 'Not Yet Graded', 'score': 0}],
# 'restaurant_id': '50018399',
# 'borough': 'Manhattan',
# 'name': 'Sweet  Generation'}

@app.route('/restaurant_search', methods = ['GET'])
def restaurant_search():
    restaurants = []
    field = request.args.get('field_name',type=str)
    keywords = request.args.get('keywords',type=str)
    if not field is None:
        client = pym.MongoClient()
        collection = client.database.restaurants
        restaurants = list(collection.find({field: keywords},{'address': 1, \
                'cuisine': 1, 'borough': 1, 'name': 1, '_id': 0}))[:20]
    if 'user' in session:
        return render_template('restaurant_search.html', username=session['user'],\
            restaurants=restaurants)
    else:
        return render_template('restaurant_search.html', username=None,\
            restaurants=restaurants)

    return render_template('restaurant_search.html', username=session['user'])

@app.route('/get_page')
def get_page():
    field = request.args.get('field',type=str)
    keywords = request.args.get('keywords',type=str)
    if "+" in keywords:
        keywords = keywords.split("+")
        keywords = " ".join(keywords)
    number = request.args.get('number',type=int)
    client = pym.MongoClient()
    collection = client.database.restaurants
    restaurants = list(collection.find({field: keywords},{'address': 1, \
            'cuisine': 1, 'borough': 1, 'name': 1, '_id': 0}))[(number-1)*20:number*20]
    return json.dumps(restaurants,ensure_ascii=False)

@app.route('/get_number_of_pages')
def get_number_of_pages():
    field = request.args.get('field',type=str)
    keywords = request.args.get('keywords',type=str)
    number = request.args.get('number',type=int)
    client = pym.MongoClient()
    collection = client.database.restaurants
    number = collection.count({field: keywords})
    return str(number)

@app.errorhandler(404)
def page_not_found(error):
    return "Page not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
