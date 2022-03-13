import math
from random import random

def point(h, k, r):  # code taken from D5
        """This creates a random point somewhere on the circumference of a circle"""
        # h and k are the center of the circle so the origin point
        # r is radius
        theta = random() * 2 * math.pi
        return h + math.cos(theta) * r, k + math.sin(theta) * r