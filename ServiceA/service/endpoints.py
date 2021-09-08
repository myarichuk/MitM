"""
Alice
"""
import os
from service import app
from helper import SecretMessageSender
import configparser

IS_IN_DOCKER = os.environ.get('IN_DOCKER_CONTAINER', False)

config = configparser.ConfigParser()
config.read('serviceConfig.ini')

if IS_IN_DOCKER:
    messageSender = SecretMessageSender(config['otherService']['dockerUrl'])
else:
    messageSender = SecretMessageSender(config['otherService']['dockerUrl'])

@app.route('/')
def hello():
    return "<h1>Hello World! (from Alice)</h1>"

@app.route('/handshake')
def handshake():
    messageSender.send_handshake()
    response = messageSender.send_secret()
    return { 'secret': messageSender.secret, 'response': response.json() }