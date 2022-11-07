#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author : Jean-Alexis HERMEL
# Date : 11/10/2022

from Vue.constantes import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class ItemJeton(QGraphicsPixmapItem):

    def __init__(self, table_roulette_scene, x, y, liste_numeros_concernes, valeur=1):
        super().__init__()
        self.table_roulette_scene = table_roulette_scene

        self.position_jeton = (x, y)  # position théorique du jeton
        self.valeur = valeur  # valeur du jeton
        self.liste_numeros_concernes = liste_numeros_concernes

        self.taille_jeton = self.table_roulette_scene.table_roulette_view.taille_jeton
        self.jeton_bleu_1 = None
        self.jeton_jaune_5 = None
        self.jeton_rouge_10 = None
        self.jeton_vert_25 = None
        self.jeton_violet_50 = None

        self.textItem = None  # texte du jeton

        self.set_couleur_jeton()
        self.table_roulette_scene.addItem(self)
        self.coordonnees = (x - self.sceneBoundingRect().width() // 2, y - self.sceneBoundingRect().height() // 2)
        self.setPos(self.coordonnees[0], self.coordonnees[1])  # pour placer le centre image

        #print(x, y, ": Coordonnes théorique de l'item jeton")
        #print(int(self.pos().x()), int(self.pos().y()), ": Coordonnes de l'item jeton")

    def set_couleur_jeton(self):
        taille_texte = 5
        if 1 <= self.valeur < 5:
            self.jeton_bleu_1 = QPixmap(trouver_image_ressources("jeton_bleu.png"))
            self.setPixmap(self.jeton_bleu_1.scaled(self.taille_jeton, self.taille_jeton, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            taille_texte = 10
        elif 5 <= self.valeur < 10:
            self.jeton_jaune_5 = QPixmap(trouver_image_ressources("jeton_jaune.png"))
            self.setPixmap(self.jeton_jaune_5.scaled(self.taille_jeton, self.taille_jeton, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            taille_texte = 8
        elif 10 <= self.valeur < 25:
            self.jeton_rouge_10 = QPixmap(trouver_image_ressources("jeton_rouge.png"))
            self.setPixmap(self.jeton_rouge_10.scaled(self.taille_jeton, self.taille_jeton, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            taille_texte = 8
        elif 25 <= self.valeur < 50:
            self.jeton_vert_25 = QPixmap(trouver_image_ressources("jeton_vert.png"))
            self.setPixmap(self.jeton_vert_25.scaled(self.taille_jeton, self.taille_jeton, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            taille_texte = 8
        elif 50 <= self.valeur:
            self.jeton_violet_50 = QPixmap(trouver_image_ressources("jeton_violet.png"))
            self.setPixmap(self.jeton_violet_50.scaled(self.taille_jeton, self.taille_jeton, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            taille_texte = 8

            if 100 <= self.valeur < 1000:
                taille_texte = 6
            elif self.valeur >= 1000:
                taille_texte = 5
                self.valeur = 1000

        self.textItem = QGraphicsSimpleTextItem(str(self.valeur), self)
        self.textItem.setFont(QFont('Terminus', taille_texte, QFont.Bold))
        self.textItem.setBrush(QBrush(QColor(40, 40, 40, 255), Qt.SolidPattern))
        rect = self.textItem.boundingRect()
        rect.moveCenter(self.boundingRect().center())
        self.textItem.setPos(rect.topLeft())
        self.textItem.setActive(False)

    def redessiner(self):
        self.table_roulette_scene.addItem(self)


class Helper(QObject):
    messageSignal = pyqtSignal(int)


class ItemCase(QGraphicsPolygonItem):

    def __init__(self, table_roulette_view, x, y, taille_case, numero):
        super(ItemCase, self).__init__()
        self.helper = Helper()
        self.helper.messageSignal.connect(self.stop_animation_case)
        self.numero = numero
        self.table_roulette_view = table_roulette_view

        self.coordonnees = []

        self.timer = QTimer()  # pour acutualiser le temps barre de status 5ms
        self.timer.setInterval(250)
        self.timer.timeout.connect(self.animation_case)
        self.nombre_clignotement = 7

        if self.table_roulette_view.widget_central_table_roulette.main_window.modele.jeu[str(self.numero)][0] == "red":
            self.couleur = "rouge"
        elif self.table_roulette_view.widget_central_table_roulette.main_window.modele.jeu[str(self.numero)][0] == "black":
            self.couleur = "noir"
        else:
            self.couleur = "vert"

        self.couleur_de_base = self.couleur

        carre = QPolygonF([
            QPointF(x, y),
            QPointF(x, y + taille_case),
            QPointF(x + taille_case, y + taille_case),
            QPointF(x + taille_case, y),
        ])
        rectangle_long = QPolygonF([
            QPointF(x, y),
            QPointF(x, y + taille_case),
            QPointF(x + taille_case * 4, y + taille_case),
            QPointF(x + taille_case * 4, y),
        ])
        rectangle_court = QPolygonF([
            QPointF(x, y),
            QPointF(x, y + taille_case),
            QPointF(x + taille_case * 2, y + taille_case),
            QPointF(x + taille_case * 2, y),
        ])
        zero = QPolygonF([
            QPointF(x + taille_case/2, y),
            QPointF(x, y + taille_case * 1.5),
            QPointF(x + taille_case/2, y + taille_case * 3),
            QPointF(x + taille_case, y + taille_case * 3),
            QPointF(x + taille_case, y)
        ])

        if numero in ["1st 12", "2nd 12", "3rd 12"]:
            polygone = rectangle_long
            self.coordonnees = [(x, y), (x + taille_case * 4, y + taille_case)]
        elif numero in ['1 to 18', "19 to 36", "PAIR", "IMPAIR", 'ROUGE', "NOIR"]:
            polygone = rectangle_court
            self.coordonnees = [(x, y), (x + taille_case * 2, y + taille_case)]
        elif numero == "0":
            polygone = zero
            self.coordonnees = [(x, y), (x + taille_case, y + taille_case * 3)]
        else:
            polygone = carre
            self.coordonnees = [(x, y), (x + taille_case, y + taille_case)]

        if self.couleur == "rouge":
            self.brush = QBrush(ROUGE, Qt.SolidPattern)
        elif self.couleur == "noir":
            self.brush = QBrush(NOIR, Qt.SolidPattern)
        else:
            self.brush = QBrush(VERT, Qt.SolidPattern)

        self.pen = QPen(CREME_CLAIR, Qt.SolidLine)
        self.pen.setWidth(5)
        self.pen.setJoinStyle(Qt.MiterJoin)

        self.setPolygon(polygone)
        self.setBrush(self.brush)
        self.setPen(self.pen)

        self.textItem = QGraphicsSimpleTextItem(str(self.numero), self)
        self.textItem.setFont(QFont('Roboto', 20, QFont.Bold))
        self.textItem.setBrush(QBrush(CREME, Qt.SolidPattern))
        rect = self.textItem.boundingRect()
        rect.moveCenter(self.boundingRect().center())
        self.textItem.setPos(rect.topLeft())
        self.textItem.setEnabled(False)

        self.setAcceptHoverEvents(True)

    def run_animation_case(self):
        self.timer.start()
        self.table_roulette_view.scene.animation_clignottement_en_cours = True

    def stop_animation_case(self):

        self.timer.stop()
        self.nombre_clignotement = 7

        if self.couleur_de_base == "rouge":
            self.brush = QBrush(ROUGE, Qt.SolidPattern)
            self.couleur = "rouge"

        elif self.couleur_de_base == "vert":
            self.brush = QBrush(VERT, Qt.SolidPattern)
            self.couleur = "vert"

        elif self.couleur_de_base == "noir":
            self.brush = QBrush(NOIR, Qt.SolidPattern)
            self.couleur = "noir"

        self.textItem.setBrush(QBrush(CREME, Qt.SolidPattern))
        self.setBrush(self.brush)
        self.table_roulette_view.scene.animation_clignottement_en_cours = False
        self.table_roulette_view.scene.effacer_tous_les_jetons()

    def animation_case(self):

        if self.couleur == "or":
            if self.couleur_de_base == "noir":
                self.brush = QBrush(NOIR, Qt.SolidPattern)
                self.couleur = "noir"

            elif self.couleur_de_base == "rouge":
                self.brush = QBrush(ROUGE, Qt.SolidPattern)
                self.couleur = "rouge"

            elif self.couleur_de_base == "vert":
                self.brush = QBrush(VERT, Qt.SolidPattern)
                self.couleur = "vert"

            self.textItem.setBrush(QBrush(CREME, Qt.SolidPattern))
        else:
            self.textItem.setBrush(QBrush(NOIR_CLAIR, Qt.SolidPattern))
            self.brush = QBrush(OR, Qt.SolidPattern)
            self.couleur = "or"

        self.setBrush(self.brush)
        self.nombre_clignotement -= 1

        if self.nombre_clignotement == 0:
            self.helper.messageSignal.emit(1)


class ItemCaseGain(QGraphicsPolygonItem):
    def __init__(self, table_roulette_view, x, y, taille_case, numero, valeur_gain):
        super(ItemCaseGain, self).__init__()
        self.numero = numero
        self.table_roulette_view = table_roulette_view

        self.valeur_gain = valeur_gain

        shift_vers_bas = 7
        shift_vers_droite = 4
        carre = QPolygonF([
            QPointF(x + int((1/6) * taille_case), y + shift_vers_bas),
            QPointF(x + int((1/6) * taille_case), y + int(taille_case*(2/9)) + shift_vers_bas),
            QPointF(x + int((5/6) * taille_case), y + int(taille_case*(2/9)) + shift_vers_bas),
            QPointF(x + int((5/6) * taille_case), y + shift_vers_bas),
        ])
        zero = QPolygonF([
            QPointF(x + int((1 / 6) * taille_case) + shift_vers_droite, y + taille_case + shift_vers_bas),
            QPointF(x + int((1 / 6) * taille_case) + shift_vers_droite, y + taille_case + int(taille_case * (2 / 9)) + shift_vers_bas),
            QPointF(x + int((5 / 6) * taille_case) + shift_vers_droite, y + taille_case + int(taille_case * (2 / 9)) + shift_vers_bas),
            QPointF(x + int((5 / 6) * taille_case) + shift_vers_droite, y + taille_case + shift_vers_bas),
        ])

        if numero == "0":
            polygone = zero
        else:
            polygone = carre

        brush = QBrush(GRIS_MAIN, Qt.SolidPattern)
        pen = QPen(OR, Qt.SolidLine)
        pen.setWidth(2)
        pen.setJoinStyle(Qt.MiterJoin)

        self.setPolygon(polygone)
        self.setBrush(brush)
        self.setPen(pen)

        if str(self.valeur_gain) != "0":
            if 0 <= float(valeur_gain) < 100:
                taille_font = 8
            elif 100 <= float(valeur_gain) < 1000:
                taille_font = 7
            else:
                taille_font = 7

            self.textItem = QGraphicsSimpleTextItem(str(self.valeur_gain), self)
            #self.textItem.setOpacity(1)
            self.textItem.setFont(QFont('Roboto', taille_font, QFont.Bold))
            self.textItem.setBrush(QBrush(OR, Qt.SolidPattern))
            rect = self.textItem.boundingRect()
            rect.moveCenter(self.boundingRect().center())
            self.textItem.setPos(rect.topLeft())
            self.textItem.setEnabled(False)

        self.setOpacity(0.9)


class ItemRoue(QGraphicsItemGroup):

    def __init__(self, table_roulette_view):
        super(ItemRoue, self).__init__()
        self.table_roulette_view = table_roulette_view
        self.modele = self.table_roulette_view.widget_central_table_roulette.main_window.modele

        self.dic_item_case_roue = {}  # stock les items case roue

        angle = 0

        pen = QPen(CREME_CLAIR, Qt.SolidLine)
        pen.setWidth(2)
        pen.setJoinStyle(Qt.MiterJoin)

        for numero in self.table_roulette_view.widget_central_table_roulette.main_window.modele.roue:

            brush = QBrush(VERT, Qt.SolidPattern)
            match self.modele.jeu[numero][0]:
                case "red":
                    brush = QBrush(ROUGE, Qt.SolidPattern)
                case "black":
                    brush = QBrush(NOIR, Qt.SolidPattern)

            case_roue = QGraphicsEllipseItem(1060, 230, 300, 300)
            case_roue.setStartAngle(angle)
            case_roue.setSpanAngle(156)  # 2pi = 360*16 -> (360*16/37)
            case_roue.setBrush(brush)
            case_roue.setPen(pen)

            textItem = QGraphicsSimpleTextItem(str(numero))
            textItem.setParentItem(case_roue)
            textItem.setRotation(angle)
            textItem.setFont(QFont('Roboto', 6, QFont.Bold))
            textItem.setBrush(QBrush(CREME, Qt.SolidPattern))
            center = case_roue.boundingRect().center()
            textItem.setPos(center.x(), center.y())

            self.addToGroup(textItem)


            self.dic_item_case_roue[numero] = case_roue
            self.addToGroup(self.dic_item_case_roue[numero])
            angle += 156

        cache_roue = QGraphicsEllipseItem(1110, 280, 200, 200)
        cache_roue.setStartAngle(0)
        cache_roue.setSpanAngle(360 * 16)
        cache_roue.setBrush(QBrush(GRIS_MAIN, Qt.SolidPattern))
        pen_cache_roue = QPen(CREME_CLAIR, Qt.SolidLine)
        pen_cache_roue.setWidth(3)
        pen_cache_roue.setJoinStyle(Qt.MiterJoin)
        cache_roue.setPen(pen_cache_roue)
        #self.addToGroup(cache_roue)

