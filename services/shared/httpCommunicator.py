from changeprocess import KeyChangeCommunicator
import requests
import json

class HttpChangeCommunicator(KeyChangeCommunicator):
   def __init__(self, url: str) -> None:
       super().__init__()
       self.url = url
       self.session = requests.Session() 
 
   def sendNumbers(self, myNumbers: tuple[int, int]) -> tuple[int, int]:
      myNumbers = {'first':myNumbers[0], 'second':myNumbers[1] }      
      response = self.session.put(self.url + "/handshake", params = myNumbers)
      responseJson = json.loads(response.text)

      return int(responseJson[0]), int(responseJson[1])
 
   def sendSecret(self, encryptedSecret: str) ->  None:
      self.session.post(self.url + "/secret", json = { 'secret': encryptedSecret })

   def toJson(self) -> str:
      return json.dumps({ 'url': self.url })

   def fromJson(kccJson: str) -> KeyChangeCommunicator:
      parsed = json.loads(kccJson)
      return HttpChangeCommunicator(str(parsed['url']))