import math
from itertools import cycle

class SecretMessageSender:
   def __init__(self, other_host):
      self.host = other_host
      self.state = 'before'
      self.the_message = 'this is ultra mega giga top secret message'

   def receive_handshake(self, first_x, second_x, first_y, second_y):
      self.x = first_x + second_x
      self.y = first_y + second_y
      self.state = 'after_handshake'   
      self.secret = math.pow(self.x + self.y, 3) * math.pow(20 - self.x - self.y, 2)

   def receive_secret(self, encrypted):
      decrypted = SecretMessageSender.xor(encrypted, self.secret)
      return decrypted

   def xor(data: str, key):
      xored = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in zip(data, cycle(str(key))))
      return xored