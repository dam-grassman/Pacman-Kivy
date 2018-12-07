"""

On crée une classe héritée de la classe Widget et dont le joueur est une instance

"""

####################################################################################################

###Imports

####################################################################################################

from kivy import require
from kivy.uix.widget import Widget
from kivy.properties import StringProperty

require('1.9.1')#version de Kivy utilisée dans ce script

####################################################################################################

###Classe de la pokeball

####################################################################################################

class Pokeball(Widget):

    ima = StringProperty("Images/pokeball.png")

    def bounce_joueur(self, joueur):
        # Si le joueur entre en contact avec la pokeball
        if self.x-10<= joueur.pos[0] and self.x+10>= joueur.pos[0] and self.y-30 == joueur.pos[1]:
            return True
        else:
            return False

# On teste le contact entre le joueur et la pokeball
# On renvoie un booléen car, pour retirer la pokeball (le widget), on aura besoin de faire un test booleen