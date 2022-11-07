#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author : Jean-Alexis HERMEL
# Date : 12/10/2022

from Vue.constantes import *
from Modele.outils import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import numpy as np
import matplotlib

matplotlib.use('Qt5Agg')


class WidgetLabelBanqueMise(QWidget):

    def __init__(self, widget_central_table_roulette):
        super(QWidget, self).__init__(widget_central_table_roulette)
        self.widget_central_table_roulette = widget_central_table_roulette
        layoutH = QHBoxLayout(self)

        self.label = QLabel(f"Mise Totale : ")
        self.label.setStyleSheet(CSS.css_label_banque_mise)
        # self.label.setFixedSize(300, 60)
        self.label.setContentsMargins(5, 0, 0, 0)
        self.label.setFixedSize(200, 30)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.label2 = QLabel(f"Banque : ")
        self.label2.setStyleSheet(CSS.css_label_banque_mise)
        self.label2.setFixedSize(190, 30)
        self.label2.setContentsMargins(5, 0, 0, 0)
        self.label2.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        layoutH.addWidget(self.label)
        layoutH.addWidget(self.label2)
        layoutH.setContentsMargins(10, 0, 0, 10)
        layoutH.setSpacing(10)

        self.setLayout(layoutH)

        self.update_label_banque()
        self.update_label_mise()

    def update_label_banque(self):
        banque = self.widget_central_table_roulette.main_window.modele.banque
        self.label2.setText(f"Banque :  {banque}")

    def update_label_mise(self):
        mise = self.widget_central_table_roulette.main_window.modele.calculer_mise_totale()
        self.label.setText(f"Mise Totale :  {mise}")


class WidgetSimulation(QWidget):

    def __init__(self, widget_tab_bar):
        super().__init__(widget_tab_bar)
        self.widget_tab_bar = widget_tab_bar
        self.worker = WorkerSimulation(self, 0, 0, 100)

        self.grid_layout = QGridLayout(self)
        self.grid_layout.setContentsMargins(20, 0, 0, 0)
        self.grid_layout.setVerticalSpacing(9)
        self.grid_layout.setHorizontalSpacing(15)
        self.grid_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.label_nombre_simu = QLabel("Nombre de tirages :")
        self.label_nombre_simu.setFixedHeight(40)
        self.label_nombre_simu.setStyleSheet(CSS.css_label_banque_mise)

        self.line_edit = QLineEdit("500")
        self.line_edit.setValidator(QIntValidator(1, 10000))
        self.line_edit.setMaxLength(8)
        self.line_edit.setStyleSheet(CSS.css_demo_edit)
        self.line_edit.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.line_edit.setFixedSize(113, 40)

        self.label_nombre_courbes = QLabel("Nombre de simulations :")
        self.label_nombre_courbes.setFixedHeight(40)
        self.label_nombre_courbes.setStyleSheet(CSS.css_label_banque_mise)

        self.line_edit_courbes = QLineEdit("50")
        self.line_edit_courbes.setValidator(QIntValidator(1, 100))
        self.line_edit_courbes.setMaxLength(8)
        self.line_edit_courbes.setStyleSheet(CSS.css_demo_edit)
        self.line_edit_courbes.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.line_edit_courbes.setFixedSize(113, 40)

        self.label_banque_initiale = QLabel("Banque initiale :")
        self.label_banque_initiale.setFixedHeight(40)
        self.label_banque_initiale.setStyleSheet(CSS.css_label_banque_mise)

        self.line_edit_banque = QLineEdit("20")
        self.line_edit_banque.setValidator(QIntValidator())
        self.line_edit_banque.setMaxLength(8)
        self.line_edit_banque.setStyleSheet(CSS.css_demo_edit)
        self.line_edit_banque.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.line_edit_banque.setFixedSize(113, 40)

        self.plaintext = QPlainTextEdit()
        self.plaintext.setReadOnly(True)
        self.plaintext.setFixedSize(370, 300)
        self.plaintext.setMaximumBlockCount(500)
        self.plaintext.setStyleSheet(CSS.css_plain_text)
        self.plaintext.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.plaintext.appendPlainText(" Indiquer le nombre de simulations ")
        self.plaintext.horizontalScrollBar().setValue(0)

        self.lancer_button = QPushButton('LANCER')
        self.lancer_button.clicked.connect(self.lancer_simulation)
        self.lancer_button.setStyleSheet(CSS.css_bouton_tourner)
        self.lancer_button.setFixedSize(370, 40)

        self.pbar = QProgressBar(self)
        self.pbar.setStyleSheet(CSS.css_progress_bar_0_50)
        self.pbar.setValue(0)
        self.pbar.setFixedSize(370, 15)

        self.graph_stats_tirages = GraphStatsTirages(self)
        self.graph_stats_gains = GraphStatsGains(self)
        self.graph_stats_banque = GraphStatsBanque(self)
        self.historique_simulations_banque = []  # historiques des X simulations de N tirages

        self.grid_layout.addWidget(self.label_nombre_simu, 0, 0, 2, 1, alignment=(Qt.AlignTop | Qt.AlignLeft))
        self.grid_layout.addWidget(self.line_edit, 0, 2, 1, 1, alignment=(Qt.AlignTop | Qt.AlignLeft))
        self.grid_layout.addWidget(self.label_nombre_courbes, 1, 0, 2, 1, alignment=(Qt.AlignTop | Qt.AlignLeft))
        self.grid_layout.addWidget(self.line_edit_courbes, 1, 2, 1, 1, alignment=(Qt.AlignTop | Qt.AlignLeft))
        self.grid_layout.addWidget(self.label_banque_initiale, 2, 0, 2, 1, alignment=(Qt.AlignTop | Qt.AlignLeft))
        self.grid_layout.addWidget(self.line_edit_banque, 2, 2, 1, 1, alignment=(Qt.AlignTop | Qt.AlignLeft))
        self.grid_layout.addWidget(self.plaintext, 3, 0, 7, 3, alignment=(Qt.AlignTop | Qt.AlignLeft))
        self.grid_layout.addWidget(self.lancer_button, 11, 0, 1, 3, alignment=(Qt.AlignTop | Qt.AlignLeft))
        self.grid_layout.addWidget(self.pbar, 12, 0, 1, 3, alignment=(Qt.AlignTop | Qt.AlignLeft))

        self.grid_layout.addWidget(self.graph_stats_tirages, 0, 3, 3, 30, alignment=(Qt.AlignVCenter | Qt.AlignLeft))
        self.grid_layout.addWidget(self.graph_stats_gains, 3, 3, 8, 30, alignment=(Qt.AlignTop | Qt.AlignLeft))
        self.grid_layout.addWidget(self.graph_stats_banque, 8, 3, 8, 30, alignment=(Qt.AlignTop | Qt.AlignLeft))

        self.setLayout(self.grid_layout)

    def lancer_simulation(self):
        self.plaintext.clear()
        self.historique_simulations_banque = []
        self.verifier_entrees()
        self.graph_stats_banque.remise_zero()
        self.thread = QThread()

        self.worker = WorkerSimulation(self, self.line_edit.text(), self.line_edit_courbes.text(), self.line_edit_banque.text())
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.finished.connect(self.thread.deleteLater)
        self.worker.finished.connect(lambda: self.pbar.setValue(0))
        self.worker.progress.connect(self.update_progress_bar)
        self.worker.signal_graph_stats_tirage.connect(self.update_graph_stats_tirages)
        self.worker.signal_graph_stats_gains.connect(self.update_graph_stats_gains)
        self.worker.signal_graph_stats_banque_plot.connect(self.update_graph_stats_banque_plot)
        self.worker.signal_graph_stats_banque_fin.connect(self.update_graph_stats_banque_fin)
        self.thread.start()
        self.lancer_button.setEnabled(False)
        self.thread.finished.connect(lambda: self.lancer_button.setEnabled(True))

    def verifier_entrees(self):
        """ Vérifie les entrees utilisateur de la simulation"""
        if self.line_edit_courbes.text() == "0":
            self.line_edit_courbes.setText("1")

        if int(self.line_edit_courbes.text()) > 300:
            self.line_edit_courbes.setText("300")

        if self.line_edit.text() == "0":
            self.line_edit.setText("1")

        if int(self.line_edit.text()) > 10000:
            self.line_edit.setText("10000")

        if int(self.line_edit_courbes.text()) > int(self.line_edit.text()):  # si le nombre de simu est < nb de courbes
            self.line_edit_courbes.setText(self.line_edit.text())

    def addtext(self, text: str):
        self.plaintext.appendPlainText(text)

    def update_progress_bar(self, valeur):
        if valeur < 50:
            self.pbar.setStyleSheet(CSS.css_progress_bar_0_50)
        else:
            self.pbar.setStyleSheet(CSS.css_progress_bar_50_100)
        self.pbar.setValue(valeur)

    def update_graph_stats_tirages(self, liste):
        abscisse = []
        ordonnee = []
        for valeur in liste:
            abscisse.append(valeur[0])
            ordonnee.append(valeur[1])

        couleurs = []
        for x in abscisse:
            couleurs.append(self.widget_tab_bar.main_window.modele.jeu[str(x)][0])

        self.graph_stats_tirages.plot(abscisse, ordonnee, couleurs)

    def update_graph_stats_gains(self, liste, mise_totale, banqueroute):
        abscisse = []
        ordonnee = []
        for valeur in liste:
            abscisse.append(valeur[0])
            ordonnee.append(valeur[1])

        couleurs = []
        i = 0
        for x in abscisse:
            if banqueroute == i:
                couleurs.append("red")
            else:
                couleurs.append("#FDE08D")
            i += 1

        moyenne_de_gain = np.mean(ordonnee)
        mediane_de_gain = np.median(ordonnee)
        ecart_type_de_gain = np.std(ordonnee)

        self.graph_stats_gains.plot(abscisse, ordonnee, couleurs, moyenne_de_gain)
        self.addtext(f"Sur {len(abscisse)} tirages pour une mise de {mise_totale} :")
        self.addtext(f"Moyenne : {moyenne_de_gain}")
        self.addtext(f"Mediane : {mediane_de_gain}")
        self.addtext(f"Ecart type : {ecart_type_de_gain:.2f}")

    def update_graph_stats_banque_plot(self, liste):
        abscisse = []
        ordonnee = []
        for valeur in liste:
            abscisse.append(valeur[0])
            ordonnee.append(valeur[1])

        self.historique_simulations_banque.append([abscisse, ordonnee])
        self.graph_stats_banque.plot(abscisse, ordonnee)

    def update_graph_stats_banque_fin(self):
        self.graph_stats_banque.afficher_graphique()

        liste_numeros_tirage_banqueroute = []  # liste des N-ième tirages menant à une banqueroute, si elle arrive, pour chaque simulation

        nb_simu_positives = 0
        for simulation in self.historique_simulations_banque:
            curseur_tirage = 1
            is_banqueroute = False
            for tirage in simulation[1]:
                if tirage < 0:
                    liste_numeros_tirage_banqueroute.append(curseur_tirage)
                    is_banqueroute = True
                    break
                curseur_tirage += 1

            if not is_banqueroute:
                nb_simu_positives += 1

        self.addtext(f"Nombre de simulations sans banqueroute : {nb_simu_positives}")
        self.addtext(f"En moyenne, la banqueroute arrive au {np.mean(liste_numeros_tirage_banqueroute): .1f} ième tirage")


class WorkerSimulation(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    signal_graph_stats_tirage = pyqtSignal(list)
    signal_graph_stats_gains = pyqtSignal(list, int, int)
    signal_graph_stats_banque_plot = pyqtSignal(list)
    signal_graph_stats_banque_fin = pyqtSignal()

    def __init__(self, widget_simulation, nb_tirage, nb_courbes, banque_initiale):
        QObject.__init__(self)
        self.widget_simulation = widget_simulation
        self.nb_tirage = int(nb_tirage)              # donnée entrée par ihm
        self.nb_courbes = int(nb_courbes)            # donnée entrée par ihm
        self.banque_initiale = int(banque_initiale)  # valeur banque au depart de la simulation, entrée IHM
        self.progression_actuelle = 0           # valeur progress bar pour le calcul

    def run(self):
        comptage_numeros_sortis = [[x, 0] for x in range(0, 37)]  # graph_stats_tirages
        gains_par_tirage = []       # graph_stats_gains
        banque_par_tirage = []      # graph stats banque
        banqueroute = None          # graph stats banque
        mise_totale = 0
        banque = self.banque_initiale

        for simulation in range(0, self.nb_courbes):
            for x in range(1, self.nb_tirage + 1):
                mise_totale, numero, gain_tirage = self.widget_simulation.widget_tab_bar.main_window.modele.lancer_tirage_simulation()
                banque_par_tirage.append([x, banque])

                if simulation == 0:   # on ne crée ces graphiques qu'une fois
                    #### graph_stats_tirages ####
                    for numero_liste in comptage_numeros_sortis:
                        if numero_liste[0] == numero:
                            numero_liste[1] += 1

                    #### graph_stats_gains ####
                    gains_par_tirage.append([x, gain_tirage])

                #### graph_stats_banque ####
                if banqueroute is None:
                    if banque - mise_totale < 0:   # si on ne peut plus miser → banqueroute
                        banqueroute = x
                banque += gain_tirage
                banque_par_tirage.append([x, banque])

                ### mise à jour barre de progression ###
                x_map = python_map(x * simulation, 0, self.nb_tirage * self.nb_courbes, 0, 100)  # pourcentage d'evolution de la progress bar
                if x_map > self.progression_actuelle:  # permet de ne pas envoyer plein de signaux identiques
                    self.progression_actuelle = x_map
                    self.progress.emit(int(x_map))

            self.signal_graph_stats_banque_plot.emit(banque_par_tirage)  # on ajoute une courbe pour 1 simulation de X tirages
            banque_par_tirage = []
            banque = self.banque_initiale

        self.signal_graph_stats_tirage.emit(comptage_numeros_sortis)
        if self.nb_tirage <= 1000:
            self.signal_graph_stats_gains.emit(gains_par_tirage, mise_totale, banqueroute)
        self.signal_graph_stats_banque_fin.emit()
        self.finished.emit()


class GraphStatsTirages(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure(facecolor='#363636', figsize=(20, 10))
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.ax = None
        self.setFixedSize(750, 150)
        self.setContentsMargins(0, 0, 0, 0)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        #self.setAttribute(Qt.WA_StyledBackground, True)
        #self.setStyleSheet('background-color: orange;')

    def plot(self, abscisses, ordonnees, couleurs):
        self.figure.clf()
        self.figure.subplots_adjust(0, 0.12, 1, 0.8, 0, 0)
        self.ax = self.figure.add_subplot(111)
        self.ax.xaxis.set_ticks(range(37))

        self.ax.xaxis.set_ticklabels([str(x) for x in range(37)], rotation=0, color='#FDE08D', fontsize=7)
        self.ax.set_frame_on(False)

        p1 = self.ax.bar(abscisses, ordonnees, width=0.6, color=couleurs, linewidth=0)
        self.ax.bar_label(p1, fontsize=6, color='#FDE08D')
        self.ax.set_title('Quantité des numéros sortis pour la premiere simulation de N tirages', fontsize=10, pad=10, color="#FDE08D")

        self.canvas.draw()


class GraphStatsGains(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure(facecolor='#363636', figsize=(20, 10))
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.ax = None
        self.setFixedSize(750, 200)
        self.setContentsMargins(0, 0, 0, 0)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        #self.setAttribute(Qt.WA_StyledBackground, True)
        #self.setStyleSheet('background-color:blue;')

    def plot(self, abscisses, ordonnees, couleurs, moyenne):
        self.figure.clf()
        self.figure.subplots_adjust(0.07, 0.2, 0.95, 0.8, 0, 0)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_frame_on(False)
        p1 = self.ax.bar(abscisses, ordonnees, color=couleurs)
        self.ax.tick_params(color='#FDE08D', labelcolor="#FDE08D", labelsize=8)
        self.ax.bar_label(p1, fontsize=6, color='#FDE08D')
        self.ax.grid(alpha=0.2, linestyle='--')
        self.ax.hlines(y=moyenne, xmin=0, xmax=len(abscisses), linewidth=1, color='#468966')
        self.ax.set_title('Gain pour une même mise des N tirages de la premiere simulation ', fontsize=10, pad=10, color="#FDE08D")

        self.canvas.draw()


class GraphStatsBanque(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.figure = Figure(facecolor='#363636', figsize=(20, 10))
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.ax = None
        self.setFixedSize(750, 240)
        self.setContentsMargins(0, 0, 0, 0)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        #self.setAttribute(Qt.WA_StyledBackground, True)
        #self.setStyleSheet('background-color: green;')

    def plot(self, abscisses, ordonnees):
        #self.figure.clf()
        #self.figure.subplots_adjust(0.07, 0.1, 0.95, 0.8, 0, 0)
        #self.ax = self.figure.add_subplot(111)

        self.ax.plot(abscisses, ordonnees)
        #self.ax.tick_params(color='#FDE08D', labelcolor="#FDE08D", labelsize=7)
        #self.ax.hlines(y=0, xmin=0, xmax=len(abscisses), linewidth=1, color='r')
        #self.ax.grid(alpha=0.2, linestyle='--')
        #self.ax.set_frame_on(False)
        #self.ax.set_title('Evolution de la banque pour une même mise', fontsize=10, pad=10, color="#FDE08D")

        #self.canvas.draw()

    def remise_zero(self):
        self.figure.clf()
        self.figure.subplots_adjust(0.07, 0.1, 0.95, 0.8, 0, 0)
        self.ax = self.figure.add_subplot(111)

        self.ax.tick_params(color='#FDE08D', labelcolor="#FDE08D", labelsize=7)
        self.ax.grid(alpha=0.2, linestyle='--')
        self.ax.set_frame_on(False)
        self.ax.set_title('Evolution de la banque pour une même mise', fontsize=10, pad=10, color="#FDE08D")

    def afficher_graphique(self):
        self.ax.hlines(y=0, xmin=0, xmax=self.ax.get_xlim()[1], linewidth=1, color='r')
        self.canvas.draw()





