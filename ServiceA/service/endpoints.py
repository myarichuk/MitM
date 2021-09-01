"""
Routes and views for the flask application.
"""

from service import app

@app.route('/')
def hello():
    return "<h1>Hello World (from server A)!</h1>"

@app.route('/call_b')
def call_b():
    return "<h1>Hello World!</h1>"    