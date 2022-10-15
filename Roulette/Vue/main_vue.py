#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author : Jean-Alexis HERMEL
# Date : 05/10/2022


from Vue.widgets.widget_roulette import *
from Vue.widgets.widget_bouttons import *


class MainWindow(QMainWindow):

    def __init__(self, modele, controleur):
        super().__init__()
        self.modele = modele          # instance du modele de jeu
        self.controleur = controleur  # controleur

        self.setWindowTitle('Roulette')
        chemin_icone = trouver_image_ressources("icone_roulette.png")
        self.setWindowIcon(QIcon(chemin_icone))
        self.setStyleSheet(CSS.css_main_window)

        self.widget_central_table_roulette = WidgetCentralTableRoulette(self)
        self.setCentralWidget(self.widget_central_table_roulette)

        #self.center()

    def center(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())



