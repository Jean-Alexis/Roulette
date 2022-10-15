#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author : Jean-Alexis HERMEL
# Date : 11/10/2022

from Vue.constantes import *


class WidgetBoutonEffacerJetons(QWidget):

    def __init__(self, widget_central_table_roulette):
        super(QWidget, self).__init__(widget_central_table_roulette)
        self.widget_central_table_roulette = widget_central_table_roulette
        layout = QHBoxLayout(self)
        self.btn_effacer_jetons = QPushButton("Effacer les Jetons")
        self.btn_effacer_jetons.clicked.connect(self.widget_central_table_roulette.widget_table_roulette.scene.effacer_tous_les_jetons)
        self.btn_effacer_jetons.setStyleSheet(CSS.css_bouton_effacer_jetons)

        #self.setAttribute(Qt.WA_StyledBackground, True)
        # self.setStyleSheet('background-color: yellow;')
        self.setFixedSize(200, 50)

        layout.addWidget(self.btn_effacer_jetons)
        layout.setContentsMargins(45, 0, 10, 0)

        self.setLayout(layout)


class WidgetBoutonTourner(QWidget):

    def __init__(self, widget_central_table_roulette):
        super(QWidget, self).__init__(widget_central_table_roulette)
        self.widget_central_table_roulette = widget_central_table_roulette
        layout = QHBoxLayout(self)
        self.btn_tourner = QPushButton("TOURNER")
        self.btn_tourner.clicked.connect(self.clicked)
        self.btn_tourner.setStyleSheet(CSS.css_bouton_tourner)

        #self.setAttribute(Qt.WA_StyledBackground, True)
        #self.setStyleSheet('background-color: yellow;')
        self.setFixedSize(400, 60)

        layout.addWidget(self.btn_tourner)
        layout.setContentsMargins(0, 0, 0, 10)

        self.setLayout(layout)

    def clicked(self):
        if not self.widget_central_table_roulette.widget_table_roulette.scene.animation_clignottement_en_cours:
            self.widget_central_table_roulette.main_window.modele.lancer_tirage(1)
            self.widget_central_table_roulette.widget_historique_tirage.actualiser_historique()
            self.widget_central_table_roulette.widget_table_roulette.animer_case_tirage(self.widget_central_table_roulette.main_window.modele.queue_resultats_tirages[0])
            self.widget_central_table_roulette.main_window.modele.mettre_banque_a_jour()


class WidgetBoutonMontrerGainsCases(QWidget):

    def __init__(self, widget_central_table_roulette):
        super(QWidget, self).__init__(widget_central_table_roulette)
        self.widget_central_table_roulette = widget_central_table_roulette
        layout = QVBoxLayout(self)
        self.btn_montrer_gains = QPushButton("Afficher Gains")
        self.btn_montrer_gains.pressed.connect(self.click_bouton)
        self.btn_montrer_gains.released.connect(self.release_bouton)
        self.btn_montrer_gains.setStyleSheet(CSS.css_bouton_afficher_gains)
        self.btn_montrer_gains.setCheckable(True)
        self.btn_montrer_gains.setChecked(True)
        self.btn_montrer_gains.setContentsMargins(0, 0, 0, 0)
        self.btn_montrer_gains.setFixedSize(125, 30)

        self.label = QLabel(f"Gain Moy/case: 0\nRatio Gain/Mise: 0")
        self.label.setStyleSheet(CSS.css_label_info)
        self.label.setFixedSize(125, 25)
        self.label.setContentsMargins(0, 0, 0, 0)
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)


        # self.setAttribute(Qt.WA_StyledBackground, True)
        # self.setStyleSheet('background-color: yellow;')
        #self.setFixedSize(120, 60)

        layout.addWidget(self.btn_montrer_gains)
        layout.addWidget(self.label)
        layout.setContentsMargins(10, 0, 0, 0)
        layout.setSpacing(0)


        self.setLayout(layout)

    def click_bouton(self):
        self.widget_central_table_roulette.widget_table_roulette.initier_cases_gain()
        gain_moyen, ratio_gain_mise = self.widget_central_table_roulette.main_window.modele.calculer_gain_moyen_case()
        self.label.setText(f"Gain Moy/case: {gain_moyen}\nRatio Gain/mise: {ratio_gain_mise}")

    def release_bouton(self):
        self.btn_montrer_gains.setChecked(True)
        for num_case, item_case_gain in self.widget_central_table_roulette.widget_table_roulette.dic_item_case_gain.items():
            self.widget_central_table_roulette.widget_table_roulette.scene.removeItem(item_case_gain)
        self.widget_central_table_roulette.widget_table_roulette.dic_item_case_gain = {}



class WidgetBoutonJeton(QWidget):

    def __init__(self, widget_selection_jeton, valeur, couleur, taille_jeton):
        super(QWidget, self).__init__()
        self.widget_selection_jeton = widget_selection_jeton
        self.taille_jeton = taille_jeton
        self.valeur = valeur
        self.couleur = couleur

        layout = QHBoxLayout(self)
        self.bouton_jeton = QPushButton(str(self.valeur))
        self.bouton_jeton.setFixedSize(self.taille_jeton, self.taille_jeton)
        self.bouton_jeton.clicked.connect(self.click_event)
        self.bouton_jeton.setStyleSheet(CSS.css_style_jeton(self.couleur, "grand"))
        self.bouton_jeton.setCursor(QCursor(Qt.PointingHandCursor))
        layout.addWidget(self.bouton_jeton)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def click_event(self):
        self.widget_selection_jeton.widget_central_table_roulette.widget_table_roulette.scene.valeur_ajout_jeton = self.valeur
        self.widget_selection_jeton.reinitialiser_grand_jetons()
        self.bouton_jeton.setStyleSheet(CSS.css_style_jeton(self.couleur, "petit"))
