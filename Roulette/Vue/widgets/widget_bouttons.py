#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author : Jean-Alexis HERMEL
# Date : 11/10/2022

from Vue.constantes import *
from copy import copy


class WidgetBoutonsHistoriqueJetons(QWidget):

    def __init__(self, widget_central_table_roulette):
        super(QWidget, self).__init__(widget_central_table_roulette)
        self.widget_central_table_roulette = widget_central_table_roulette
        #self.setFixedSize(110, 50)

        self.grid_layout = QGridLayout(self)
        self.grid_layout.setContentsMargins(0, 10, 0, 3)
        self.grid_layout.setSpacing(0)

        self.label_historique_mise = QLabel("Historique Mises")
        self.label_historique_mise.setStyleSheet(CSS.css_label_info)
        self.label_historique_mise.setFixedSize(90, 10)
        self.label_historique_mise.setContentsMargins(0, 0, 0, 0)
        self.label_historique_mise.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.btn_vers_gauche = QPushButton("<")
        self.btn_vers_gauche.setFixedSize(30, 30)
        self.btn_vers_gauche.setStyleSheet(CSS.css_bouton_afficher_gains)
        self.btn_vers_gauche.clicked.connect(self.click_gauche)

        self.btn_vers_droite = QPushButton(">")
        self.btn_vers_droite.setFixedSize(30, 30)
        self.btn_vers_droite.setStyleSheet(CSS.css_bouton_afficher_gains)
        self.btn_vers_droite.clicked.connect(self.click_droit)

        self.grid_layout.addWidget(self.label_historique_mise, 2, 0, 1, 6, alignment=(Qt.AlignBottom | Qt.AlignVCenter))
        self.grid_layout.addWidget(self.btn_vers_gauche, 1, 2, 1, 1, alignment=(Qt.AlignBottom | Qt.AlignHCenter))
        self.grid_layout.addWidget(self.btn_vers_droite, 1, 3, 1, 1, alignment=(Qt.AlignBottom | Qt.AlignHCenter))

        self.setLayout(self.grid_layout)

    def click_gauche(self):
        scene = self.widget_central_table_roulette.widget_table_roulette.scene

        if len(scene.historique_dic_jeton) != 0:
            if scene.curseur_historique_dic_jeton != 0:
                scene.curseur_historique_dic_jeton -= 1
                scene.effacer_tous_les_jetons()
                scene.dic_jeton = copy(scene.historique_dic_jeton[scene.curseur_historique_dic_jeton])
                scene.placer_jetons_du_dic_jetons()

    def click_droit(self):
        scene = self.widget_central_table_roulette.widget_table_roulette.scene

        if len(scene.historique_dic_jeton) != 0:
            if scene.curseur_historique_dic_jeton < scene.nombre_historique_dic_jeton:

                scene.effacer_tous_les_jetons()
                scene.dic_jeton = copy(scene.historique_dic_jeton[scene.curseur_historique_dic_jeton])
                scene.placer_jetons_du_dic_jetons()
                scene.curseur_historique_dic_jeton += 1


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

    def __init__(self, table_roulette_view):
        super(QWidget, self).__init__(table_roulette_view)
        self.table_roulette_view = table_roulette_view
        layout = QHBoxLayout(self)
        self.btn_tourner = QPushButton("TOURNER")
        self.btn_tourner.clicked.connect(self.clicked)
        self.btn_tourner.setStyleSheet(CSS.css_bouton_tourner)
        self.scene = self.table_roulette_view.scene
        self.modele = self.table_roulette_view.widget_central_table_roulette.main_window.modele

        #self.setAttribute(Qt.WA_StyledBackground, True)
        #self.setStyleSheet('background-color: yellow;')
        self.setFixedSize(320, 60)

        layout.addWidget(self.btn_tourner)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)

    def clicked(self):
        if self.modele.calculer_mise_totale() <= self.modele.banque:

            if not self.scene.animation_clignottement_en_cours:
                if len(self.scene.dic_jeton) != 0:  # si on a misé quelque chose
                    self.scene.ajouter_pattern_historique_mise()

                    if self.scene.nombre_historique_dic_jeton < 100:
                        self.scene.nombre_historique_dic_jeton += 1
                    self.scene.curseur_historique_dic_jeton = 0

                self.modele.lancer_tirage()
                self.table_roulette_view.widget_central_table_roulette.widget_historique_tirage.actualiser_historique()
                self.table_roulette_view.widget_central_table_roulette.widget_table_roulette.animer_case_tirage(self.modele.queue_resultats_tirages[0])
                gain_reel, mise = self.table_roulette_view.widget_central_table_roulette.main_window.modele.mettre_banque_a_jour()

                if mise > 0:
                    self.table_roulette_view.widget_central_table_roulette.widget_table_roulette.animer_label_gain(gain_reel)
        else:
            QMessageBox.critical(self.table_roulette_view.widget_central_table_roulette, 'Erreur',
                                 f"Mise de jetons supérieure au solde de la banque (={self.modele.banque})")


class WidgetBoutonRejouerMise(QWidget):

    def __init__(self, table_roulette_view):
        super(QWidget, self).__init__(table_roulette_view)
        self.table_roulette_view = table_roulette_view
        layout = QHBoxLayout(self)
        self.btn_tourner = QPushButton()
        self.btn_tourner.clicked.connect(self.clicked)
        self.btn_tourner.setStyleSheet(CSS.css_bouton_rejouer_mise)
        self.scene = self.table_roulette_view.scene
        self.modele = self.table_roulette_view.widget_central_table_roulette.main_window.modele

        #self.setAttribute(Qt.WA_StyledBackground, True)
        #self.setStyleSheet('background-color: yellow;')
        self.setFixedSize(45, 60)

        layout.addWidget(self.btn_tourner)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)

    def clicked(self):
        if len(self.table_roulette_view.scene.historique_dic_jeton) > 0:
            self.table_roulette_view.scene.effacer_tous_les_jetons()
            self.table_roulette_view.scene.dic_jeton = copy(self.table_roulette_view.scene.historique_dic_jeton[0])
            self.table_roulette_view.scene.placer_jetons_du_dic_jetons()
            self.table_roulette_view.scene.curseur_historique_dic_jeton += 1


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
