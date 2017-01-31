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

    @property
    def image(self):
        text = self.text
        w, h = self.font.getsize(text)
        margin_x = round(self.margin_x * w / self.w)
        margin_y = round(self.margin_y * h / self.h)

        image = Image.new('RGB',
                          (w + 2*margin_x, h + 2*margin_y),
                          (255, 255, 255, 255))

        # Text
        self._writeText(image, text, pos=(margin_x, margin_y))

        # Two lines
        self._drawLine(image)

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
            if not isinstance(file, ImageFont.ImageFont):
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
        if isinstance(font, ImageFont.ImageFont):
            self.__font = font
        else:
            fontsize = self.h - 2 * self.margin_x
            self.__font = ImageFont.truetype(font, fontsize)

    def _writeText(self, image, text, pos):
        offset = 0
        x,y = pos

        for c in text:
            # Write letter
            c_size = self.font.getsize(c)
            c_image = Image.new('RGBA', c_size, (0,0,0,0))
            c_draw = ImageDraw.Draw(c_image)
            c_draw.text((0, 0), c, font=self.font, fill=(0,0,0,255))

            # Transform
            c_image = self._rndLetterTransform(c_image)

            # Paste onto image
            image.paste(c_image, (x+offset, y), c_image)
            offset += c_size[0]

    def _drawLine(self, image):
        w,h = image.size
        w *= 5
        h *= 5

        l_image = Image.new('RGBA', (w,h), (0,0,0,0))
        l_draw = ImageDraw.Draw(l_image)

        x1 = int(w * random.uniform(0, 0.1))
        y1 = int(h * random.uniform(0, 1))
        x2 = int(w * random.uniform(0.9, 1))
        y2 = int(h * random.uniform(0, 1))

        # Draw
        l_draw.line(((x1, y1), (x2, y2)), fill=(0, 0, 0, 0xff), width=12)

        # Transform
        l_image = self._rndLineTransform(l_image)
        l_image = l_image.resize(image.size, resample=Image.BILINEAR)

        # Paste onto image
        image.paste(l_image, (0,0), l_image)

    def _rndLetterTransform(self, image):
        w,h = image.size

        dx = w * random.uniform(0.2, 0.7)
        dy = h * random.uniform(0.2, 0.7)

        x1, y1 = self.__class__._rndPointDisposition(dx, dy)
        x2, y2 = self.__class__._rndPointDisposition(dx, dy)

        w += abs(x1) + abs(x2)
        h += abs(x1) + abs(x2)

        quad = (
            x1,     -y1,
            -x1,    h + y2,
            w + x2, h - y2,
            w - x2, y1
        )

        return image.transform(image.size, Image.QUAD,
                               data=quad, resample=Image.BILINEAR)

    def _rndLineTransform(self, image):
        w,h = image.size

        dx = w * random.uniform(0.2, 0.5)
        dy = h * random.uniform(0.2, 0.5)
        
        x1, y1 = [abs(z) for z in self.__class__._rndPointDisposition(dx, dy)]
        x2, y2 = [abs(z) for z in self.__class__._rndPointDisposition(dx, dy)]

        quad = (
            x1,    -y1,
            -x1,    h + y2,
            w + x2, h - y2,
            w - x2, y1
        )

        return image.transform(image.size, Image.QUAD,
                               data=quad, resample=Image.BILINEAR)

    @staticmethod
    def _rndPointDisposition(dx, dy):
        x = int(random.uniform(-dx, dx))
        y = int(random.uniform(-dy, dy))
        return (x,y)
