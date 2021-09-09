from mitmproxy import ctx, http
import json
from itertools import cycle

class KeyComponents:
    def __init__(self) -> None:
        self.first: int = 0
        self.second: int = 0
        self.third: int = 0
        self.fourth: int = 0

keyChangeSessions: dict = dict()

def response(flow: http.HTTPFlow) -> None:
    def xor_string(msg: str, secret: int):
        return ''.join(chr(ord(x) ^ ord(y)) for (x,y) in zip(msg, cycle(str(secret))))

    if (flow.request.path.startswith('/handshake') and 
        flow.response.status_code == 200 and 
        'session' in flow.response.cookies):
            kparams = KeyComponents()
            kparams.first = int(flow.request.query['first'])
            kparams.second = int(flow.request.query['second'])
            responseParams = json.loads(flow.response.get_text())
            kparams.third = responseParams[0]
            kparams.fourth = responseParams[1]
            sessionId = flow.response.cookies['session'][0]
            ctx.log.info(sessionId + ' --> ' + flow.request.query['first'] + ',' + flow.request.query['second'] + ',' + str(responseParams[0]) + ',' + str(responseParams[1]))
            keyChangeSessions[sessionId] = kparams

    if (flow.request.path.startswith('/secret') and
        'session' in flow.request.cookies and 
        flow.request.cookies['session'] in keyChangeSessions):
            sessionId = flow.request.cookies['session']
            secret = json.loads(flow.request.get_text())['secret']
            ctx.log.info(sessionId + ' --> ' + 'encrypted secret: ' + secret)
            kparams = keyChangeSessions[sessionId]
            key = kparams.first * kparams.second * kparams.third * kparams.fourth
            ctx.log.info(sessionId + ' --> ' + 'decrypted secret:' + xor_string(secret, key))