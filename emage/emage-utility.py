from emage import encrypt, decrypt
import getpass, argparse

parser = argparse.ArgumentParser(description='Encrypt or decrypt a message using Emage')
parser.add_argument('-e','--encrypt', help='set mode to encrypt', action='store_true', required=False)
parser.add_argument('-m','--message', help='the message you want to be encryped', required=False)
parser.add_argument('-p','--password', help='the password to be used for encryption or decryption', required=False)
parser.add_argument('-d','--decrypt', help='set mode to decrypt', action='store_true', required=False)
parser.add_argument('-f','--file', help='path to image', required=True)
args, leftovers = parser.parse_known_args()

# Check if in Encrypt mode
if args.encrypt:
    # Check if message was entered via
    # argument or needs to be queried
    if args.message is not None:
        message = args.message
    else:
        message = input('Message: ')

    # Check if password was entered via
    # argument or needs to be queried
    if args.password is not None:
        password = args.password
    else:
        while True:
            pass1 = getpass.getpass(prompt='Password: ')
            pass2 = getpass.getpass(prompt='Password Again: ')
            # Check if passwords are same.
            if pass1 == pass2:
                password = pass1
                break
            else:
                print('Passwords not the same! Try again.')
    # Encrypt the file.
    encrypt(args.file, password, message)
    print('Encrypted')

# Check if in Decrypt mode
elif args.decrypt:
    # Check if password was entered via
    # argument or needs to be queried
    if args.password is not None:
        password = args.password
    else:
        password = getpass.getpass(prompt='Password: ')
    # Decrypt the file.
    print(decrypt(args.file, password))
else:
    print('Please enter a mode!')
    print('emage-utility --encrypt --file=./file.png')
    print('or')
    print('emage-utility --decrypt --file=./file.png')
