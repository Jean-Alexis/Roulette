#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author : Jean-Alexis HERMEL
# Date : 05/10/2022


from Vue.widgets.widget_roulette import *
from Vue.widgets.widget_bouttons import *
from Vue.widgets.widget_label import *


class MainWindow(QMainWindow):

    def __init__(self, modele, controleur):
        super().__init__()
        self.modele = modele          # instance du modele de jeu
        self.controleur = controleur  # controleur
        self.resize(1385, 720)

        self.setWindowTitle('Roulette')
        chemin_icone = trouver_image_ressources("icone_roulette.png")
        self.setWindowIcon(QIcon(chemin_icone))
        self.setStyleSheet(CSS.css_main_window)

        self.status_bar = StatusBar(self)  # bar en bas de la fenetre
        self.table_widget = TabBar(self)
        self.setCentralWidget(self.table_widget)

        #self.center()

    def center(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())


class TabBar(QTabBar):

    def __init__(self, main_window):
        super(QTabBar, self).__init__(main_window)
        self.main_window = main_window
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(CSS.css_tab_bar)

        self.widget_central_table_roulette = WidgetCentralTableRoulette(self)
        self.widget_statistiques = QWidget(self)
        self.widget_simulation = WidgetSimulation(self)

        self.tabs.addTab(self.widget_central_table_roulette, "Jeu")
        self.tabs.addTab(self.widget_statistiques, "Statistiques")
        self.tabs.addTab(self.widget_simulation, "Simulation")

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


class StatusBar(QWidget):

    def __init__(self, mainwindow):
        super(QWidget, self).__init__(mainwindow)
        self.mainwindow = mainwindow
        self.status = QStatusBar()
        self.mainwindow.setStatusBar(self.status)

        self.status.showMessage("Roulette")
        self.status.setStyleSheet(CSS.css_status_bar)

        self.status.addPermanentWidget(self.VLine())
        self.status.addPermanentWidget(self.VLine())
        self.status.addPermanentWidget(self.VLine())

    class VLine(QFrame):
        """permet de créer des lignes de séparation verticale"""

        def __init__(self):
            super().__init__()
            self.setFrameShape(self.VLine | self.Sunken)
            self.setStyleSheet(" background: #afb1b3; max-height: 18px;")




