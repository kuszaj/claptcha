# -*- coding: utf-8 -*-

"""
A simple CAPTCHA image generator.

This module provides a single class (Claptcha) that can create on the fly
PIL Image instances, BytesIO objects or save image files containing a simple
CAPTCHA strings. Its build on top of Pillow package.

It is required that user provides a TTF file with font to be used in images
and either a string with CAPTCHA text or a callable object returning strings
to be used in images.

Examples:

>>> from claptcha import Claptcha
>>>
>>> # Initialize Claptcha object
>>> c = Claptcha("Text", "FreeMono.ttf")
>>>
>>> # Create a PIL Image object, return it and provided text
>>> c.image
('Text', <PIL.Image.Image image mode=RGB size=200x80 at 0xB741406C>)
>>>
>>> # Create a BytesIO object, return it and provided text
>>> c.bytes
('Text', <_io.BytesIO object at 0xb71e87dc>)
>>>
>>> # Save image in 'claptcha.png' file, return its path and provided text
>>> c.write('claptcha.png')
('Text', 'test.png')
>>>
>>> def captchaStr():
...     return "TextFromFunc"
...
>>> # Redefine c: change its size to 100x30, use bicubic resampling filter
>>> # and add white noise
>>> from PIL import Image
>>> c = Claptcha(captchaStr, "FreeMono.ttf", (100,30),
...              resampling=Image.BICUBIC, noise=0.3)
>>> c.image
('TextFromFunc', <PIL.Image.Image image mode=RGB size=100x30 at 0xB73EE66C>)
"""

from .claptcha import Claptcha


__version__ = "0.3.3"
