from shared.changeprocess import KeyChangeCommunicator, KeyChangeProcess

class MockChangeCommunicator(KeyChangeCommunicator):
   def __init__(self) -> None:
       super().__init__()
       self.secretThatWasSent = ''
 
   def sendNumbers(self, myNumbers: tuple[int, int]) -> tuple[int, int]:
      return myNumbers[0] + 1, myNumbers[1] + 1
 
   def sendSecret(self, secret: str) ->  None:
      self.secretThatWasSent = secret

   def toJson(self) -> str:
      return ""

def test_will_send_the_key():
   dummyCommunicator = MockChangeCommunicator()
   processHandler = KeyChangeProcess(dummyCommunicator)
   processHandler.doKeyChange('this is a test 123')

   assert processHandler.dataHandler.encryptOrDecrypt('this is a test 123') == dummyCommunicator.secretThatWasSent