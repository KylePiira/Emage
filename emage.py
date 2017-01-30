# Emage (Encrypt Image Project)
# v0.1 Alpha - Jan 29, 2017
# Copyright (C) 2016-2017 Kyle Piira

import os, hashlib, getpass, binascii, random, math, simplecrypt
from PIL import Image

def openImage(imgPath):
    img = Image.open(imgPath)
    width, height = img.size # Store the original size of Image

    pixels = []
    pix = img.load()
    # Flatten image into List
    for row in range(height):
        for pixel in range(width):
            # Creates a list of each pixel in image
            pixels.append(pix[pixel, row])

    return pixels, (width, height), img

def embedImage(imgPath, salt, message):
    pixels, shape, img = openImage(imgPath)
    embedCode = str(salt.decode('utf_8')) + str(message.decode('utf_8'))
    n = 6 # Number of chars in each 'byte' of embed code.
    embedBytes = [embedCode[i:i+n] for i in range(0, len(embedCode), n)]

    def bytesProcess(bytes):
        bytes[-1]

# Generate a key from current seed
def genKeyFromHash(length, hash):
    random.seed(hash)
    return ''.join(["%s" % random.randint(0, 9) for num in range(0, length)])

def encrypt(message, password, iters = 1000000, algorthm = 'sha512'):
    salt = binascii.hexlify(os.urandom(64)) # Generate Cryptographic Hex Salt
    # Hash the password using above salt.
    passwordHash = binascii.hexlify(hashlib.pbkdf2_hmac(algorthm, password.encode(encoding='utf_8'), salt, iters))

    # Encrypt Message
    def messageEncrypt(hash, message):
        key = genKeyFromHash(32, hash)
        messageLocked = binascii.hexlify(simplecrypt.encrypt(key, message))
        return messageLocked

    messageLocked = messageEncrypt(passwordHash, message)

    return salt, passwordHash, messageLocked

def decrypt(message, password, salt, iters = 1000000, algorthm = 'sha512'):
    # Generate hash using password and salt
    passwordHash = binascii.hexlify(hashlib.pbkdf2_hmac(algorthm, password.encode(encoding='utf_8'), salt, iters))

    # Decrypt Message
    def messageDecrypt(hash, message):
        key = genKeyFromHash(32, hash)
        messageUnlocked = simplecrypt.decrypt(key, binascii.unhexlify(message))
        return messageUnlocked

    messageUnlocked = messageDecrypt(passwordHash, message)

    return messageUnlocked


message = input('Message: ')
password = getpass.getpass(prompt='Password: ')
salt, passHash, message = encrypt(message, password)
embedImage('Image.png', salt, message)
