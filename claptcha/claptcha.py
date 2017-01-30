# -*- coding: utf-8 -*-

import sys
import random
from functools import wraps
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


class ClaptchaError(Exception):
    """Exception class for Claptcha errors"""
    pass


class Claptcha(object):
    def __init__(self, size, margin, font):
        self.size = size
        self.margin = margin

    def _with_pair_validator(func):
        @wraps(func)
        def wrapper(inst, pair):
            if not hasattr(pair, '__len__') or not hasattr(pair, '__getitem__'):
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
