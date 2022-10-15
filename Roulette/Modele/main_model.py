#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author : Jean-Alexis HERMEL
# Date : 29/10/2020
from collections import OrderedDict
from Modele.outils import *
from collections import deque
from itertools import islice
from Modele.generateur_alea import lancer_roulette



class MainModele:
    def __init__(self):
        self.jeu = OrderedDict({
            "0": ["green"],
            "1": ["red", "impair", "first"],
            "2": ["black", "pair", "second"],
            "3": ["red", "impair", "third"],
            "4": ["black", "pair", "first"],
            "5": ["red", "impair", "second"],
            "6": ["black", "pair", "third"],
            "7": ["red", "impair", "first"],
            "8": ["black", "pair", "second"],
            "9": ["red", "impair", "third"],
            "10": ["black", "pair", "first"],
            "11": ["black", "impair", "second"],
            "12": ["red", "pair", "third"],
            "13": ["black", "impair", "first"],
            "14": ["red", "pair", "second"],
            "15": ["black", "impair", "third"],
            "16": ["red", "pair", "first"],
            "17": ["black", "impair", "second"],
            "18": ["red", "pair", "third"],
            "19": ["red", "impair", "first"],
            "20": ["black", "pair", "second"],
            "21": ["red", "impair", "third"],
            "22": ["black", "pair", "first"],
            "23": ["red", "impair", "second"],
            "24": ["black", "pair", "third"],
            "25": ["red", "impair", "first"],
            "26": ["black", "pair", "second"],
            "27": ["red", "impair", "third"],
            "28": ["black", "pair", "first"],
            "29": ["black", "impair", "second"],
            "30": ["red", "pair", "third"],
            "31": ["black", "impair", "first"],
            "32": ["red", "pair", "second"],
            "33": ["black", "impair", "third"],
            "34": ["red", "pair", "first"],
            "35": ["black", "impair", "second"],
            "36": ["red", "pair", "third"],
            "1st 12": ["green"],
            "2nd 12": ["green"],
            "3rd 12": ["green"],
            "1 to 18": ["green"],
            "19 to 36": ["green"],
            "PAIR": ["green"],
            "IMPAIR": ["green"],
            "ROUGE": ["red"],
            "NOIR": ["black"],
            "1st": ["green"],
            "2nd": ["green"],
            "3rd": ["green"],
        })
        self.equivalent_group_case = {
            str(['1st']): ['3', '6', '9', '12', '15', '18', '21', '24', '27', '30', '33', '36'],
            str(['2nd']): ['2', '5', '8', '11', '14', '17', '20', '23', '26', '29', '32', '35'],
            str(['3rd']): ['1', '4', '7', '10', '13', '16', '19', '22', '25', '28', '31', '34'],
            str(['1st 12']): ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
            str(['2nd 12']): ['13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24'],
            str(['3rd 12']): ['25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36'],
            str(['1st', '2nd']): ['3', '6', '9', '12', '15', '18', '21', '24', '27', '30', '33', '36',
                                  '2', '5', '8', '11', '14', '17', '20', '23', '26', '29', '32', '35'],
            str(['2nd', '3rd']): ['2', '5', '8', '11', '14', '17', '20', '23', '26', '29', '32', '35',
                                  '1', '4', '7', '10', '13', '16', '19', '22', '25', '28', '31', '34'],
            str(['1st 12', '2nd 12']): ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
                                        '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24'],
            str(['2nd 12', '3rd 12']): ['13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24',
                                        '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36'],
            str(['1 to 18']): ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16',
                               '17', '18'],
            str(['19 to 36']): ['19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32',
                                '33', '34', '35', '36'],
            str(['PAIR']): ['2', '4', '6', '8', '10', '12', '14', '16', '18', '20', '22', '24', '26', '28', '30', '32',
                            '34', '36'],
            str(['IMPAIR']): ['1', '3', '5', '7', '9', '11', '13', '15', '17', '19', '21', '23', '25', '27', '29', '31',
                              '33', '35'],
            str(['ROUGE']): ['1', '3', '5', '7', '9', '12', '14', '16', '18', '19', '21', '23', '25', '27', '30', '32',
                             '34', '36'],
            str(['NOIR']): ['2', '4', '6', '8', '10', '11', '13', '15', '17', '20', '22', '24', '26', '28', '29', '31',
                            '33', '35']
        }
        self.dic_des_mises = {}  # regroupe les mises effectuées ['case_misee(s)'] = mise_actuelle
        self.banque = 100        # Somme restante pour effectuer des mises
        self.queue_resultats_tirages = deque(maxlen=100)

    def transformer_dic_des_mises(self):
        """Remplace les cases misées qui ne sont pas des numéros par les cases numéros qu'ils représentent"""

        for hash, case_misees in self.dic_des_mises.items():
            for equivalent_case, valeur_equivalent in self.equivalent_group_case.items():
                if str(case_misees['cases']) == equivalent_case:
                    self.dic_des_mises[hash]['cases'] = valeur_equivalent

            if case_misees['mise'] >= 1000:
                self.dic_des_mises[hash]['mise'] = 1000

    def calculer_gain_par_case(self) -> OrderedDict:
        """Alanyse les cases misées et leurs mises, et complete le dictionnaire de gains en fonction"""
        dic_gain_par_case = OrderedDict({str(k):0 for k in [x for x in range(0, 37)]})

        for hash, case_misees in self.dic_des_mises.items():
            mise = case_misees['mise']

            if len(case_misees['cases']) == 1:
                for case in case_misees['cases']:
                    dic_gain_par_case[case] += (mise * 36)

            elif len(case_misees['cases']) == 2:
                for case in case_misees['cases']:
                    dic_gain_par_case[case] += (mise * 18)

            elif len(case_misees['cases']) == 3:
                for case in case_misees['cases']:
                    dic_gain_par_case[case] += (mise * 12)

            elif len(case_misees['cases']) == 4:
                for case in case_misees['cases']:
                    dic_gain_par_case[case] += (mise * 9)

            elif len(case_misees['cases']) == 6:
                for case in case_misees['cases']:
                    dic_gain_par_case[case] += (mise * 6)

            elif len(case_misees['cases']) == 12:
                for case in case_misees['cases']:
                    dic_gain_par_case[case] += (mise * 3)

            elif len(case_misees['cases']) == 18:
                for case in case_misees['cases']:
                    dic_gain_par_case[case] += (mise * 2)

                dic_gain_par_case["0"] += (mise / 2)  # cas du zero pour chance simple

            elif len(case_misees['cases']) == 24:
                for case in case_misees['cases']:
                    dic_gain_par_case[case] += (mise * 1.5)

        return dic_gain_par_case

    def calculer_mise_totale(self):
        mise_totale = 0
        for hash, case_misees in self.dic_des_mises.items():
            mise_totale += case_misees["mise"]

        return mise_totale

    def calculer_gain_moyen_case(self):
        """Calcule le gain moyen pour une case et le ratio gain_moyen/mise_totale en se basant sur l'ensemble des mises sur toutes les cases"""

        dic_de_gain = self.calculer_gain_par_case()

        mise_totale = self.calculer_mise_totale()
        gain_total = 0
        for numero, gain in dic_de_gain.items():
            gain_total += gain

        gain_moyen = round(gain_total/37, 3)

        try:
            ratio_gain_mise = round(gain_moyen/mise_totale, 3)
        except ZeroDivisionError:
            ratio_gain_mise = 0

        return gain_moyen, ratio_gain_mise

    def is_mise_avec_banque_positive(self, mise_case):
        mise_totale = self.calculer_mise_totale()
        return (self.banque - mise_totale - mise_case) < 0

    def lancer_tirage(self, nombre_tirage: int):
        tirage = lancer_roulette(nombre_tirage)
        self.queue_resultats_tirages.appendleft(tirage)

    def mettre_banque_a_jour(self):
        numero_sorti = self.queue_resultats_tirages[0]
        mise_totale = self.calculer_mise_totale()
        gain_total = self.calculer_gain_par_case()[str(numero_sorti)]
        self.banque += (gain_total - mise_totale)








