#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author : Jean-Alexis HERMEL
# Date : 02/10/2022
import json
import os
from time import perf_counter_ns


def prRed(skk): print("\033[91m {}\033[00m".format(skk))
def prGreen(skk): print("\033[92m {}\033[00m".format(skk))
def prYellow(skk): print("\033[93m {}\033[00m".format(skk))
def prLightPurple(skk): print("\033[94m {}\033[00m".format(skk))
def prPurple(skk): print("\033[95m {}\033[00m".format(skk))
def prCyan(skk): print("\033[96m {}\033[00m".format(skk))
def prLightGray(skk): print("\033[97m {}\033[00m".format(skk))
def prBlack(skk): print("\033[98m {}\033[00m".format(skk))


class Timer:
    def __init__(self):
        self.t1_start = perf_counter_ns()
        self.t1_stop = None

    def calculer_temps_execution(self):
        self.t1_stop = perf_counter_ns() - self.t1_start
        prLightPurple(f"Temps écoulé : {self.t1_stop/10**6}")


def print_dic(dico):
    for key, value in dico.items():
        prGreen(f"{key} : {value}")


def trouver_image_ressources(nom_image: str):
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), "Ressources", str(nom_image))


def hash_liste_numeros_concernes(liste_numeros_concernes):
    """Retourne un identifiant unique de la liste des numéros concernés par une mise d'un jeton"""
    return hash(tuple(liste_numeros_concernes))
