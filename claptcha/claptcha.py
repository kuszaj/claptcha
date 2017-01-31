# -*- coding: utf-8 -*-

import sys
import os
import random
from functools import wraps
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


class ClaptchaError(Exception):
    """Exception class for Claptcha errors"""
    pass


class Claptcha(object):
    def __init__(self, source, size, margin, font, format='PNG'):
        self.source = source
        self.size = size
        self.margin = margin
        self.font = font
        self.format = format

        self.__image = None

    @property
    def image(self):
        text = self.text
        w, h = self.font.getsize(text)
        margin_x = round(self.margin_x * w / self.w)
        margin_y = round(self.margin_y * h / self.h)

        image = Image.new('RGBA',
                          (w + 2*margin_x, h + 2*margin_y),
                          (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        return image

    @property
    def bytes(self):
        bytes = BytesIO()
        self.image.save(bytes, format = self.format)
        bytes.seek(0)
        return bytes

    def write(self, file):
        self.image.save(file, format = self.format)

    @property
    def source(self):
        return self.__source

    @source.setter
    def source(self, source):
        if not (isinstance(source, str) or callable(source)):
            raise ClaptchaError("source has to be either a string or be callable")
        self.__source = source

    @property
    def text(self):
        if isinstance(self.source, str):
            return self.source
        else:
            return self.source()

    def _with_pair_validator(func):
        @wraps(func)
        def wrapper(inst, pair):
            if not (hasattr(pair, '__len__') and hasattr(pair, '__getitem__')):
                raise ClaptchaError("Sequence not provided")
            if len(pair) != 2:
                raise ClaptchaError("Sequence has to have exactly 2 elements")
            return func(inst, pair)
        return wrapper

    @property
    def size(self):
        return self.__size
        
    @size.setter
    @_with_pair_validator
    def size(self, size):
        self.__size = (int(size[0]), int(size[1]))
       
    @property
    def w(self):
        return self.size[0]

    @property
    def h(self):
        return self.size[1]

    @property
    def margin(self):
        return self.__margin
    
    @margin.setter
    @_with_pair_validator
    def margin(self, margin):
        self.__margin = (int(margin[0]), int(margin[1]))

    @property
    def margin_x(self):
        return self.__margin[0]

    @property
    def margin_y(self):
        return self.__margin[1]

    def _with_file_validator(func):
        @wraps(func)
        def wrapper(inst, file):
            if not isintance(file, ImageFont):
                if not os.path.exists(file):
                    raise ClaptchaError("%s doesn't exist" % (file,))
                if not os.path.isfile(file):
                    raise ClaptchaError("%s is not a file" % (file,))
            return func(inst, file)
        return wrapper

    @property
    def font(self):
        return self.__font

    @font.setter
    @_with_file_validator
    def font(self, font):
        if isinstance(font, ImageFont):
            self.__font = font
        else:
            fontsize = self.h - 2 * self.margin_x
            self.__font = ImageFont.truetype(font, fontsize)
