# Emage (Encrypt Image Project)
# v0.5 Beta - Feb 4, 2017
# Copyright (C) 2016-2017 Kyle Piira

import os, hashlib, binascii, random, simplecrypt
from PIL import Image as PILImage

class Helper:
    # Convert Hex codes to RGB
    def hexToRGB(value):
        # Return (red, green, blue) for the color given as #rrggbb.
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

    # Convert RGB to Hex codes
    def rgbToHex(value):
        red, green, blue = value[:3]
        # Return color as #rrggbb for the given color values
        return '%02x%02x%02x' % (red, green, blue)

    # Generate a key from current seed
    def genKeyFromHash(length, hash):
        random.seed(hash)
        return ''.join(["%s" % random.randint(0, 9) for num in range(0, length)])

    # Generate hash from password
    def passHash(password, salt, iters, algorthm):
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
        self.seen = False
        self.color = color

    def setColor(self, color):
        self.isModified = True
        self.seen = True
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

        self.img.save(self.imgPath, "PNG")

def encrypt(imgPath, password, message, iters = 1000000, algorthm = 'sha512'):
    # Initilize Image
    img = Image()
    # Open Image
    img.open(imgPath)

    # Encrypt Message
    def messageEncrypt(hash, message):
        key = Helper.genKeyFromHash(32, hash)
        messageLocked = binascii.hexlify(simplecrypt.encrypt(key, message))
        return messageLocked

    # We are using a while loop to verify that the first character
    # of the last byte of the encrypted message does not start with
    # a zero, so that we can pad it with zeros. If it does we will
    # regenerate it until it no longer does.
    while True:
        # Generate Cryptographic Hex Salt
        # Salt length must be a multiple of
        # 6 so that it can fit in Hex codes
        salt = binascii.hexlify(os.urandom(66))
        # Hash the password using above salt.
        passwordHash = Helper.passHash(password, salt, iters, algorthm)

        messageLocked = messageEncrypt(passwordHash, message)

        # '000000' is the devider between salt and message.
        embedCode = {
            'salt':str(salt.decode('utf_8')) + '000000',
            'message':str(messageLocked.decode('utf_8'))
        }
        n = 6 # Number of chars in each 'byte' of embed code.
        for itr in embedCode:
            embedCode[itr] = [embedCode[itr][i:i+n] for i in range(0, len(embedCode[itr]), n)]

        if embedCode['message'][-1][0] is not '0':
            break

    # Set the total number of pixels
    totalPixels = len(img.pixels)

    # Make last byte a full 6 chars
    embedCode['message'][-1] = embedCode['message'][-1].zfill(6)
    embedCode['message'].append('000000')

    def pixelShuffle(img, seed, key, embedCode, totalPixels):
        random.seed(seed)
        for i in range(len(embedCode[key])):
            while True:
                randIndex = random.randint(0, totalPixels)
                pixel = img.pixels[randIndex]
                if not pixel.isModified:
                    pixel.setColor(Helper.hexToRGB(embedCode[key][i]))
                    break

    # Shuffle the salt into the image
    pixelShuffle(
        img,
        Helper.passHash(password, ''.encode('utf_8'), iters, algorthm),
        'salt',
        embedCode,
        totalPixels
    )

    # Shuffle the encrypted message into image.
    pixelShuffle(img, passwordHash, 'message', embedCode, totalPixels)

    # Save the image to disk.
    img.save()

def decrypt(imgPath, password, iters = 1000000, algorthm = 'sha512'):
    # Initilize Image
    img = Image()
    # Open Image
    img.open(imgPath)
    # Retrieve pixels from image based on Seed
    def pixelUnshuffle(img, seed, totalPixels):
        random.seed(seed)
        pixels = []
        color = False
        while color != '000000':
            while True:
                randIndex = random.randint(0, totalPixels)
                pixel = img.pixels[randIndex]
                if not pixel.seen:
                    color = Helper.rgbToHex(pixel.color)
                    pixels.append(color)
                    pixel.seen = True
                    break
        return pixels

    # Retrieve the salt
    salt = ''.join(pixelUnshuffle(
        img,
        Helper.passHash(password, ''.encode('utf_8'), iters, algorthm),
        len(img.pixels)
    )[:-1]).encode('utf_8')

    # Generate hash using password and salt
    passwordHash = Helper.passHash(password, salt, iters, algorthm)

    # Retrieve the message (encrypted)
    message = pixelUnshuffle(
        img,
        passwordHash,
        len(img.pixels)
    )[:-1]

    # Remove padding from final byte.
    # print(message)
    message[-1] = message[-1].lstrip('0')

    # Convert message to bytes
    message = ''.join(message).encode('utf_8')

    # Decrypt Message
    def messageDecrypt(hash, message):
        key = Helper.genKeyFromHash(32, hash)
        messageUnlocked = simplecrypt.decrypt(key, binascii.unhexlify(message))
        return messageUnlocked

    return messageDecrypt(passwordHash, message)
