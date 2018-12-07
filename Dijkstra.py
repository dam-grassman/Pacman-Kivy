"""

Ce script contient les fonctions que nous utilisons pour
l'algorithme de Dijkstra.

"""

########################################################################

###### Imports

#######################################################################

from heapq import *
import math

def distance(pointA, pointB):
    """Calcul de la distance euclidienne entre deux points du plan"""
    return math.sqrt((pointA[0]-pointB[0])**2 + (pointA[1]-pointB[1])**2)


def graphe(liste_de_voisins, liste_de_points):

    """Création d'un graphe (sous forme de dictionnaire) à l'aide d'une liste de points
    et d'une liste indiquant les couples/triplets de voisins"""

    gr={}
    for i in range(1,len(liste_de_voisins)+1):
        gr[i]=[]
        for j in liste_de_voisins[i-1]:
            gr[i].append((distance(liste_de_points[j],liste_de_points[i]), j))
    return(gr)

def voisins(s,graph):
    """ ceci retourne les voisins du point s dans le graphe graph"""
    return graph[s]

def dijkstra (s, t, graph):

    '''On implémente l'algorithme de Dijkstra à l'aide du graphe défini ci-dessus/
     On calcule alors la liste des points successifs qui minimise la distance (pondéré) entre le point s et le point t'''

    M = set()
    d = {s: 0}
    p = {}
    suivants = [(0, s)]

    while suivants != []:

        dx, x = heappop(suivants)
        if x in M:
            continue

        M.add(x)

        for w, y in voisins(x,graph):
            if y in M:
                continue
            dy = dx + w
            if y not in d or d[y] > dy:
                d[y] = dy
                heappush(suivants, (dy, y))
                p[y] = x

    path = [t]
    x = t
    while x != s:
        x = p[x]
        path.insert(0, x)

    return d[t], path


def argmin(f, l, j):

    '''Cette fonction qui nous servira plus tard, retourne l'indice du minimum d'une liste'''

    arg = j
    for i in range(len(l)):
        if f(l[i]) < f(arg):
            arg = l[i]
    return arg