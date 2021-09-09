"""
Bob
"""
import os
from controller import app
import configparser
from httpCommunicator import HttpChangeCommunicator
from changeprocess import KeyChangeProcess
from flask import request, make_response
import json
import random

IS_IN_DOCKER = os.environ.get('IN_DOCKER_CONTAINER', False)

config = configparser.ConfigParser()
config.read('serviceConfig.ini')

if IS_IN_DOCKER:
    url: str = 'http://service_a:5555'#config['otherService']['dockerUrl']
else:
    url: str = 'http://localhost:5555'#config['otherService']['dockerUrl']

currentKeyChangeProcess: KeyChangeProcess

@app.route('/')
def hello():
    return "<h1>Hello World! (from Bob)</h1>"

@app.route('/changekey', methods=['GET'])
def changekey():
    currentKeyChangeProcess = KeyChangeProcess(HttpChangeCommunicator(url))
    newKey: str = request.args.get('newkey')
    if(newKey is None): #just in case...
        newKey = random.randint(5, 10000)
    currentKeyChangeProcess.doKeyChange()
    return make_response(json.dump({ 'message': 'OK'}),200)

@app.route('/handshake', methods=['PUT'])
def handshake():
    currentKeyChangeProcess = KeyChangeProcess(HttpChangeCommunicator(url))
    first = int(request.args.get('first'))
    second = int(request.args.get('second'))
    
    return currentKeyChangeProcess.continueChangeKey(first, second)

@app.route('/secret', methods=['POST', 'GET'])
def secret():
    if request.method == 'POST':
        currentKeyChangeProcess.receiveNewKey(request.get_json()['secret'])
    else:
        return make_response(json.dump({ 'secret': currentKeyChangeProcess.newKey }), 200)