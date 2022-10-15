#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author : Jean-Alexis HERMEL
# Date : 05/10/2022


from PyQt5.QtCore import QObject, pyqtSlot


class MainController(QObject):
    def __init__(self, model):
        super().__init__()

        self.model = model

    # Takes Signal from UI
    @pyqtSlot(int)
    def change_amount(self, value):
        self.model.amount = value

        # calculate even or odd
        self.model.even_odd = 'odd' if value % 2 else 'even'

        # calculate button enabled state
        self.model.enable_reset = True if value else False

    @pyqtSlot(str)
    def add_user(self, value):
        self.model.add_user(value)
        # calculate button enabled state
        #if(self._model.users.count > 0):
        #    self._model.enable_del_user = True if value else False

    @pyqtSlot(int)
    def delete_user(self, value):
        self.model.delete_user(value)
        # calculate button enabled state
        #if(self._model.users.count > 0):
        #    self._model.enable_del_user = True if value else False
