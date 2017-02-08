# Claptcha

Simple CAPTCHA generator package.

This module provides a single class (Claptcha) that can create on the fly
PIL Image instances, BytesIO objects or save image files containing a simple
CAPTCHA strings. Its build on top of Pillow package.

It is required that user provides a TTF file with font to be used in images
and either a string with CAPTCHA text or a callable object returning strings
to be used in images.

## Installation

```bash
$ python3 setup.py install
```

## Usage

```python
from claptcha import Claptcha

# Initialize Claptcha object with "Text" as text and FreeMono as font
c = Claptcha("Text", "FreeMono.ttf")

# Get PIL Image object
text, image = c.image

print(text))         # Text
print(type(image)))  # <class 'PIL.Image.Image'>

# Get BytesIO object (note that it will represent a different image, just
# with the same text)
text, bytes = c.bytes

print(text))         # Text
print(type(bytes)))  # <class '_io.BytesIO'>

# Save a PNG file 'test.png'
text, file = c.write('test.png')

print(text))         # Text
print(file))         # test.png
```

```python
import random
import string
from PIL import Image
from claptcha import Claptcha

def randomString():
    rndLetters = (random.choice(string.ascii_uppercase) for _ in range(6))
    return "".join(rndLetters)

# Initialize Claptcha object with random text, FreeMono as font, of size
# 100x30, using bicubic resampling filter and adding a bit of white noise
c = Claptcha(randomString, "FreeMono.ttf", (100,30),
             resample=Image.BICUBIC), noise=0.3)

text, _ = c.write('captcha1.png')
print(text)  # PZTBXB

text, _ = c.write('captcha2.png')
print(text)  # NEDKEM
```

## License

MIT
