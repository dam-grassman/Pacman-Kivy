"""

Ce script définit les couloirs du labyrinthe. Cela permet de dicter aux fantômes et au joueur les
positions qui lui sont accessibles dans la fenêtre.

"""

from Dijkstra import graphe

axx = 1200
orr = 400
tx = 77
ty = 77
px = 25
py = 25

couloir = []

# On crée un dictionnaire contenant les coordonnées des intersections entre les couloirs
# qui sont donc les positions où les personnages peuvent tourner

dpoint = {}

dpoint[1] = (tx + axx/100, orr/100 + 36)
dpoint[2] = (12*tx + 0.09*axx, orr/100 + 36)
dpoint[3] = (tx + axx/100, 3*ty + 0.04*orr + 36)
dpoint[4] = (12*tx + 0.09*axx, 3*ty + 0.04*orr + 36)

dpoint[5] = (3*tx + 0.02*axx, orr/100 + 36)
dpoint[6] = (3*tx + 0.02*axx, 3*ty + 0.04*orr + 36)

dpoint[7] = (6*tx + 0.04*axx, orr/100 + 36)
dpoint[8] = (6*tx + 0.04*axx, 3*ty + 0.04*orr + 36)

dpoint[9] = (8*tx + 0.06*axx, orr/100 + 36)
dpoint[10] = (8*tx + 0.06*axx, 3*ty + 0.04*orr + 36)

dpoint[11] = (10*tx + 0.08*axx, orr/100 + 36)
dpoint[12] = (10*tx + 0.08*axx, 3*ty + 0.04*orr + 36)

dpoint[13] = (2*tx + 0.02*axx, ty + 0.02*orr + 36)
dpoint[14] = (3*tx + 0.02*axx, ty+ 0.02*orr + 36)
dpoint[15] = (2*tx + 0.02*axx, 2*ty + 0.03*orr + 36)
dpoint[16] = (3*tx + 0.02*axx, 2*ty + 0.03*orr + 36)

dpoint[17] = (6*tx + 0.04*axx, ty + 0.02*orr + 36)
dpoint[18] = (7*tx + 0.05*axx, ty + 0.02*orr + 36)
dpoint[19] = (7*tx + 0.05*axx, 2*ty + 0.03*orr + 36)
dpoint[20] = (8*tx + 0.06*axx, 2*ty + 0.03*orr + 36)

dpoint[21] = (11*tx + 0.09*axx, ty + 0.02*orr + 36)
dpoint[22] = (12*tx + 0.09*axx, ty + 0.02*orr + 36)
dpoint[23] = (11*tx + 0.09*axx, 2*ty + 0.03*orr + 36)
dpoint[24] = (12*tx + 0.09*axx, 2*ty + 0.03*orr + 36)

dpoint[25] = (9*tx + 0.07*axx, orr/100 + 36)
dpoint[26] = (9*tx + 0.07*axx, ty + 0.02*orr + 36)

dpoint[27] = (0, int((3*ty + 0.04*orr)/2 + 36))
dpoint[28] = (tx + 0.01*axx, int((3*ty + 0.04*orr)/2 + 36))
dpoint[29] = (12*tx + 0.09*axx, int((3*ty + 0.04*orr)/2 + 36))
dpoint[30] = (13*tx + 0.09*axx, int((3*ty + 0.04*orr)/2 + 36))

# liste des couloirs qui sont définis par un quadruplet regroupant les abscisses et ordonnées de ses extrémités

couloir = [dpoint[1]+dpoint[2], dpoint[2]+dpoint[4], dpoint[1]+dpoint[3], dpoint[3]+dpoint[4], dpoint[5]+dpoint[6], dpoint[7]+dpoint[8], dpoint[9]+dpoint[10],
           dpoint[11]+dpoint[12], dpoint[13]+dpoint[14], dpoint[15]+dpoint[16], dpoint[17]+dpoint[18], dpoint[19]+dpoint[20],
           dpoint[21]+dpoint[22], dpoint[23]+dpoint[24], dpoint[25]+dpoint[26], dpoint[27]+dpoint[28], dpoint[29]+dpoint[30]]

# liste formée de listes à deux ou trois éléments qui sont les numéros de couples/triplets voisins

liste_voisins = [[28, 5], [11, 22], [28, 6], [12, 24], \
                 [1, 7, 17], [3, 8, 16], [5, 9, 17], [6, 10, 17],\
                 [7, 20, 25], [8, 12, 20], [2, 12, 25], [4, 10, 11],\
                 [14], [5, 13, 16], [16], [6, 14, 15], [7, 8, 18], [17],\
                 [20], [9, 10, 19], [22], [2, 21, 29], [24], [4, 29, 23],\
                 [9, 11, 26], [25], [28, 30], [1, 3, 27], [22, 24, 30], [27, 29]]

# graphe représentant les points (les voisins dans le graphe sont exactement les voisins dans le labyrinthe)

graph = graphe(liste_voisins, dpoint)
