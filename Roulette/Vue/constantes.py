#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author : Jean-Alexis HERMEL
# Date : 11/10/2022


from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from Vue import CSS
from Modele.outils import *
from collections import OrderedDict
import os

ROUGE = QColor(197, 18, 18, 255)
VERT = QColor(46, 125, 50, 255)
NOIR = QColor(25, 25, 25, 255)
OR = QColor(253, 224, 141, 255)
GRIS = QColor(40, 41, 45, 255)
GRIS_MAIN = QColor(54,54,54, 255)

ROUGE_CLAIR = QColor(241, 106, 106, 255)
VERT_CLAIR = QColor(119, 205, 123, 255)
NOIR_CLAIR = QColor(115, 115, 115, 255)

CREME = QColor(243, 242, 211, 255)
CREME_CLAIR = QColor(251, 251, 240, 255)

TAILLE_CASE = 80
TAILLE_JETON = TAILLE_CASE//2 - 1


class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)
        self.setFixedSize(100,100)
        self.setContentsMargins(0, 0, 0, 0)
