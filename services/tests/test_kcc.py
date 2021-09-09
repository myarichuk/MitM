from shared.datahandler import KeyChangeDataHandler

#sanity check
def test_can_initialize():
   calc = KeyChangeDataHandler()
   assert calc is not None

#test the actual key change process without server-to-server transmission
def test_can_encrypt_and_decrypt():
   calcA = KeyChangeDataHandler()
   calcB = KeyChangeDataHandler()
   
   my = calcA.calculate_my()
   other = calcB.calculate_my()
   calcA.receiveOther(other)
   calcB.receiveOther(my)

   secret = 'foo bar 123!!!'

   encryptedSecret = calcA.encryptOrDecrypt(secret)
   decryptedSecret = calcB.encryptOrDecrypt(encryptedSecret)   

   assert secret == decryptedSecret

