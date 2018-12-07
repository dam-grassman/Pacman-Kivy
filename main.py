"""

Ceci est notre script principal contenant notre application. Il est possible de la
lancer en exécutant ce script ou en lancer le script "home.py" qui ouvre une
page d'accueil redirigant l'utilisateur vers cette application.

"""

####################################################################

### Imports

#####################################################################

from kivy.config import Config
Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '400')

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.label import Label
import time
from couloirs import *
from bouton_central import *
from fantome import *
from joueur import *
from points import *
from music import *
from classe_pokeball import *
from kivy.uix.screenmanager import Screen

require('1.9.1')# version de Kivy utilisée dans ce script

#####################################################################

### Classe Wall

#####################################################################
class Wall(Widget):
    pass

#####################################################################

###Classe du jeu Pacman

#####################################################################

class PacmanGame(Screen):

    """ Il s'agit de notre application, qui se met à jour régulièrement pour prendre en compte
    l'interaction avec l'utilisateur. On va instancier les fantômes, le joueur et le bouton """

    partie = 'EN COURS'
    joueur = Player()
    gost1 = Fantome()
    gost2 = Fantome()
    photo = Photo()
    temps = 0
    liste_point = ['point{0}'.format(i) for i in range(0, len(point_a_manger))]

    def chrono(self,dt):
        '''On enregistre le temps à l'appel de cette fonction'''
        self.temps = time.time()

    def score_temps(self):
        '''On caclule le score supplémentaire obtenue avec le temps de jeu\
        Plus on finie le jeu vite, plus on gagne de points '''
        return (max([500-(time.time()-self.temps), 0]))

    ##################### le keyboard

    def __init__(self, **kwargs):
        super(PacmanGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'up':
            self.joueur.velocity=(0,1)
        elif keycode[1] == 'down':
            self.joueur.velocity=(0,-1)
        elif keycode[1] == 'left':
            self.joueur.velocity=(-1,0)
        elif keycode[1] == 'right':
            self.joueur.velocity=(1,0)
        return True

    #####################La fonction updtate

    def update(self, dt):

        '''cette methode met a jour le jeu, entre le déplacement du joueur, la strategie des fantômes, etc ...'''

        ## Tant que la partie est en cours :
        if self.partie == 'EN COURS':
            self.joueur.move()
            self.joueur.move()

            #Si on attrape la pokeball, on l'ajoute au pokedex
            if self.pokeball.bounce_joueur(self.joueur):
                self.remove_widget(self.pokeball)
                self.joueur.pokedex = 1

            #On regarde si Sacha attrape des points blancs
            for i in reversed(range(len(ensemble))):
                if (self.joueur.pos[0] <= point_a_manger[ensemble[i]][0] - 20) and (
                    self.joueur.pos[0] >= point_a_manger[ensemble[i]][0] - 50) \
                        and (self.joueur.pos[1] <= point_a_manger[ensemble[i]][1] - 20) and (
                    self.joueur.pos[1] >= point_a_manger[ensemble[i]][1] - 50):
                    #Si oui, on retire le Widger du point, ainsi que sa position dans la liste "ensemble" puis on incrémente le score
                    self.remove_widget(globals()['point{0}'.format(ensemble[i])])
                    dico_points_voisins[ensemble[i]]=(dico_points_voisins[ensemble[i]][0],0)
                    del ensemble[i]
                    self.joueur.score += 1

                    #S'il n'y a plus de points à manger, on a gagné
                    if ensemble==[]:
                        self.partie = 'GAGNE'
                        self.joueur.score += ceil(self.score_temps())



            # On s'interresse au contact etre Sacha et un fantôme suivant qu'il possède une pokeball ou non
            for gost in [self.gost1, self.gost2]:
                #Si aucune pokeball, sacha se fait manger et la partie est finie
                if self.joueur.pokedex == 0:
                    if distance(self.joueur.pos, gost.pos) <= tx / 2:
                        self.remove_widget(self.joueur)
                        self.partie = 'GAME OVER'

                #sinon Sacha attrape le fantôme
                else:
                    if distance(self.joueur.pos, gost.pos) <= tx / 2:
                        self.remove_widget(gost)
                        self.add_widget(Pokeball(ima="Images/pokeball2.gif", pos=[gost.pos[0] + 20, gost.pos[1] + 20],
                                                 size=(50, 50)))
                        gost.pos = [0, 0]
                        del gost
                        self.joueur.pokedex = 0
                        #Manger un fantôme rajoute des points au score
                        self.joueur.score += 200

        #si la parti est finie, on arrete de jouer : suivant que l'on a gagné ou perdu, on affiche le label et le score en conséquence
        else:
            if self.partie == 'GAME OVER':
                label = Label(text='GAME OVER\nSCORE={0}'.format(self.joueur.score), font_size=200)
                self.add_widget(label)
            else :
                label = Label(text='BRAVO\nSCORE={0}'.format(self.joueur.score), font_size=150)
                self.add_widget(label)

    def update_gost1(self,dt):
        '''On update la position du 1er fantôme\
         1fois s'il n'a pas évolué et jusqu'a 3fois s'il est dans sa dernière évolution (le fantôme ira alors 3fois plus vite)'''
        for i in range(self.gost1.evolution+1):
            self.gost1.strategie()

    def update_gost2(self,dt):
        '''De même pour le second fantôme, qui possède une statégie différente'''
        for i in range(self.gost2.evolution+1):
            self.gost2.strategie()

    def faire_strategie1(self,dt):
        '''On update alors la stratégie que doit suivre le 1er fantôme'''
        self.gost1.strategie_a_suivre(self.joueur.pt_proche)

    def faire_strategie2(self,dt):
        '''On update alors la stratégie que doit suivre le 2nd fantôme'''
        self.gost2.strategie_a_suivre2(self.joueur.pt_proche)

    def evolution(self,dt):
        ''' On fait évoluer les fantôme à l'appel de cette fonction'''
        if self.gost1.evolution ==0 and self.gost2.evolution ==0:
            self.gost1.evolution = 1
            self.gost2.evolution = 1
        else :
            self.gost1.evolution = 2
            self.gost2.evolution = 2

    def commencer(self):
        '''On commence par rajouter tout les widgets des points sur la map suivant leur position donné par la liste 'liste_a_manger' '''
        for i in range(0, len(point_a_manger)):
            if i != 179 and i != 170:
                globals()[self.liste_point[i]] = Points(pos=point_a_manger[i], size=(5, 5))
                self.add_widget(globals()[self.liste_point[i]])

#####################################################################

###Classe de l'application

#####################################################################

class PacmanApp(App):
    '''Classe de notre application'''
    title = "Pacman - Grasset/Randrianarisoa"
    debut = time.clock()
    def build(self):
        ''' Cette méthode crée le jeu, déclenche les départs des fantômes et rafraichit ensuite la fénetre à l'aide de la fonction Clock.shedule_interval '''
        game = PacmanGame()
        game.name = 'game'
        game.commencer()
        def retard(self):
            Clock.schedule_interval(game.update_gost2, 1.0 / 60.0)
        Clock.schedule_once(retard,15)
        Clock.schedule_interval(game.update_gost1, 1.0/60.0)
        Clock.schedule_interval(game.faire_strategie1, 5)
        Clock.schedule_interval(game.faire_strategie2, 5)
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        Clock.schedule_once(game.evolution, 50)
        Clock.schedule_once(game.evolution, 25)
        Clock.schedule_once(game.chrono)
        return game

#####################################################################

if __name__ == '__main__':
    PacmanApp().run()