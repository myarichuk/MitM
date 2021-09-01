"""
Routes and views for the flask application.
"""

from service import app

@app.route('/')
def hello():
    return "<h1>Hello World (from server B)!</h1>"