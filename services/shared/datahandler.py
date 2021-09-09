import random
from itertools import cycle

class KeyChangeDataHandler:

   def __init__(self):
      self.xor_string = lambda msg, secret: ''.join(chr(ord(x) ^ ord(y)) for (x,y) in zip(msg, cycle(str(secret))))

   def calculate_my(self) -> tuple[int, int]:
      num = random.randint(1, 9)
      self.first = 3 ** num
      self.second = 2 ** (10 - num)
      return self.first, self.second

   def receiveOther(self, otherNumbers: tuple[int, int]) -> None:
      self.third = otherNumbers[0]
      self.fourth = otherNumbers[1]

   def encryptOrDecrypt(self, message: str) -> str:
      secret = self.first * self.second * self.third * self.fourth
      return self.xor_string(message, secret)
   
