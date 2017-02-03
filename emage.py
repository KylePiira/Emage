# Emage (Encrypt Image Project)
# v0.3 Alpha - Feb 3, 2017
# Copyright (C) 2016-2017 Kyle Piira

import os, hashlib, getpass, binascii, random, simplecrypt
from PIL import Image as PILImage

class Helper:
    # Convert Hex codes to RGB
    def hexToRGB(value):
        # Return (red, green, blue) for the color given as #rrggbb.
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

    # Convert RGB to Hex codes
    def rgbToHex(red, green, blue):
        # Return color as #rrggbb for the given color values
        return '%02x%02x%02x' % (red, green, blue)

    # Generate a key from current seed
    def genKeyFromHash(length, hash):
        random.seed(hash)
        return ''.join(["%s" % random.randint(0, 9) for num in range(0, length)])

    # Generate hash from password
    def passHash(algorthm, password, salt, iters):
        return binascii.hexlify(
                    hashlib.pbkdf2_hmac(
                                    algorthm,
                                    password.encode(encoding='utf_8'),
                                    salt,
                                    iters
                                )
                            )

class Pixel:
    def __init__(self, color):
        self.isModified = False
        self.color = color

    def changeColor(self, color):
        self.isModified = True
        self.color = color

class Image:
    def __init__(self):
        self.imgPath = None
        self.img = None
        self.pixels = None
        self.width = None
        self.height = None

    def open(self, imgPath):
        self.img = PILImage.open(imgPath)
        self.width, self.height = self.img.size # Store the original size of Image
        self.imgPath = imgPath

        pixels = []
        pix = self.img.load()
        # Flatten image into List
        for row in range(self.height):
            for pixel in range(self.width):
                # Creates a list of each pixel in image
                pixels.append(Pixel(pix[pixel, row]))

        self.pixels = pixels

    def save(self):
        pix = self.img.load()
        pixelNum = 0

        for row in range(self.height):
            for pixel in range(self.width):
                # Creates a list of each pixel in image
                # print(str(pixelNum) + '. ' + str(self.pixels[pixelNum].color))
                pix[pixel, row] = self.pixels[pixelNum].color
                pixelNum += 1

        self.img.save(self.imgPath)

def embedImage(img, salt, hash, password, message):
    # '000000' is the devider between salt and message.
    embedCode = {
        'salt':str(salt.decode('utf_8')) + '000000',
        'message':str(message.decode('utf_8'))
    }
    n = 6 # Number of chars in each 'byte' of embed code.
    for itr in embedCode:
        embedCode[itr] = [embedCode[itr][i:i+n] for i in range(0, len(embedCode[itr]), n)]

    # Set the total number of pixels
    totalPixels = len(img.pixels)

    # Make last byte a full 6 chars
    embedCode['message'][-1] = embedCode['message'][-1].zfill(6)

    for i in range(len(embedCode['salt'])):
        random.seed(password)
        img.pixels[random.randint(0, totalPixels)].changeColor(Helper.hexToRGB(embedCode['salt'][i]))

    for i in range(len(embedCode['message'])):
        random.seed(hash)
        img.pixels[random.randint(0, totalPixels)].changeColor(Helper.hexToRGB(embedCode['message'][i]))

    img.save()

def encrypt(message, password, iters = 1000000, algorthm = 'sha512'):
    # Generate Cryptographic Hex Salt
    # Salt length must be a multiple of
    # 6 so that it can fit in Hex codes
    salt = binascii.hexlify(os.urandom(66))
    # Hash the password using above salt.
    passwordHash = Helper.passHash(algorthm, password, salt, iters)

    # Encrypt Message
    def messageEncrypt(hash, message):
        key = Helper.genKeyFromHash(32, hash)
        messageLocked = binascii.hexlify(simplecrypt.encrypt(key, message))
        return messageLocked

    messageLocked = messageEncrypt(passwordHash, message)

    return salt, passwordHash, messageLocked

def decrypt(message, password, salt, iters = 1000000, algorthm = 'sha512'):
    # Generate hash using password and salt
    passwordHash = Helper.passHash(algorthm, password, salt, iters)

    # Decrypt Message
    def messageDecrypt(hash, message):
        key = Helper.genKeyFromHash(32, hash)
        messageUnlocked = simplecrypt.decrypt(key, binascii.unhexlify(message))
        return messageUnlocked

    messageUnlocked = messageDecrypt(passwordHash, message)

    return messageUnlocked


message = input('Message: ')
password = getpass.getpass(prompt='Password: ')
salt, passHash, message = encrypt(message, password)
img = Image()
img.open('Image.png')
embedImage(img, salt, passHash, password, message)
