from distutils.core import setup
setup(
  name = 'emage',
  packages = ['emage'], # this must be the same as the name above
  version = 'v0.5.2b',
  description = 'A library for encrypting and decrypting data into images.',
  author = 'Kyle Piira',
  author_email = 'contact@kylepiira.com',
  url = 'https://github.com/KylePiira/Emage', # use the URL to the github repo
  download_url = 'https://github.com/KylePiira/Emage/archive/v0.5.2.tar.gz',
  keywords = ['emage', 'encryption', 'decryption'], # arbitrary keywords
  license = 'GNUv3',
  classifiers = [],
  install_requires=['simple-crypt','pillow'],
)
