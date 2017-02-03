# Emage (Encrypt Image Project)
# v0.2 Alpha - Jan 29, 2017
# Copyright (C) 2016-2017 Kyle Piira

import os, hashlib, getpass, binascii, random, simplecrypt
from PIL import Image

# Convert Hex codes to RGB
def hexToRGB(value):
    # Return (red, green, blue) for the color given as #rrggbb.
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

# Convert RGB to Hex codes
def rgbToHex(red, green, blue):
    # Return color as #rrggbb for the given color values
    return '%02x%02x%02x' % (red, green, blue)

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

def embedImage(imgPath, img, pixels, salt, message):
    # '000000' is the devider between salt and message.
    embedCode = str(salt.decode('utf_8')) + '000000' + str(message.decode('utf_8'))
    n = 6 # Number of chars in each 'byte' of embed code.
    embedBytes = [embedCode[i:i+n] for i in range(0, len(embedCode), n)]

    # Make last byte a full 6 chars
    embedBytes[-1] = embedBytes[-1].zfill(6)

    for i in range(len(embedBytes)):
        pixels[i] = hexToRGB(embedBytes[i])

    width, height = img.size # Store the original size of Image
    pix = img.load()
    pixelNum = 0
    for row in range(height):
        for pixel in range(width):
            # Creates a list of each pixel in image
            pix[pixel, row] = pixels[pixelNum]
            pixelNum += 1

    img.save(imgPath)
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

def encrypt(message, password, iters = 1000000, algorthm = 'sha512'):
    # Generate Cryptographic Hex Salt
    # Salt length must be a multiple of
    # 6 so that it can fit in Hex codes
    salt = binascii.hexlify(os.urandom(66))
    # Hash the password using above salt.
    passwordHash = passHash(algorthm, password, salt, iters)

    # Encrypt Message
    def messageEncrypt(hash, message):
        key = genKeyFromHash(32, hash)
        messageLocked = binascii.hexlify(simplecrypt.encrypt(key, message))
        return messageLocked

    messageLocked = messageEncrypt(passwordHash, message)

    return salt, passwordHash, messageLocked

def decrypt(message, password, salt, iters = 1000000, algorthm = 'sha512'):
    # Generate hash using password and salt
    passwordHash = passHash(algorthm, password, salt, iters)

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
pixels, (width, height), img = openImage('Image.png')
embedImage('Image.png', img, pixels, salt, message)
