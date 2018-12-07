"""

On crée une classe héritée de la classe Widget et dont les fantômes du Pacman seront des instances

"""

####################################################################################################

###Imports

####################################################################################################

from kivy import require
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,StringProperty
from kivy.vector import Vector
from couloirs import dpoint, couloir, liste_voisins, graph
from Dijkstra import dijkstra, distance, argmin
from random import randint
from points import *
from math import *

require('1.9.1')# version de Kivy utilisée dans ce script

####################################################################################################

#Classe du Fantome

####################################################################################################

class Fantome(Widget):
    """ Il s'agit du fantôme qui poursuit le joueur pour l'éliminer. Cette classe est similaire à celle
     du player, plus d'informations sont disponibles dans sa classe """
    objectif=0
    evolution = 0
    pt_proche = 26
    sp = StringProperty("Images/fantominus_left.gif")
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(-1)
    elan = (0, -1)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    strat = (0, [])


    def direction(self):
        """ Cette première méthode permet de donner au fantôme une direction au hasard """
        dep = randint(0,3)
        if dep == 0 :
            self.velocity = (-1, 0)
        if dep == 1 :
            self.velocity = (1, 0)
        if dep == 2 :
            self.velocity = (0, 1)
        if dep == 3 :
            self.velocity = (0, -1)


    def move(self, aleatoire=True):

        """ Méthode permettant de faire avancer le fantôme tout en tenant compte des
        contraintes du terrain (mur) """

        ancienne_pos = self.pos.copy()

        for corr in couloir:
            if (corr[0] <= self.velocity_x + self.pos[0]) and (corr[2] >= self.velocity_x + self.pos[0]) and \
                    (corr[1] <= self.velocity_y + self.pos[1]) and (corr[3] >= self.velocity_y + self.pos[1]): #les tests permettent de s'assurer que le fantôme sera dans les limites du labyrinthe s'il effectue un mouvement
                self.pos = Vector(*self.velocity)+self.pos
                self.elan = self.velocity.copy()
                if self.velocity == [-1, 0]:
                    if self.evolution == 1:
                        self.sp = "Images/spectrum_left.gif"
                    elif self.evolution == 2 :
                        self.sp = "Images/ectoplasma_left.gif"
                    else:
                        self.sp = "Images/fantominus_left.gif"
                if self.velocity == [1, 0]:
                    if self.evolution == 1:
                        self.sp = "Images/spectrum_right.gif"
                    elif self.evolution == 2:
                        self.sp = "Images/ectoplasma_right.gif"
                    else:
                        self.sp = "Images/fantominus_right.gif"

        if self.pos == ancienne_pos:
            for corr in couloir:
                if (corr[0] <= self.elan[0] + self.pos[0]) and (corr[2] >= self.elan[0] + self.pos[0]) and \
                        (corr[1] <= self.elan[1] + self.pos[1]) and (corr[3] >= self.elan[1] + self.pos[1]):
                    self.pos = Vector(*self.elan) + self.pos

        #si le fantôme ne peut pas avancer, même avec son élan, on lui donne une direction aléatoire
        if self.pos == ancienne_pos:
            if (self.strat[1] == [] or aleatoire) and ((self.pos[0],self.pos[1]) in dpoint):
                self.direction()
                self.move()

        #position du passage secret
        if self.pos == [dpoint[27][0], (dpoint[27][1])]:
            self.pos = [dpoint[30][0], (dpoint[30][1])]

        elif self.pos == [dpoint[30][0], (dpoint[30][1])]:
            self.pos =[dpoint[27][0], (dpoint[27][1])]

        #On calcule le point (du graphe) le plus proche

        self.pt_proche = \
            argmin(lambda x: distance(self.pos, dpoint[x]), liste_voisins[self.pt_proche - 1], self.pt_proche)

    def bounce_joueur(self, joueur):

        """ Décrit le comportement du fantôme en cas de collision avec le joueur """

        if self.collide_widget(joueur):
            self.size = 1, 1
            return True
        else:
            return False

    def strategie(self):

        """ Méthode à appeler pour que le fantôme numero1 effectue un mouvement suivant sa strategie"""

        try:
            if (self.pos[0], self.pos[1]) == dpoint[self.strat[1][0]]:
                self.strat = (self.strat[0], self.strat[1][1::])

            if (dpoint[self.strat[1][0]][1] - self.pos[1]) != 0:
                self.velocity = [0,(dpoint[self.strat[1][0]][1] - self.pos[1]) / abs(dpoint[self.strat[1][0]][1] - self.pos[1])]
            if (dpoint[self.strat[1][0]][0] - self.pos[0]) != 0:
                self.velocity = [(dpoint[self.strat[1][0]][0] - self.pos[0]) / abs(dpoint[self.strat[1][0]][0] - self.pos[0]), 0]
            self.move(False)
        except:
            self.move()

    def strategie_a_suivre(self, proche_joueur):

        """ Méthode qui indique les points à suivre pour effectuer le plus court chemin jusqu'au joueur \
        Cela concerne ici le premier fantôme """

        self.strat = dijkstra(self.pt_proche, proche_joueur, graph)


    def strategie_2(self, proche_joueur):

        """ On implémente uns seconde strategie qui vise a attribuer un score aux différents points et de retourner le point qui possède le plus gros score \
        On tient en compte les points voisins non consommés ainsi que la distance au PacMan """

        score = [ 0 for i in range(len(ens_point))]
        score[self.objectif]-=300
        for i in range(len(ens_point)):
            if dico_points_voisins[ens_point[i]][1]==1:
                score[i]+=25
            for j in dico_points_voisins[ens_point[i]][0]:
                if dico_points_voisins[j][1]==1:
                    score[i]+=20
            score[i]+= 200*max([(-1/500)*distance(dpoint[proche_joueur], point_a_manger[ens_point[i]]) + 1, 0])

        return score.index(max(score))

    def strategie_a_suivre2(self, proche_joueur):

        """ Méthode qui indique les points à suivre pour effectuer le plus court chemin jusqu'au joueur \
        Cela concerne le deuxième fantôme """

        self.objectif = self.strategie_2(proche_joueur)
        self.strat = dijkstra(self.pt_proche, dico_pls_pr_voisins_point[self.objectif], graph)







