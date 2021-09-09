import json
import random
from itertools import cycle

class KeyChangeDataHandler:
   def __init__(self) -> None:
      self.first = 0
      self.second = 0
      self.third = 0
      self.fourth = 0

   def calculate_my(self) -> tuple[int, int]:
      num = random.randint(1, 9)
      self.first = 3 ** num
      self.second = 2 ** (10 - num)
      return self.first, self.second

   def receiveOther(self, otherNumbers: tuple[int, int]) -> None:
      self.third = otherNumbers[0]
      self.fourth = otherNumbers[1]

   def encryptOrDecrypt(self, message: str) -> str:
      def xor_string(msg: str, secret: int):
         return ''.join(chr(ord(x) ^ ord(y)) for (x,y) in zip(msg, cycle(str(secret))))
         
      secret: int = self.first * self.second * self.third * self.fourth
      return xor_string(message, secret)
   

   def toJson(self) -> str:
      return json.dumps({ 'first': self.first, 'second': self.second, 'third': self.third, 'fourth': self.fourth })

   def fromJson(kcdJson: str):
      newInstance = KeyChangeDataHandler()
      
      newInstance.first = int(kcdJson['first'])
      newInstance.second = int(kcdJson['second'])
      newInstance.third = int(kcdJson['third'])
      newInstance.fourth = int(kcdJson['fourth'])

      return newInstance