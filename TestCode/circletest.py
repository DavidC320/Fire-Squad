# code from Robᵩ
import matplotlib.pyplot as plt
from math import pi, cos, sin
from random import random

def point(h, k, r):
    # h and k are the center of the circle so the origin point
    # r is radius
    theta = random() * 2 * pi
    return h + cos(theta) * r, k + sin(theta) * r

xy = [point(0,0,800) for _ in range(30)]

plt.scatter(*zip(*xy))
plt.grid(color='k', linestyle=':', linewidth=1)
plt.show()