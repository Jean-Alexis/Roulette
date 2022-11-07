#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author : Jean-Alexis HERMEL
# Date : 05/10/2022
import os

css_main_window = """
    QMainWindow {
        background: #363636;
        border: none;
    }
    QMessageBox {
        background: #363636;
        font-family:"Arial";
        font-weight:bold;
        font-size: 16px;
        text-align:center;
        color: rgba(251, 251, 240, 255);
    }
    QMessageBox QLabel {
        color: rgba(243, 242, 211, 255);
        background: #363636;
    }
    
    QMessageBox QPushButton{
        display:inline-block;
        padding: 10px;
        border:0.15em solid #000000;
        border-radius: 5px;
        text-decoration:none;
        font-family:'Roboto';
        font-weight:bold;
        color:rgb(255, 251, 195);
        text-shadow: 0 0.04em 0.04em rgba(0,0,0,0.35);
        background-color: rgb(70, 137, 102);
        text-align:center;
        transition: all 0.1s;
        font-size: 13px
    }
    QMessageBox QPushButton:pressed {
        text-shadow: 0 0 2em rgba(255,255,255,1);
        color: rgb(255, 225, 154);  
        border-color: rgb(255, 225, 154);
        transition: 0.4s;
        padding-bottom : 1px;
        padding-right : 1px;
    }
    QMessageBox QPushButton:hover {
        border: 2px solid ;
        text-shadow: 0 0.04em 0.04em rgba(0,0,0,0.35);
        background-color: rgb(119, 205, 123, 255);
        
    }
"""

css_btn_send_do = """
    QPushButton{
        font-family:"Arial";
        font-weight:bold;
        font-size: 15px;
        text-align:center;
        background: rgba(255, 255, 255, 150);
        border-radius: 6px;
        padding: 4px;
        border: 2px solid #8f8f91;
        margin : 0px;
    }
    QPushButton:pressed{
        border: 2px solid #656970;
        padding-bottom : 3px;
        padding-right : 3px;
        background: qlineargradient(x1:5, y1:0, x2:0, y2:1, 
                        stop:0 #4F5254, 
                        stop:1 #afb1b3);
    }
    QPushButton:hover{
        border: 3px solid #656970;
    }
"""

css_bouton_effacer_jetons = """
    QPushButton{
        display:inline-block;
        padding: 10px;
        border:0.15em solid #000000;
        border-radius: 5px;
        text-decoration:none;
        font-family:'Roboto';
        font-weight:bold;
        color:rgb(255, 251, 195);
        text-shadow: 0 0.04em 0.04em rgba(0,0,0,0.35);
        background-color: rgb(70, 137, 102);
        text-align:center;
        transition: all 0.1s;
        font-size: 13px
    }
    
    QPushButton:hover{
        text-shadow: 0 0 2em rgba(255,255,255,1);
        color: rgb(255, 225, 154);  
        border-color: rgb(255, 225, 154);
        transition: 0.4s;
    }
    
    QPushButton:pressed{
        border: 2px solid ;
        text-shadow: 0 0.04em 0.04em rgba(0,0,0,0.35);
        padding-bottom : 8px;
        padding-right : 12px;
    }
"""

css_bouton_afficher_gains = """
    QPushButton{
        display:inline-block;
        padding: 5px;
        border:0.15em solid #000000;
        border-radius: 5px;
        text-decoration:none;
        font-family:'Roboto';
        font-weight:bold;
        color:rgb(255, 251, 195);
        text-shadow: 0 0.04em 0.04em rgba(0,0,0,0.35);
        background-color: rgb(70, 137, 102);
        text-align:center;
        transition: all 0.1s;
        font-size: 13px
    }

    QPushButton:hover{
        text-shadow: 0 0 2em rgba(255,255,255,1);
        color: rgb(255, 225, 154);  
        border-color: rgb(255, 225, 154);
        transition: 0.4s;
    }

    QPushButton:pressed{
        border: 2px solid ;
        text-shadow: 0 0.04em 0.04em rgba(0,0,0,0.35);
        padding-bottom : 3px;
        padding-right : 7px;
    }
"""

css_label_info = """ 
       QLabel{
            font-family:'Roboto';
            font-weight:bold;
            color:#FDE08D;
            text-shadow: 0 0.04em 0.04em rgba(0,0,0,0.35);
            text-align:center;
            font-size: 10px;
            margin-left: 0px;
        }
    """

css_label_banque_mise = """ 
       QLabel{
            font-family: 'Roboto';
            font-weight:bold;
            border: 2px solid #FDE08D;
            border-radius: 3px;
            text-align:center;
            font-size: 18px;
            margin-left: 0px;
            padding-top: 0px;
            color: #FDE08D;
        }
    """

css_table_roulette_view = """
    border: none;
    padding 0px;
    background: #363636;
    margin: 0px;
"""

css_bouton_tourner = """
    QPushButton{
        background: qlineargradient(
                x1: 0, y1: 1, x2: 1, y2: 1,
                stop: 0 #8f6B29, stop: 0.7 #FDE08D,
                stop: 1.0 #DF9F28);
        border-radius: 6px;
        height: 40px;
        font-family: 'Open Sans', sans-serif;
        font-weight:bold;
    
        text-align:center;
        font-size: 20px;
        margin-left: 0px;
        color: #28292d;
        subcontrol-position: right bottom;
        subcontrol-origin: margin;
        border: 2px solid #28292d; 
    }
    
    QPushButton:hover{
        background: qlineargradient(
                x1: 0, y1: 1, x2: 1, y2: 1,
                stop: 0 #DF9F28, stop: 0.7 #FDE08D,
                stop: 1.0 #8f6B29);
        border-radius: 6px;
        height: 40px;
        font-family: 'Open Sans', sans-serif;
        font-weight:bold;
    
        text-align:center;
        font-size: 20px;
        margin-left: 0px;
        color: #28292d;
        subcontrol-position: right bottom;
        subcontrol-origin: margin;
        border: 2px solid #28292d; 
        transition: 0.4s;
    }

    QPushButton:pressed{
        border: 2px solid #28292d; 
        text-shadow: 0 0.04em 0.04em rgba(0,0,0,0.35);
        padding-bottom : 3px;
        padding-right : 4px;
    }
    
"""

css_bouton_rejouer_mise = """
    QPushButton{
        background-image: url(""" + os.path.join(os.path.dirname(os.path.dirname(__file__)), "Ressources", "replay.png").replace(os.sep, '/') + """);
        background-color: qlineargradient(
                x1: 0, y1: 1, x2: 1, y2: 1,
                stop: 0 #8f6B29, stop: 0.7 #FDE08D,
                stop: 1.0 #DF9F28);
        border-radius: 6px;
        height: 40px;
        border: 2px solid #28292d;
        background-repeat: no-repeat; 
        background-position: center;
    }
    
    QPushButton:hover{
        background-color: qlineargradient(
                x1: 0, y1: 1, x2: 1, y2: 1,
                stop: 0 #DF9F28, stop: 0.7 #FDE08D,
                stop: 1.0 #8f6B29);
        border-radius: 6px;
        height: 40px;
        border: 2px solid #28292d;
    }

    QPushButton:pressed{
        background-image: url(""" + os.path.join(os.path.dirname(os.path.dirname(__file__)), "Ressources", "replay_petit.png").replace(os.sep, '/') + """);
        background-repeat: no-repeat; 
        background-position: center;
    }
    
"""

css_tab_bar = """
    QTabWidget::pane { 
        position: absolute;
        top: 1em;
        border: none;
    }

    QTabBar::tab {
        font-family:"Arial";
        font-weight:bold;
        font-size: 16px;
        text-align:center;
        color: #3c3f41;
        background:  #afb1b3;
        padding: 4px;
        min-width: 25ex;
        min-height: 8ex;
    }

    QTabBar::tab:selected{
        background: #777879;
        color: #D6D6D6;
    }
    QTabBar::tab:hover{
        background: qlineargradient(x1:5, y1:0, x2:0, y2:1, 
                    stop:0 #4F5254, 
                    stop:1 #afb1b3);}
    }"""

css_status_bar = """
    QStatusBar::item {
        border: none;
    }

    QStatusBar{
        background: #4F5254;
        font-family:"Arial";
        font-weight:bold;
        font-size: 13px;
        text-align:center;
        color: #afb1b3;
    }
"""

css_plain_text = """
    QPlainTextEdit{
        font-family:"Roboto";
        font-size: 15px;
        color: #afb1b3;
        border: 2px solid #afb1b3;
        padding: 10px;
        border-radius: 8px;
        background: #4F5254;
    }

    QScrollBar:vertical {
        border-radius: 8px;
        background: solid #afb1b3;
        width: 20px;
        margin: 23px 0px 23px 0;
        padding 2px;
    }
    QScrollBar::handle:vertical {
        background: qlineargradient(
                x1: 0, y1: 1, x2: 1, y2: 1,
                stop: 0 #afb1b3, stop: 0.7#4F5254,
                stop: 1.0 #4F5254);
        border: 1px solid #afb1b3;
        border-radius: 7px;
        min-height: 30px;
    }
    QScrollBar::add-line:vertical {
        background: qlineargradient(
                x1: 0, y1: 1, x2: 1, y2: 1,
                stop: 0 #afb1b3, stop: 0.7#4F5254,
                stop: 1.0 #4F5254);
        border-radius: 4px;
        height: 16px;
        subcontrol-position: right bottom;
        subcontrol-origin: margin;
        border: 1px solid #888A85; 
    }
    QScrollBar::sub-line:vertical {
        background: qlineargradient(
                x1: 0, y1: 1, x2: 1, y2: 1,
                stop: 0 #afb1b3, stop: 0.7#4F5254,
                stop: 1.0 #4F5254);
        border-radius: 4px;
        height: 16px;
        subcontrol-position: right top;
        subcontrol-origin: margin;
        border: 1px solid #888A85;
        position: absolute; 
    }
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: none;
    }

    QScrollBar:horizontal {
        border-radius: 8px;
        background: solid #afb1b3;
        height: 20px;
        margin: 0px 23px 0px 23px;
    }
    QScrollBar::handle:horizontal {
        background: qlineargradient(
            x1: 0, y1: 0, x2: 0, y2: 1,
            stop: 0 #afb1b3, stop: 0.7 #4F5254,
            stop: 1.0 #4F5254);
        border: 1px solid #afb1b3;
        border-radius: 7px;
        min-width: 30px;
    }
    QScrollBar::add-line:horizontal {
        background: qlineargradient(
                x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #afb1b3, stop: 0.7 #4F5254,
                stop: 1.0 #4F5254);
        border-radius: 4px;
        width: 16px;
        subcontrol-position: right;
        subcontrol-origin: margin;
        border: 1px solid #888A85;
    }
    QScrollBar::sub-line:horizontal {
        background: qlineargradient(
                x1: 0, y1: 0, x2: 0, y2: 1,
                stop: 0 #afb1b3, stop: 0.7 #4F5254,
                stop: 1.0 #4F5254);
        border-radius: 4px;
        width: 16px;
        subcontrol-position: top left;
        subcontrol-origin: margin;
        border: 1px solid #888A85;
        position: absolute;
    }
    QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
        background: none;
    }
"""

css_demo_edit = """
    QLineEdit{
        color:  #4F5254;
        font-family:"Roboto";
        font-size: 14px;
        font-weight:bold;
        background: #afb1b3;
        border: 2px solid gray;
        border-radius: 6px;
        padding: 0 8px;
        selection-background-color: darkgray;
    }
"""

css_progress_bar_0_50 = """
    QProgressBar {
        border: 2px solid #28292d; 
        border-radius: 6px;
        text-align: center;
        font-family: 'Roboto';
        font-weight:bold;
        color: #afb1b3;
        background-color: #363636;
    }

    QProgressBar::chunk {
        background-color: #FDE08D;
        border-radius: 5px;    
    }
"""

css_progress_bar_50_100 = """
    QProgressBar {
        border: 2px solid #28292d; 
        border-radius: 6px;
        text-align: center;
        font-family: 'Roboto';
        font-weight:bold;
        color: #363636;
        background-color: #363636;
    }

    QProgressBar::chunk {
        background-color: #FDE08D;
        border-radius: 5px;    
    }
"""


def css_style_case_historique_tirage(nombre, modele):
    style = ""
    couleur_nombre = modele.jeu[str(nombre)][0]
    if couleur_nombre == "green":
        style = """
         QLabel{
            background-color: rgb(46, 125, 50, 255);
            font-family: 'Roboto';
            font-weight:bold;
            text-align:center;
            border-radius: 3px;
            font-size: 10px;
            margin-left: 0px;
            color: #FDE08D;
            border: 1px solid;
        }
        """
    elif couleur_nombre == "red":
        style = """
         QLabel{
            background-color: rgb(197, 18, 18, 255);
            font-family: 'Roboto';
            font-weight:bold;
            text-align:center;
            border-radius: 3px;
            font-size: 10px;
            margin-left: 0px;
            color: #FDE08D;
            border: 1px solid;
        }
        """
    elif couleur_nombre == "black":
        style = """
         QLabel{
            background-color: rgb(25, 25, 25, 255);
            font-family: 'Roboto';
            font-weight:bold;
            text-align:center;
            border-radius: 3px;
            font-size: 10px;
            margin-left: 0px;
            color: #FDE08D;
            border: 1px solid;
        }
        """
    return style


def css_style_jeton(couleur, taille):
    jeton_url = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Ressources", f"jeton_{couleur}.png")
    jeton_url = jeton_url.replace(os.sep, '/')

    css_jeton = ""

    if taille == "grand":
        css_jeton = """
            QPushButton{
                border-image: url(""" + jeton_url + """);
                font-family:"Roboto";
                font-weight:bold;
                font-size: 15px;
            }
        """

    if taille == "petit":
        css_jeton = """
            QPushButton{
               border-image: url(""" + jeton_url + """);
               font-family:"Roboto";
               margin: 5px;
               font-weight:bold;
               font-size: 10px;
            }
        """

    return css_jeton


def css_label_animation_gain(nombre):
    css_label_animation_gain = """ 
           QLabel{
                font-family:'Roboto';
                font-weight:bold;
                color:#FDE08D;
                border-radius: 50%;
                border: 3px solid #FDE08D;
                text-align: center;
                font-size: 25px;
                margin-left: 0px;
            }
        """

    return css_label_animation_gain
