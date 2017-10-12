# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return '¡Hola Mundo!'

@app.route('/user/<username>')
def user_greeting(username):
    par1 = request.args.get('catname')
    return '''  <!DOCTYPE html>
                <head>
                  <link rel="stylesheet" type="text/css" href="/static/style.css">
                </head>
                <html>
                  <body>
                    <h1>Hello %s!</h1>
                    <p>This is a picture created by merging a cat and another picture
                    with a deep neural network.</p>
                    <p>You named it %s.</p>
                    <img src='/static/deepdreamcat.jpg'>
                  </body>
                </html>
                ''' % (username, par1)

@app.errorhandler(404)
def page_not_found(error):
    return "Page not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
