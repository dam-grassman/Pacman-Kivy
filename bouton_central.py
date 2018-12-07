"""

Ceci est le code qui va permettre d'afficher une photo dans la case centrale du jeu

"""
from kivy import require
from kivy.uix.widget import Widget
from kivy.properties import StringProperty

require('1.9.1')# version de Kivy utilisée dans ce script

class Photo(Widget):
    ph = StringProperty("Images/N.png")
    pass