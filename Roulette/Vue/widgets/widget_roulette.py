#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author : Jean-Alexis HERMEL
# Date : 11/10/2022

from Vue.items.item_roulette import *
from Vue.widgets.widget_bouttons import *
from Vue.widgets.widget_label import *
from Vue.constantes import *
from collections import deque
from copy import copy
from PyQt5.QtGui import *


class WidgetHistoriqueTirages(QWidget):

    def __init__(self, widget_central_table_roulette):
        super(QWidget, self).__init__(widget_central_table_roulette)
        self.widget_central_table_roulette = widget_central_table_roulette
        self.setFixedSize(30 * 38, 33)

        self.layout_h_central = QHBoxLayout(self)
        self.layout_h_central.setContentsMargins(0, 3, 0, 0)
        self.layout_h_central.setSpacing(0)

        self.layout_h_gauche = QHBoxLayout(self)
        self.layout_h_gauche.setSpacing(0)
        self.btn_vers_gauche_simple = QPushButton("<")
        self.btn_vers_gauche_simple.setFixedSize(30, 30)
        self.btn_vers_gauche_simple.setStyleSheet(CSS.css_bouton_afficher_gains)
        self.btn_vers_gauche_simple.clicked.connect(self.decalage_gauche_simple)
        self.btn_vers_gauche_rapide = QPushButton("<<")
        self.btn_vers_gauche_rapide.setFixedSize(30, 30)
        self.btn_vers_gauche_rapide.setStyleSheet(CSS.css_bouton_afficher_gains)
        self.btn_vers_gauche_rapide.clicked.connect(self.actualiser_historique)
        self.layout_h_gauche.addWidget(self.btn_vers_gauche_rapide, alignment=(Qt.AlignLeft | Qt.AlignVCenter))
        self.layout_h_gauche.addWidget(self.btn_vers_gauche_simple, alignment=(Qt.AlignLeft | Qt.AlignVCenter))

        self.layout_h_droite = QHBoxLayout(self)
        self.layout_h_droite.setSpacing(0)
        self.btn_vers_droite_simple = QPushButton(">")
        self.btn_vers_droite_simple.setFixedSize(30, 30)
        self.btn_vers_droite_simple.setStyleSheet(CSS.css_bouton_afficher_gains)
        self.btn_vers_droite_simple.clicked.connect(self.decalage_droite_simple)
        self.btn_vers_droite_rapide = QPushButton(">>")
        self.btn_vers_droite_rapide.setFixedSize(30, 30)
        self.btn_vers_droite_rapide.setStyleSheet(CSS.css_bouton_afficher_gains)
        self.btn_vers_droite_rapide.clicked.connect(self.decalage_droite_rapide)
        self.layout_h_droite.addWidget(self.btn_vers_droite_simple, alignment=(Qt.AlignVCenter | Qt.AlignRight))
        self.layout_h_droite.addWidget(self.btn_vers_droite_rapide, alignment=(Qt.AlignVCenter | Qt.AlignRight))

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(50, 0, 50, 0)
        self.layout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        self.layout_h_central.addLayout(self.layout_h_gauche)
        self.layout_h_central.addLayout(self.layout)
        self.layout_h_central.addLayout(self.layout_h_droite)
        self.layout_h_central.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)

        self.setLayout(self.layout_h_central)

        self.nombre_case_a_afficher = 25
        self.valeur_decalage_droite_simple = 0

        for i in range(0, 500):
            self.widget_central_table_roulette.main_window.modele.lancer_tirage()
        self.actualiser_historique()

    def afficher_cases(self, nombre):
        case = QLabel(str(nombre))
        case.setFixedSize(30, 30)
        case.setStyleSheet(CSS.css_style_case_historique_tirage(nombre, self.widget_central_table_roulette.main_window.modele))
        case.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.layout.addWidget(case)

    def actualiser_historique(self):
        self.valeur_decalage_droite_simple = 0

        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)

        nombre_cases_affichees = 0
        for nombre in self.widget_central_table_roulette.main_window.modele.queue_resultats_tirages:
            if nombre_cases_affichees < self.nombre_case_a_afficher:
                self.afficher_cases(nombre)
                nombre_cases_affichees += 1

    def decalage_droite_simple(self):
        if len(self.widget_central_table_roulette.main_window.modele.queue_resultats_tirages) > self.nombre_case_a_afficher:
            if (len(self.widget_central_table_roulette.main_window.modele.queue_resultats_tirages) - self.valeur_decalage_droite_simple) > self.nombre_case_a_afficher:

                self.valeur_decalage_droite_simple += 1

                for i in reversed(range(self.layout.count())):
                    self.layout.itemAt(i).widget().setParent(None)

                curseur_queue = 0
                nombre_cases_affichees = 0
                for nombre in self.widget_central_table_roulette.main_window.modele.queue_resultats_tirages:
                    curseur_queue += 1
                    if curseur_queue > self.valeur_decalage_droite_simple:
                        if nombre_cases_affichees < self.nombre_case_a_afficher:
                            self.afficher_cases(nombre)
                            nombre_cases_affichees += 1

    def decalage_gauche_simple(self):
        if len(self.widget_central_table_roulette.main_window.modele.queue_resultats_tirages) > self.nombre_case_a_afficher:

            if self.valeur_decalage_droite_simple != 0:
                self.valeur_decalage_droite_simple -= 1

            for i in reversed(range(self.layout.count())):
                self.layout.itemAt(i).widget().setParent(None)

            curseur_queue = 0
            nombre_cases_affichees = 0
            for nombre in self.widget_central_table_roulette.main_window.modele.queue_resultats_tirages:
                curseur_queue += 1
                if curseur_queue > self.valeur_decalage_droite_simple:
                    if nombre_cases_affichees < self.nombre_case_a_afficher:
                        self.afficher_cases(nombre)
                        nombre_cases_affichees += 1

    def decalage_droite_rapide(self):
        if len(self.widget_central_table_roulette.main_window.modele.queue_resultats_tirages) > self.nombre_case_a_afficher:

            self.valeur_decalage_droite_simple = (len(self.widget_central_table_roulette.main_window.modele.queue_resultats_tirages) - self.nombre_case_a_afficher)
            for i in reversed(range(self.layout.count())):
                self.layout.itemAt(i).widget().setParent(None)

            curseur_queue = 0
            nombre_cases_affichees = 0
            for nombre in self.widget_central_table_roulette.main_window.modele.queue_resultats_tirages:
                curseur_queue += 1
                if curseur_queue > (len(self.widget_central_table_roulette.main_window.modele.queue_resultats_tirages) - self.nombre_case_a_afficher):
                    if nombre_cases_affichees < self.nombre_case_a_afficher:
                        self.afficher_cases(nombre)
                        nombre_cases_affichees += 1


class WidgetSelectionJeton(QWidget):

    def __init__(self, widget_central_table_roulette):
        super(QWidget, self).__init__(widget_central_table_roulette)
        self.widget_central_table_roulette = widget_central_table_roulette
        layout = QHBoxLayout(self)
        self.taille_jeton = self.widget_central_table_roulette.widget_table_roulette.taille_jeton + 10

        self.jeton_bleu_1 = WidgetBoutonJeton(self, 1, "bleu", self.taille_jeton)
        self.jeton_jaune_5 = WidgetBoutonJeton(self, 5, "jaune", self.taille_jeton)
        self.jeton_rouge_10 = WidgetBoutonJeton(self, 10, "rouge", self.taille_jeton)
        self.jeton_vert_25 = WidgetBoutonJeton(self, 25, "vert", self.taille_jeton)
        self.jeton_violet_50 = WidgetBoutonJeton(self, 50, "violet", self.taille_jeton)

        layout.addWidget(self.jeton_bleu_1)
        layout.addWidget(self.jeton_jaune_5)
        layout.addWidget(self.jeton_rouge_10)
        layout.addWidget(self.jeton_vert_25)
        layout.addWidget(self.jeton_violet_50)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)
        #self.setAttribute(Qt.WA_StyledBackground, True)
        # self.setStyleSheet('background-color: red;')

    def reinitialiser_grand_jetons(self):
        self.jeton_bleu_1.bouton_jeton.setStyleSheet(CSS.css_style_jeton(self.jeton_bleu_1.couleur, "grand"))
        self.jeton_jaune_5.bouton_jeton.setStyleSheet(CSS.css_style_jeton(self.jeton_jaune_5.couleur, "grand"))
        self.jeton_rouge_10.bouton_jeton.setStyleSheet(CSS.css_style_jeton(self.jeton_rouge_10.couleur, "grand"))
        self.jeton_vert_25.bouton_jeton.setStyleSheet(CSS.css_style_jeton(self.jeton_vert_25.couleur, "grand"))
        self.jeton_violet_50.bouton_jeton.setStyleSheet(CSS.css_style_jeton(self.jeton_violet_50.couleur, "grand"))


class WidgetCentralTableRoulette(QWidget):

    def __init__(self, table_widget):
        super(QWidget, self).__init__(table_widget)
        self.main_window = table_widget.main_window

        #self.setFixedHeight(700)
        self.installEventFilter(self)
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setContentsMargins(0, 40, 0, 0)
        self.grid_layout.setVerticalSpacing(0)
        self.grid_layout.setHorizontalSpacing(2)
        self.grid_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.widget_table_roulette = TableRouletteView(self)
        self.widget_bouton_effacer_jetons = WidgetBoutonEffacerJetons(self)
        self.widget_selection_jeton = WidgetSelectionJeton(self)
        self.widget_bouton_montrer_gains_cases = WidgetBoutonMontrerGainsCases(self)
        self.widget_boutons_historique_jetons = WidgetBoutonsHistoriqueJetons(self)
        self.widget_label_banque_mise = WidgetLabelBanqueMise(self)
        self.widget_historique_tirage = WidgetHistoriqueTirages(self)

        self.grid_layout.addWidget(self.widget_bouton_effacer_jetons, 2, 1, 2, 2, alignment=(Qt.AlignTop | Qt.AlignLeft))
        self.grid_layout.addWidget(self.widget_selection_jeton, 2, 3, 2, 2,alignment=(Qt.AlignTop | Qt.AlignLeft))
        self.grid_layout.addWidget(self.widget_bouton_montrer_gains_cases, 2, 5, 2, 1, alignment=(Qt.AlignTop | Qt.AlignLeft))
        self.grid_layout.addWidget(self.widget_boutons_historique_jetons, 2, 7, 1, 1, alignment=(Qt.AlignTop | Qt.AlignLeft))
        self.grid_layout.addWidget(self.widget_label_banque_mise, 2, 8, 2, 1, alignment=(Qt.AlignTop | Qt.AlignLeft))
        self.grid_layout.addWidget(self.widget_table_roulette, 4, 1, 10, 21, alignment=(Qt.AlignTop | Qt.AlignHCenter))

        self.v_layout = QVBoxLayout(self)
        self.v_layout.setSpacing(0)
        self.v_layout.setStretch(1, 1)

        self.v_layout.addLayout(self.grid_layout)
        self.v_layout.addWidget(self.widget_historique_tirage, alignment=(Qt.AlignTop | Qt.AlignHCenter))

        self.v_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.v_layout.setContentsMargins(100, 100, 100, 100)

        self.setLayout(self.v_layout)

    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseButtonPress:
            return False  # propage event aux items au-dessus
        else:
            return False


class TableRouletteScene(QGraphicsScene):
    def __init__(self, table_roulette_view):
        super().__init__(table_roulette_view)
        self.setSceneRect(-10, -10, 1380, 545)
        self.table_roulette_view = table_roulette_view
        self.modele = self.table_roulette_view.widget_central_table_roulette.main_window.modele
        self.installEventFilter(self)

        self.dic_jeton = {}  # contient l'état actuel des mises de jetons sur la table
        self.nombre_historique_dic_jeton = 0  # nombre actuel de positions sauvegardées (10 max)
        self.historique_dic_jeton = deque(maxlen=100)  # sauvegarde de l'historique des mises effectuées et tirées
        self.curseur_historique_dic_jeton = 0  # curseur permettant de naviguer dans l'historique de dic jetons

        self.valeur_ajout_jeton = 1  # valeur par defaut, change selon mise selectionnee
        self.animation_clignottement_en_cours = False

    def eventFilter(self, source, event):
        """ Filtre les élements concernant la scène"""
        if event.type() == QEvent.GraphicsSceneWheel:
            return False  # propage event aux items au-dessus

        elif event.type() == QEvent.GraphicsSceneMouseDoubleClick:
            return False  # propage event aux items au-dessus

        elif event.type() == QEvent.GraphicsSceneMousePress:
            if (not self.animation_clignottement_en_cours) and (not self.table_roulette_view.animation_label_gain_en_cours):

                if qApp.mouseButtons() == Qt.RightButton:
                    self.mousePressEvent_right(event)
                    self.mise_a_jour_label_banque_mise()
                    return False  # propage event aux items au dessus

                elif qApp.mouseButtons() == Qt.LeftButton:
                    self.mousePressEvent_left(event)
                    self.mise_a_jour_label_banque_mise()
                    return False  # propage event aux items au dessus

                else:
                    return False
            else:
                return False

        elif event.type() == QEvent.GraphicsSceneMouseMove:
            if self.table_roulette_view.widget_central_table_roulette.widget_bouton_montrer_gains_cases.btn_montrer_gains.isChecked():
                self.mouseMoveEvent_(event)
            return False  # propage event aux items au dessus
        else:
            return False

    def ajouter_pattern_historique_mise(self):
        """Sauvegarde la mise des jetons actuelle dans la queue d'historique"""
        self.historique_dic_jeton.appendleft(copy(self.dic_jeton))

    def placer_jetons_du_dic_jetons(self):
        print_dic(self.dic_jeton)
        for pos, jeton in self.dic_jeton.items():
            jeton.redessiner()

            # écrit ou réécrit la valeur de la mise pour un groupe de cases
            self.modele.dic_des_mises[hash_liste_numeros_concernes(jeton.liste_numeros_concernes)] = {
                "mise": jeton.valeur,
                "cases": jeton.liste_numeros_concernes
            }
            self.modele.transformer_dic_des_mises()  # change les cases non-numéro en liste de numéros
            for key, value in self.modele.dic_des_mises.items():
                prGreen(f"{key}: mise: {value['mise']}    {value['cases']}")

        self.mise_a_jour_label_banque_mise()

    def mousePressEvent_left(self, event):
        x = int(event.scenePos().x())
        y = int(event.scenePos().y())
        liste_numeros = self.trouver_cases(x, y)
        liste_numeros_concernes = self.filtrer_liste_items_concernes(sorted(liste_numeros))
        liste_numeros_concernes = self.filtrer_liste_numeros_concernes(liste_numeros_concernes)

        #print(x, y, "Pos scene")

        if not self.modele.is_mise_avec_banque_positive(self.valeur_ajout_jeton):
            if len(liste_numeros_concernes) != 0:  # si on n'est pas dans un cas où on ne peut pas poser de jeton
                x_jeton, y_jeton = self.trouver_position_jeton(liste_numeros_concernes)

                # on cherche s'il y a deja un jeton à cet endroit dans le dictionnaire de position de jeton
                jeton_existant = False
                for position_jeton in self.dic_jeton.keys():
                    if position_jeton == str((x_jeton, y_jeton)):
                        jeton_existant = True

                if not jeton_existant:
                    jeton = ItemJeton(self, x_jeton, y_jeton, liste_numeros_concernes, self.valeur_ajout_jeton)
                    self.dic_jeton[str(jeton.position_jeton)] = jeton
                    nouvelle_valeur_jeton = jeton.valeur
                else:
                    jeton_trouve = self.dic_jeton[str((x_jeton, y_jeton))]
                    valeur_jeton = jeton_trouve.valeur
                    self.removeItem(jeton_trouve)
                    del self.dic_jeton[str((x_jeton, y_jeton))]

                    nouvelle_valeur_jeton = valeur_jeton + self.valeur_ajout_jeton
                    jeton = ItemJeton(self, x_jeton, y_jeton, liste_numeros_concernes, nouvelle_valeur_jeton)
                    self.dic_jeton[str(jeton.position_jeton)] = jeton

                # écrit ou réécrit la valeur de la mise pour un groupe de cases
                self.modele.dic_des_mises[hash_liste_numeros_concernes(liste_numeros_concernes)] = {
                    "mise": nouvelle_valeur_jeton,
                    "cases": liste_numeros_concernes
                }
                self.modele.transformer_dic_des_mises()  # change les cases non-numéro en liste de numéros
                for key, value in self.modele.dic_des_mises.items():
                    prGreen(f"{key}: mise: {value['mise']}    {value['cases']}")

        else:
            QMessageBox.critical(self.table_roulette_view.widget_central_table_roulette,'Erreur',
                                 f"Mise de {self.valeur_ajout_jeton} supérieure au solde de la banque (={self.modele.banque})")

    def mousePressEvent_right(self, event):
        x = int(event.scenePos().x())
        y = int(event.scenePos().y())
        liste_numeros = self.trouver_cases(x, y)
        liste_numeros_concernes = self.filtrer_liste_items_concernes(sorted(liste_numeros))
        liste_numeros_concernes = self.filtrer_liste_numeros_concernes(liste_numeros_concernes)

        if len(liste_numeros_concernes) != 0:  # si on n'est pas dans un cas où on ne peut pas poser de jeton
            x_jeton, y_jeton = self.trouver_position_jeton(liste_numeros_concernes)

            # on cherche s'il y a deja un jeton à cet endroit dans le dictionnaire de position de jeton
            jeton_existant = False
            for position_jeton in self.dic_jeton.keys():
                if position_jeton == str((x_jeton, y_jeton)):
                    jeton_existant = True

            if jeton_existant:
                jeton_trouve = self.dic_jeton[str((x_jeton, y_jeton))]
                self.removeItem(jeton_trouve)                 # efface le jeton graphiquement
                del self.dic_jeton[str((x_jeton, y_jeton))]   # efface le jeton de son dic gestionnaire
                del self.modele.dic_des_mises[hash_liste_numeros_concernes(liste_numeros_concernes)]  # efface la mise du modele

    def mouseMoveEvent_(self, event):
        if not self.animation_clignottement_en_cours:
            x = int(event.scenePos().x())
            y = int(event.scenePos().y())
            liste_numeros = self.trouver_cases(x, y)
            liste_numeros_concernes = self.filtrer_liste_items_concernes(sorted(liste_numeros))

            for numero_a_surligner in liste_numeros_concernes:
                for item in self.items():
                    if "ItemCase" in str(type(item)):
                        if numero_a_surligner == item.numero:
                            if self.table_roulette_view.widget_central_table_roulette.main_window.modele.jeu[numero_a_surligner][0] == "black":
                                brush = QBrush(NOIR_CLAIR, Qt.SolidPattern)
                                item.setOpacity(50)
                            elif self.table_roulette_view.widget_central_table_roulette.main_window.modele.jeu[numero_a_surligner][0] == "red":
                                brush = QBrush(ROUGE_CLAIR, Qt.SolidPattern)
                            else:
                                brush = QBrush(VERT_CLAIR, Qt.SolidPattern)
                            item.setBrush(brush)
                            item.textItem.setBrush(QBrush(OR, Qt.SolidPattern))

            for item in self.items():
                if "ItemCase" in str(type(item)):
                    if item.numero not in liste_numeros_concernes or (-10 <= x <= 10) or (-10 <= y <= 10) or (1110 <= x <= 1140) or (390 <= y <= 420):

                        if self.table_roulette_view.widget_central_table_roulette.main_window.modele.jeu[item.numero][0] == "black":
                            brush = QBrush(NOIR, Qt.SolidPattern)

                        elif self.table_roulette_view.widget_central_table_roulette.main_window.modele.jeu[item.numero][0] == "red":
                            brush = QBrush(ROUGE, Qt.SolidPattern)

                        else:
                            brush = QBrush(VERT, Qt.SolidPattern)

                        item.setBrush(brush)
                        item.textItem.setBrush(QBrush(CREME, Qt.SolidPattern))

    def mise_a_jour_label_banque_mise(self):
        self.table_roulette_view.widget_central_table_roulette.widget_label_banque_mise.update_label_banque()
        self.table_roulette_view.widget_central_table_roulette.widget_label_banque_mise.update_label_mise()

    def filtrer_liste_numeros_concernes(self, liste_numeros_concernes):
        """supprime les digits lorsque les mises sont des chances multiples"""
        if '1st 12' in liste_numeros_concernes and '2nd 12' in liste_numeros_concernes:
            liste_numeros_concernes = ['1st 12', '2nd 12']
        elif '2nd 12' in liste_numeros_concernes and '3rd 12' in liste_numeros_concernes:
            liste_numeros_concernes = ['2nd 12', '3rd 12']
        elif '1st' in liste_numeros_concernes and '2nd' in liste_numeros_concernes:
            liste_numeros_concernes = ['1st', '2nd']
        elif '2nd' in liste_numeros_concernes and '3rd' in liste_numeros_concernes:
            liste_numeros_concernes = ['2nd', '3rd']

        elif '1st 12' in liste_numeros_concernes:
            liste_numeros_concernes = ['1st 12']
        elif '2nd 12' in liste_numeros_concernes:
            liste_numeros_concernes = ['2nd 12']
        elif '3rd 12' in liste_numeros_concernes:
            liste_numeros_concernes = ['3rd 12']
        elif '1st' in liste_numeros_concernes:
            liste_numeros_concernes = ['1st']
        elif '2nd' in liste_numeros_concernes:
            liste_numeros_concernes = ['2nd']
        elif '3rd' in liste_numeros_concernes:
            liste_numeros_concernes = ['3rd']

        elif '1 to 18' in liste_numeros_concernes:
            liste_numeros_concernes = ['1 to 18']
        elif '19 to 36' in liste_numeros_concernes:
            liste_numeros_concernes = ['19 to 36']
        elif 'PAIR' in liste_numeros_concernes:
            liste_numeros_concernes = ['PAIR']
        elif 'IMPAIR' in liste_numeros_concernes:
            liste_numeros_concernes = ['IMPAIR']
        elif 'ROUGE' in liste_numeros_concernes:
            liste_numeros_concernes = ['ROUGE']
        elif 'NOIR' in liste_numeros_concernes:
            liste_numeros_concernes = ['NOIR']

        return liste_numeros_concernes

    def trouver_position_jeton(self, liste_numeros_concernes):
        """ Renvoie la position que le jeton doit avoir selon la liste des cases surlignées"""
        min_x, min_y, max_x, max_y = 20000, 20000, 0, 0

        if len(liste_numeros_concernes) != 0:
            item_trouve = None

            for numero_item in liste_numeros_concernes:
                for item in self.items():
                    if "ItemCase" in str(type(item)):
                        if item.numero == numero_item:
                            item_trouve = item

                #print(item_trouve.numero, item_trouve.coordonnees)
                item_x_min = item_trouve.coordonnees[0][0]
                item_y_min = item_trouve.coordonnees[0][1]
                item_x_max = item_trouve.coordonnees[1][0]
                item_y_max = item_trouve.coordonnees[1][1]

                if item_x_min < min_x:
                    min_x = item_x_min
                if item_y_min < min_y:
                    min_y = item_y_min
                if item_x_max > max_x:
                    max_x = item_x_max
                if item_y_max > max_y:
                    max_y = item_y_max

            if liste_numeros_concernes == ['0', '3']:
                x_center = (min_x + max_x) // 2
                y_center = (min_y + max_y) // 6
            elif liste_numeros_concernes == ['0', '2', '3']:
                x_center = (min_x + max_x) // 2
                y_center = int((min_y + max_y) * (1/3))
            elif liste_numeros_concernes == ['0', '1', '2']:
                x_center = (min_x + max_x) // 2
                y_center = int((min_y + max_y) * (2/3))
            elif len(liste_numeros_concernes) == 3:
                x_center = (min_x + max_x) // 2
                y_center = max_y
            elif liste_numeros_concernes == ['0', '1']:
                x_center = (min_x + max_x) // 2
                y_center = int((min_y + max_y) * (5/6))
            elif liste_numeros_concernes == ['0', '1', '2', '3'] or len(liste_numeros_concernes) == 6:
                x_center = (min_x + max_x) // 2
                y_center = max_y

            else:
                x_center = (min_x + max_x) // 2
                y_center = (min_y + max_y) // 2

            return x_center, y_center

    @staticmethod
    def filtrer_liste_items_concernes(liste_items):
        # Premiere douzaine
        if ("1st 12" in liste_items) and (len(liste_items) > 1):
            # 4 premieres triplettes
            if len(liste_items) == 2:
                if "1" in liste_items:
                    liste_items = ['1', '2', '3']
                elif "4" in liste_items:
                    liste_items = ['4', '5', '6']
                elif "7" in liste_items:
                    liste_items = ['7', '8', '9']
                elif "10" in liste_items:
                    liste_items = ['10', '11', '12']
                elif "2nd 12" in liste_items:
                    liste_items = ['1st 12', '2nd 12', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24']
                else:
                    liste_items = []

            elif len(liste_items) == 3:
                if "1" in liste_items and "0" in liste_items:
                    liste_items = ['0', '1', '2', '3']
                elif "1" in liste_items and "4" in liste_items:
                    liste_items = ['1', '2', '3', '4', '5', '6']
                elif "4" in liste_items and "7" in liste_items:
                    liste_items = ['4', '5', '6', '7', '8', '9']
                elif "7" in liste_items and "10" in liste_items:
                    liste_items = ['7', '8', '9', '10', '11', '12']
                else:
                    liste_items = []

            elif len(liste_items) == 4:
                if "10" in liste_items and "13" in liste_items and "2nd 12" in liste_items:
                    liste_items = ['10', '11', '12', '13', '14', '15']
                else:
                    liste_items = []

            else:
                liste_items = []

        elif ("2nd 12" in liste_items) and (len(liste_items) > 1):
            # 4 deuxieme triplettes
            if len(liste_items) == 2:
                if "13" in liste_items:
                    liste_items = ['13', '14', '15']
                elif "16" in liste_items:
                    liste_items = ['16', '17', '18']
                elif "19" in liste_items:
                    liste_items = ['19', '20', '21']
                elif "22" in liste_items:
                    liste_items = ['22', '23', '24']
                elif "3rd 12" in liste_items:
                    liste_items = ['2nd 12', '3rd 12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36']
                else:
                    liste_items = []

            elif len(liste_items) == 3:
                if "13" in liste_items and "16" in liste_items:
                    liste_items = ['13', '14', '15', '16', '17', '18']
                elif "16" in liste_items and "19" in liste_items:
                    liste_items = ['16', '17', '18', '19', '20', '21']
                elif "19" in liste_items and "22" in liste_items:
                    liste_items = ['19', '20', '21', '22', '23', '24']
                else:
                    liste_items = []

            elif len(liste_items) == 4:
                if "22" in liste_items and "25" in liste_items and "3rd 12" in liste_items:
                    liste_items = ['22', '23', '24', '25', '26', '27']
                else:
                    liste_items = []
            else:
                liste_items = []

        elif ("3rd 12" in liste_items) and (len(liste_items) > 1):
            # 4 troisieme triplettes
            if len(liste_items) == 2:
                if "25" in liste_items:
                    liste_items = ['25', '26', '27']
                elif "28" in liste_items:
                    liste_items = ['28', '29', '30']
                elif "31" in liste_items:
                    liste_items = ['31', '32', '33']
                elif "34" in liste_items:
                    liste_items = ['34', '35', '36']
                else:
                    liste_items = []

            elif len(liste_items) == 3:
                if "25" in liste_items and "28" in liste_items:
                    liste_items = ['25', '26', '27', '28', '29', '30']
                elif "28" in liste_items and "31" in liste_items:
                    liste_items = ['28', '29', '30', '31', '32', '33']
                elif "31" in liste_items and "34" in liste_items:
                    liste_items = ['31', '32', '33', '34', '35', '36']
                else:
                    liste_items = []

            else:
                liste_items =[]

        elif len(liste_items) == 2:
            if "1 to 18" in liste_items\
                    or "PAIR" in liste_items\
                    or "ROUGE" in liste_items\
                    or "NOIR" in liste_items\
                    or "IMPAIR" in liste_items\
                    or "19 to 36" in liste_items:
                liste_items = []

            elif "34" in liste_items and "3rd" in liste_items:
                liste_items = []
            elif "35" in liste_items and "2nd" in liste_items:
                liste_items = []
            elif "36" in liste_items and "1st" in liste_items:
                liste_items = []
            elif "1st" in liste_items and '2nd' in liste_items:
                liste_items = ['1st', '2nd', '3', '6', '9', '12', '15', '18', '21', '24', '27', '30', '33', '36', '2', '5', '8', '11', '14', '17', '20', '23', '26', '29', '32', '35']
            elif "2nd" in liste_items and '3rd' in liste_items:
                liste_items = ['2nd', '3rd', '2', '5', '8', '11', '14', '17', '20', '23', '26', '29', '32', '35', '1', '4', '7', '10', '13', '16', '19', '22', '25', '28', '31', '34']

        elif len(liste_items) == 4:
            if "1st" in liste_items or "2nd" in liste_items or "3rd" in liste_items:
                liste_items = []

        elif liste_items == ['1st 12']:
            liste_items = ['1st 12', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']

        elif liste_items == ['2nd 12']:
            liste_items = ['2nd 12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24']

        elif liste_items == ['3rd 12']:
            liste_items = ['3rd 12', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36']

        elif liste_items == ['1st']:
            liste_items = ['1st', '3', '6', '9', '12', '15', '18', '21', '24', '27', '30', '33', '36']

        elif liste_items == ['2nd']:
            liste_items = ['2nd', '2', '5', '8', '11', '14', '17', '20', '23', '26', '29', '32', '35']

        elif liste_items == ['3rd']:
            liste_items = ['3rd', '1', '4', '7', '10', '13', '16', '19', '22', '25', '28', '31', '34']

        elif '1 to 18' in liste_items:
            liste_items = ['1 to 18', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18']
        elif '19 to 36' in liste_items:
            liste_items = ['19 to 36', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36']
        elif 'PAIR' in liste_items:
            liste_items = ['PAIR', '2', '4', '6', '8', '10', '12', '14', '16', '18', '20', '22', '24', '26', '28', '30', '32', '34', '36']
        elif 'IMPAIR' in liste_items:
            liste_items = ['IMPAIR', '1', '3', '5', '7', '9', '11', '13', '15', '17', '19', '21', '23', '25', '27', '29', '31', '33', '35']
        elif 'ROUGE' in liste_items:
            liste_items = ['ROUGE', '1', '3', '5', '7', '9', '12', '14', '16', '18', '19', '21', '23', '25', '27', '30', '32', '34', '36']
        elif 'NOIR' in liste_items:
            liste_items = ['NOIR', '2', '4', '6', '8', '10', '11', '13', '15', '17', '20', '22', '24', '26', '28', '29', '31', '33', '35']

        return liste_items

    def trouver_cases(self, x, y):
        taille_decalage = 10
        liste_items_concernes = []
        liste_points_a_verifier = [(x - taille_decalage, y - taille_decalage),
                                   (x + taille_decalage, y - taille_decalage),
                                   (x + taille_decalage, y + taille_decalage),
                                   (x - taille_decalage, y + taille_decalage)]

        for item in self.items():
            if "ItemCase" in str(type(item)):
                x1 = item.coordonnees[0][0]
                y1 = item.coordonnees[0][1]
                x2 = item.coordonnees[1][0]
                y2 = item.coordonnees[1][1]

                for point_a_verif in liste_points_a_verifier:
                    x_point_verif = point_a_verif[0]
                    y_point_verif = point_a_verif[1]

                    if (x1 <= x_point_verif <= x2) and (y1 <= y_point_verif <= y2):
                        if item not in liste_items_concernes:
                            liste_items_concernes.append(item)

        k = []
        for item_ in liste_items_concernes:
            k.append(item_.numero)
        return k

    def effacer_tous_les_jetons(self):
        """Efface tous les jetons sur le plateau et dans le dictionnaire les référençant"""
        for jeton_pos, jeton_value in list(self.dic_jeton.items()):
            self.removeItem(jeton_value)
            del self.dic_jeton[jeton_pos]
            self.modele.dic_des_mises = {}  # réinitialisation du dic rassemblant les mises

        self.mise_a_jour_label_banque_mise()


class WidgetAnimationeGain(QWidget):
    def __init__(self, table_roulette_view, valeur):
        super().__init__(table_roulette_view)
        layoutH = QHBoxLayout(self)
        self.label = QLabel(valeur)
        self.label.setFixedSize(100, 100)
        layoutH.addWidget(self.label)
        self.label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.setLayout(layoutH)

    def mise_a_jour_text(self, gain):
        if gain >= 0:
            self.label.setText("+ " + str(gain))
        else:
            self.label.setText("- " + str(abs(gain)))
        self.label.setStyleSheet(CSS.css_label_animation_gain(gain))


class TableRouletteView(QGraphicsView):
    def __init__(self, widget_central_table_roulette):
        super().__init__(widget_central_table_roulette)
        self.widget_central_table_roulette = widget_central_table_roulette
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setRenderHint(QPainter.Antialiasing)
        self.installEventFilter(self)
        self.setStyleSheet(CSS.css_table_roulette_view)
        #self.setAttribute(Qt.WA_StyledBackground, True)
        #self.setStyleSheet('background-color: yellow;')
        self.setContentsMargins(0, 0, 0, 0)

        self.label_animation = WidgetAnimationeGain(self, "+13")
        self.label_animation.move(200, 200)
        self.label_animation.hide()
        self.anim = None  # QPropertyAnimation des gains

        self.animation_label_gain_en_cours = False

        self.scene = TableRouletteScene(self)
        self.setScene(self.scene)

        self.dic_item_case_gain = {}   # stock les items cases_gain
        self.dic_item_case = {}        # stock les items case

        self.taille_case = TAILLE_CASE
        self.taille_jeton = TAILLE_JETON
        self.initier_cases()
        self.item_roue = None
        self.initier_roue()


        self.widget_bouton_tourner = WidgetBoutonTourner(self)
        self.widget_bouton_tourner.move(410, 430)

        self.widget_bouton_rejouer_mise = WidgetBoutonRejouerMise(self)
        self.widget_bouton_rejouer_mise.move(740, 430)


        #self.animer_label_gain(13)

    def initier_roue(self):
        self.item_roue = ItemRoue(self)
        self.scene.addItem(self.item_roue)

    def initier_cases(self):
        x = 0
        y = 0
        for numero in self.widget_central_table_roulette.main_window.modele.jeu:
            if numero == "0":
                case = ItemCase(self, x, y, self.taille_case, numero)
                y = 2 * self.taille_case
                x = self.taille_case
            elif numero == "1st 12":
                case = ItemCase(self, self.taille_case, self.taille_case * 3, self.taille_case, numero)
            elif numero == "2nd 12":
                case = ItemCase(self, self.taille_case * 5, self.taille_case * 3, self.taille_case, numero)
            elif numero == "3rd 12":
                case = ItemCase(self, self.taille_case * 9, self.taille_case * 3, self.taille_case, numero)
            elif numero == "1 to 18":
                case = ItemCase(self, self.taille_case, self.taille_case * 4, self.taille_case, numero)
            elif numero == "19 to 36":
                case = ItemCase(self, self.taille_case * 11, self.taille_case * 4, self.taille_case, numero)
            elif numero == "PAIR":
                case = ItemCase(self, self.taille_case * 3, self.taille_case * 4, self.taille_case, numero)
            elif numero == "IMPAIR":
                case = ItemCase(self, self.taille_case * 9, self.taille_case * 4, self.taille_case, numero)
            elif numero == "ROUGE":
                case = ItemCase(self, self.taille_case * 5, self.taille_case * 4, self.taille_case, numero)
            elif numero == "NOIR":
                case = ItemCase(self, self.taille_case * 7, self.taille_case * 4, self.taille_case, numero)
            elif numero == "1st":
                case = ItemCase(self, self.taille_case * 13, 0, self.taille_case, numero)
            elif numero == "2nd":
                case = ItemCase(self, self.taille_case * 13, self.taille_case * 1, self.taille_case, numero)
            elif numero == "3rd":
                case = ItemCase(self, self.taille_case * 13, self.taille_case * 2, self.taille_case, numero)
            else:
                case = ItemCase(self, x, y, self.taille_case, numero)
                y -= self.taille_case
                if int(numero) % 3 == 0:
                    y = (2 * self.taille_case)
                    x += self.taille_case

            self.dic_item_case[str(numero)] = case
            self.scene.addItem(case)

    def initier_cases_gain(self):
        x = 0
        y = 0
        case_gain = None
        for numero in self.widget_central_table_roulette.main_window.modele.jeu:
            if numero == "0":
                valeur_gain = self.widget_central_table_roulette.main_window.modele.calculer_gain_par_case()[str(numero)]
                case_gain = ItemCaseGain(self, x, y, self.taille_case, numero, valeur_gain)
                y = 2 * self.taille_case
                x = self.taille_case
            elif numero in ["1st 12", "2nd 12", "3rd 12", "1 to 18", "19 to 36", "PAIR", "IMPAIR", "ROUGE", "NOIR", "1st", "2nd", "3rd"]:
                pass

            else:
                dic_valeur_gain = self.widget_central_table_roulette.main_window.modele.calculer_gain_par_case()
                valeur_gain = dic_valeur_gain[str(numero)]
                case_gain = ItemCaseGain(self, x, y, self.taille_case, numero, valeur_gain)
                y -= self.taille_case
                if int(numero) % 3 == 0:
                    y = (2 * self.taille_case)
                    x += self.taille_case

            self.dic_item_case_gain[str(numero)] = case_gain
            self.scene.addItem(case_gain)

        #print_dic(dic_valeur_gain)
        #print()

    def stop_animation_label_gain(self):
        self.anim.stop()
        self.label_animation.hide()
        self.animation_label_gain_en_cours = False

    def animer_label_gain(self, gain_reel):
        self.anim = QPropertyAnimation(self.label_animation, b'pos')
        self.anim.setDuration(2700)
        self.anim.setEasingCurve(QEasingCurve(QEasingCurve.OutQuart))
        self.anim.setStartValue(QPoint(507, 0))
        self.anim.setEndValue(QPoint(507, 110))
        self.anim.finished.connect(self.stop_animation_label_gain)
        self.label_animation.show()
        self.animation_label_gain_en_cours = True
        self.label_animation.mise_a_jour_text(gain_reel)
        #self.anim.setTargetObject(self.label_animation)
        self.anim.start()

    def animer_case_tirage(self, numero_tirage):
        if not self.scene.animation_clignottement_en_cours:
            for numero_case, item_case in self.dic_item_case.items():
                if str(numero_tirage) == str(numero_case):
                    item_case.run_animation_case()

    def eventFilter(self, source, event):
        """ filtre les elements concernant la vue"""
        return False  # propage event aux items au dessus