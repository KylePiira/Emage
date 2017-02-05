from emage import encrypt, decrypt
import random, time, sys

currentTest = 0
try:
    testsNum = sys.argv[1]
except IndexError:
    testsNum = 100
try:
    while currentTest <= int(testsNum):
        password = str(random.randint(10000,99999999999999999999))
        message = str(random.randint(100000000000000000000,9999999999999999999999999999999999))
        encrypt('penguins.png', password, message)
        decryptedMessage = decrypt('penguins.png', password).decode('utf_8')
        if decryptedMessage == message:
            print('Test Passed => ' + message)
        else:
            print('Test Failed:')
            print('Password: ' + password)
            print('Message: ' + message)
            print('Returned Message: ' + decryptedMessage)
            time.sleep(10)
        currentTest += 1
except:
    print(password)
    print(message)
    exit()
