# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, session, redirect, url_for
import shelve
app = Flask(__name__)

app.secret_key = "whatever"

@app.route('/login', methods = ['POST'])
def login():
    user = request.form['user']
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
    return render_template('profile.html', username=username, name=name, surname=surname)

@app.route('/change_info', methods = ['GET','POST'])
def change_info():
    if request.method == 'GET':
        database = shelve.open('users')
        name = database[session['user']]['name']
        surname = database[session['user']]['surname']
        database.close()
        return render_template('change_info.html', username=session['user'], name=name, surname=surname)
    else:
        username = request.form['newusername']
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

@app.route('/lorem', methods = ['GET', 'POST'])
def lorem():
    if request.method == 'POST':
        if 'user' in session:
            return logout()
        else:
            return login()
    else:
        if 'user' in session:
            return render_template('lorem.html', username=session['user'],\
                last1=session['lastpages'][2], last2=session['lastpages'][1],\
                last3=session['lastpages'][0])
        else:
            return render_template('lorem.html', username=None)

@app.errorhandler(404)
def page_not_found(error):
    return "Page not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
