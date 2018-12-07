"""

On crée une classe héritée de la classe Widget et dont les murs sont une instance

"""

####################################################################################################

###Imports

####################################################################################################

from kivy import require
from kivy.uix.widget import Widget
from couloirs import couloir
from Dijkstra import *
from couloirs import *

require('1.9.1')# version de Kivy utilisée dans ce script

####################################################################################################

###Classe des points

####################################################################################################

point_a_manger = []
# liste des coordonnées des points que le joueur doit absorber

for a0, a1, b0, b1 in couloir:
    if a0 == b0:
        for j in range(int(a1) + 20, int(b1) - 20, 20):
            #On place des points régulièrement espacés dans les couloirs verticaux (sauf extrémités)
            point_a_manger.append([a0 + 38.5, j + 38.5])
            #On centre les points
    else:
        for j in range(int(a0), int(b0), 20):
            #On place des points régulièrement espacés dans les couloirs horizontaux
            point_a_manger.append([j + 38.5, a1 + 38.5])

point_a_manger = point_a_manger[:191]
#On se restreint au 191 premiers points blancs(cad de 0 à 190), on ne veut pas de points dans le passage secret

ensemble = [i for i in range(len(point_a_manger)) if i not in [179, 170]]
# la liste "ensemble" va servir pour que l'on actualise les points blancs qu'il reste dans le jeu. On supprimera des élements de cette liste au fur et à mesure du jeu.

ens_point= ensemble.copy()
#On crée une copie de "ensemble" pour disposer de l'ensemble des points blancs. Cette liste nous servira en autre pour calculer le score de la strategie du 2nd fantôme

def voisins_points():

    ''' Cette fonction nous permet de créer un dictionnaire qui à chaque point blanc associe la liste des points blancs voisins à moins de 60pixels de distance '''

    dico_points_voisins = {}
    for i in ensemble:
        l = []
        for j in ensemble:
            if j != i and distance(point_a_manger[i], point_a_manger[j]) <= 60:
                l.append(j)
        dico_points_voisins[i]=(l,1)
    return dico_points_voisins

dico_points_voisins = voisins_points()


def pls_pr_voisins_pt():

    '''  Fonction qui associe a chaque points blancs le point du graphe le plus proche \
     Cela nous servira en autre aux strategies des fanômes qui fonctionnent sur les points du graphe'''

    dico={}
    for i in ens_point:
        coord=point_a_manger[i]
        proche = 1
        dist = distance(dpoint[1], coord)
        for j in range(1,31):
            if distance(dpoint[j],point_a_manger[i])<dist:
                proche=j
                dist=distance(dpoint[j],point_a_manger[i])
        dico[i]=proche
    return dico

dico_pls_pr_voisins_point= pls_pr_voisins_pt()
#On dispose maintenant du dictionnaire des points du graphe les plus proches des points blancs à manger


####################################################################################################

###Classe des points

####################################################################################################

class Points(Widget):

    """ Les points permettent au joueur d'augmenter son score et de finir la partie"""

    def bounce_joueur(self, joueur):

        """ Si le joueur entre en contact avec le point """

        if [self.x-38.5, self.y-38.5] == joueur.pos:
            return True
        else:
            return False