from changeprocess import KeyChangeCommunicator
import requests
import json

class HttpChangeCommunicator(KeyChangeCommunicator):
   def __init__(self, url: str) -> None:
       super().__init__()
       self.url = url
 
   def sendNumbers(self, myNumbers: tuple[int, int]) -> tuple[int, int]:
      myNumbers = {'first':myNumbers[0], 'second':myNumbers[1] }      
      response = requests.put(self.host + "/handshake", params = myNumbers)
      responseJson = json.loads(response.text)

      return int(responseJson['first']), int(responseJson['second'])
 
   def sendSecret(self, encryptedSecret: str) ->  None:
      requests.post(self.host + "/secret", json = { 'secret': encryptedSecret })