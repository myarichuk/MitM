from __future__ import annotations
from datahandler import KeyChangeDataHandler
from abc import ABC, abstractmethod

class KeyChangeCommunicator(ABC):
   @abstractmethod
   def sendNumbers(self, myNumbers: tuple[int, int]) -> tuple[int, int]:
      pass
 
   @abstractmethod
   def sendSecret(self, secret: str) ->  None:
      pass

class KeyChangeProcess:
   def __init__(self, communicator: KeyChangeCommunicator):
      self.dataHandler = KeyChangeDataHandler()
      self.communicator = communicator
   
   def doKeyChange(self, newKey: str) -> None:
      my = self.dataHandler.calculate_my()
      other = self.communicator.sendNumbers(my)
      self.dataHandler.receiveOther(other)
      self.communicator.sendSecret(self.dataHandler.encryptOrDecrypt(newKey))
   
   def continueChangeKey(self, otherNumber: tuple[int, int]) -> tuple[int, int]:
      self.dataHandler.receiveOther(otherNumber)      
      my = self.dataHandler.calculate_my()
      return my

   def receiveNewKey(self, encryptedKey: str) -> str:
      self.newKey = self.dataHandler.encryptOrDecrypt(encryptedKey)
      return self.newKey