#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author : Jean-Alexis HERMEL
# Date : 12/10/2022

from Vue.constantes import *


class WidgetLabelBanqueMise(QWidget):

    def __init__(self, widget_central_table_roulette):
        super(QWidget, self).__init__(widget_central_table_roulette)
        self.widget_central_table_roulette = widget_central_table_roulette
        layoutH = QHBoxLayout(self)

        self.label = QLabel(f"Mise Totale : ")
        self.label.setStyleSheet(CSS.css_label_banque_mise)
        #self.label.setFixedSize(300, 60)
        self.label.setContentsMargins(20, 0, 0, 17)
        self.label.setFixedWidth(250)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.label2 = QLabel(f"Banque : ")
        self.label2.setStyleSheet(CSS.css_label_banque_mise)
        self.label2.setFixedWidth(250)
        self.label2.setContentsMargins(0, 0, 0, 17)
        self.label2.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        layoutH.addWidget(self.label)
        layoutH.addWidget(self.label2)
        layoutH.setContentsMargins(10, 0, 0, 0)
        layoutH.setSpacing(0)

        self.setLayout(layoutH)

        self.update_label_banque()
        self.update_label_mise()

    def update_label_banque(self):
        banque = self.widget_central_table_roulette.main_window.modele.banque
        self.label2.setText(f"Banque :  {banque}")

    def update_label_mise(self):
        mise = self.widget_central_table_roulette.main_window.modele.calculer_mise_totale()
        self.label.setText(f"Mise Totale :  {mise}")