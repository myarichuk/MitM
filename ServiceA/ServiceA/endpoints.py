"""
Routes and views for the flask application.
"""

from ServiceA import app

@app.route('/')
def hello():
    return "<h1>Hello World!</h1>"