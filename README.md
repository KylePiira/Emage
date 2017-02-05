# Emage
Image Encryption Project

# Installation
```python
pip install emage
```

# Usage
```python
from emage import encrypt, decrypt
```

then to encrypt some text

```python
encrypt('/path/to/image/file.png','strongpasswordhere','The message to be encryped')
```

to decrypt the text use

```python
message = decrypt('/path/to/image/file.png','strongpasswordhere')
```

the above will return a bytes object of the string that has been embeded in the image.

# Examples
```python
>>> from emage import encrypt, decrypt
>>> encrypt('penguins.png','password','This is a photograph of a penguin')
>>> message = decrypt('penguins.png','password')
>>> message
b'This is a photograph of a penguin'
>>> 
```
The image penguins.png now has the following text embeded in it: "This is a photograph of a penguin" protected by the password: "password".
![Penguin](/examples/penguins.png?raw=true "Penguin")
