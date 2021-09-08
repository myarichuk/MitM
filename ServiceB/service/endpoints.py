"""
Bob
"""
import os
from service import app
from flask import request
import random
from shared import SecretMessageSender

IS_IN_DOCKER = os.environ.get('IN_DOCKER_CONTAINER', False)

if IS_IN_DOCKER:
    messageSender = SecretMessageSender('http://service_a:5555')
else:
    messageSender = SecretMessageSender('http://localhost:5555')

verySecretSecret = "" 

@app.route('/')
def hello():
    return "<h1>Hello World! (from Bob)</h1>"

@app.route('/secret', methods=['POST'])
def secret():
    json = request.get_json()
    verySecretSecret = messageSender.receive_secret(json['secret'])
    print(verySecretSecret)
    return { 'decodedSecret': verySecretSecret }

@app.route('/get_secret')
def fetch_secret():
    return verySecretSecret

@app.route('/handshake')
def handshake():
    first_x = int(request.args.get('first'))
    second_x = int(request.args.get('second'))

    y = random.randint(1,9)
    first = 3 ** y
    second = 2 ** (10 - y)
    
    messageSender.receive_handshake(first_x, second_x, first, second)

    return {'first':first, 'second':second }

    