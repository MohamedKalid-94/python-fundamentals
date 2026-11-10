import math


class Circle:
    def __init__(self, r):
        self.r = r

    def area(self):
        return round(math.pi * self.r ** 2, 2)


class Rectangle:
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def area(self):
        return self.w * self.h