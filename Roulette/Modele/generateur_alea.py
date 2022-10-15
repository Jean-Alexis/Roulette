#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author : Jean-Alexis HERMEL
# Date : 02/10/2022

from random import SystemRandom
import matplotlib.pyplot as plt


def lancer_roulette(nombre_de_tours):
    cryptogen = SystemRandom()
    return cryptogen.randrange(0, 36)

"""
liste = []
for x in lancer_roulette(100000):
    liste.append(x)

plt.hist(liste, 36, edgecolor='white')
plt.show()
"""
