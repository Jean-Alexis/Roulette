import sys
import ctypes
import traceback
import logging

from PyQt5.QtWidgets import *
from Vue.main_vue import MainWindow
from Modele.main_model import MainModele
from Controleur.main_controleur import MainController


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.init_all()
        self.init_excepthook()

        self.model = MainModele()
        self.main_controleur = MainController(self.model)
        self.main_vue = MainWindow(self.model, self.main_controleur)
        self.main_vue.show()

    @staticmethod
    def init_all():
        """ Permet d'initialiser les icones et le fichier de logs"""

        myappid = u'string.to.change.icon.windows'  # permet d'afficher l'icone en barre des tâches
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    @staticmethod
    def catch_exceptions(t, val, tb):  # permet de capturer les exceptions passées à la trappe
        """ Permet d'attraper les execptions qui surviennent et qui n'auraient pas été anticipées, elles sont enregistrées
        le fichier de logs. Un message popup apparait en prévenant d'un problème, puis le programme se fermera."""
        print_traceback = ""
        for x in traceback.format_tb(tb):
            print_traceback += x
        logging.critical('Exception : {}\n\nValeur : {}\n\nTraceback: {}'.format(t, val, print_traceback))

        # QMessageBox.critical(None, "Une Erreur inconnue a été levée", print_traceback)

        sys.exit(-1)  # on quitte le programme

    def init_excepthook(self):
        """ Permet de capturer les exceptions non prévues"""
        sys.excepthook = self.catch_exceptions


if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec())
