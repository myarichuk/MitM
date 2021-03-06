"""
Alice
"""
import os

import configparser
import random

import json
from changeprocess import KeyChangeProcess
from datahandler import KeyChangeDataHandler
from httpCommunicator import HttpChangeCommunicator
from flask_session import Session
from flask import Flask, session, request, make_response


app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

IS_IN_DOCKER = os.environ.get('IN_DOCKER_CONTAINER', False)

config = configparser.ConfigParser()
config.read('config/serviceConfig.ini')

if IS_IN_DOCKER:
    url: str = config['otherService']['dockerUrl']
else:
    url: str = config['otherService']['localUrl']

#url = 'http://localhost:5000'

def storeInstance(kcp: KeyChangeProcess):
    session['first'] = kcp.dataHandler.first
    session['second'] = kcp.dataHandler.second
    session['third'] = kcp.dataHandler.third
    session['fourth'] = kcp.dataHandler.fourth
    session['initialized'] = True
    return kcp

def getKeyChangeProcess():
    def getNewInstance(otherUrl: str) -> KeyChangeProcess:
        return KeyChangeProcess(HttpChangeCommunicator(otherUrl))

    if 'initialized' not in session:
        return storeInstance(getNewInstance(url))

    instance = KeyChangeProcess(HttpChangeCommunicator(url))
    instance.dataHandler = KeyChangeDataHandler.fromJson({ 'first': session['first'], 'second': session['second'], 'third': session['third'], 'fourth': session['fourth'] })

    return instance

@app.route('/')
def hello():
    return "<h1>Hello World! (from Alice)</h1>"


@app.route('/changekey')
def changekey():
    newKey: str = request.args.get('newkey')

    # just in case...
    if newKey is None or '':
        newKey = random.randint(5, 10000)
    keyChangeProcess = getKeyChangeProcess()
    keyChangeProcess.doKeyChange(newKey)
    storeInstance(keyChangeProcess)
    session['secret'] = newKey
    return json.dumps({ 'message': 'OK'})


@app.route('/handshake', methods=['PUT'])
def handshake():
    first = int(request.args.get('first'))
    second = int(request.args.get('second'))
    keyChangeProcess = getKeyChangeProcess()
    my = keyChangeProcess.continueChangeKey((first, second))
    storeInstance(keyChangeProcess)
    return json.dumps(my)


@app.route('/secret', methods=['POST'])
def secret():
    newKey = request.get_json()['secret']
    getKeyChangeProcess().receiveNewKey(newKey)
    session['secret'] = newKey
    return { 'message': 'OK' }