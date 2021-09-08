import random
import requests
import json
import math
from itertools import cycle

class SecretMessageSender:
   def __init__(self, other_host):
      self.host = other_host
      self.state = 'before'
      self.the_message = 'this is ultra mega giga top secret message'

   def send_handshake(self):
      x = random.randint(1, 9)
      first = int(3 ** x)
      second = int(2 ** (10 - x))
      
      self.x = first + second
      
      query = {'first':first, 'second':second }
      
      response = requests.get(self.host + "/handshake", params = query)
      responseJson = json.loads(response.text)

      self.y = responseJson['first'] + responseJson['second']

      self.state = 'after_handshake'   

      self.secret = math.pow(self.x + self.y, 3) * math.pow(20 - self.x - self.y, 2)

   def send_secret(self):
      body = {'secret': SecretMessageSender.xor(self.the_message, str(self.secret), encode = True).decode() }
      response = requests.post(self.host + "/secret", json = body)
      print('sent secret...')
      self.state = 'after_secret' 

      return response

   def receive_secret(self, encrypted):
      return SecretMessageSender.xor(encrypted, self.secret)

   def xor(data: str, key, encode = False):
      xored = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in zip(data, cycle(key)))
      
      if encode:
         encoded = xored.encode('utf-8').strip()
         return encoded
      return xored