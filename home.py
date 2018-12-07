"""

Ce script permet d'avoir une page d'accueil avant de lancer le jeu.

"""

####################################################################

### Imports

#####################################################################
from kivy.config import Config
Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '400')

#L'instruction qui suit permet de fixer la taille minimal de la fenetre, en cas de redimension, veuillez revenir à cette taille
from kivy.core.window import Window
Window.minimum_width = 1200
Window.minimum_height = 400

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,FallOutTransition
from main import *
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

####################################################################

### Fichier .kv de la fenêtre d'acceuil

#####################################################################

Builder.load_string("""
#:import Volume_Slider music.Volume_Slider

<Persos>:
    Image:
		source: root.im
		pos: root.pos
        size: 76, 76

<MenuScreen>:
    perso1: ectoplasma
    perso2: spectrum
    perso3: fantominus
    perso4: sacha

    canvas:
        Rectangle:
            source: "Images/background_bis.png"
            size: self.size
            pos: self.pos

    Persos:
        id: ectoplasma
        pos: 320,37

    Persos:
        id: spectrum
        pos: 397,37

    Persos:
        id: fantominus
        pos: 464,37

    Persos:
        id: sacha
        pos: 541,37

    Button:
        size_hint: 0.25,0.25
        pos: 20,37
        background_normal: "Images/jouer.png"
        on_press: root.manager.current_screen.add_widget(root.gaming.build()) ; root.manager.current_screen.add_widget(Volume_Slider())

    Button:
        size_hint: 0.20, 0.20
        pos: 880, 37
        text: "Règles"
        font_size: 30
        color: 162 / 255, 185 / 255, 245 / 255, 1
        background_color: 14 / 255, 18 / 255, 98 / 255, 1
        on_press: root.pop.open()

""")

#####################################################################

###Les classes visibles sur l'écran d'accueil

#####################################################################
b = BoxLayout(orientation='vertical', spacing=20)
p = Popup(title='Règles du jeu', title_size=30, title_color=[0 / 255, 255 / 255, 0/ 255, 1], \
          content=b, auto_dismiss=False, separator_color = [0/ 255, 255 / 255, 0/ 255, 1])
l = Button(text = 'Fermer', size_hint = (1, 0.2))
l.bind(on_press=p.dismiss)
b.add_widget(Label(text = " Le jeu auquel vous allez jouer s'apparente à un Pacman mais quelques règles diffèrent cependant: \
                            \n\n    -Le but du jeu est de consommer tous les points blancs du jeu. Le jeu se termine dès lors que tous les points blancs sont consommés et votre score s'affiche.\
                            \n\n    -Si un fantôme arrive à vous attraper, la partie est finie. Attention, les fantômes évoluent et leur vitesse augmente alors. \
                           \n\n    -Vous remarquerez la présence d'un pokeball : en vous en saisissant, vous pourrez attraper l'un des deux fantômes. \
                           \n\n      Mais attention, il n'y a qu'une seule pokeball sur le terrain, considérez la, une fois en main, comme une vie de secours!\
                            \n\n    -Votre temps est précieux, plus vous gagnez vite, plus votre score augmente !\
                          \n\n Voila, utilisez les flèches pour vous déplacer et que la chance soit avec vous !"))
b.add_widget(l)

class Persos(Widget):

    ''' On crée la classe des personnages que l'on peut voir sur l'écran d'accueuil. \
    Ces personnages servent d'animation lorsque l'on est sur la page d'acceuil'''

    photo_im = [StringProperty(""), StringProperty("")]
    im=photo_im[0]
    velocity_x = NumericProperty(2)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    avance = 260

    def move(self):
        if self.avance > 0:
            self.pos = Vector(*self.velocity) + self.pos
            self.avance -= 2
        else:
            self.velocity_x = - self.velocity_x
            self.avance = 260
            self.im = self.photo_im[min(int(self.velocity_x / abs(self.velocity_x)), 0)]


class MenuScreen(Screen):

    ''' On définit l'ecran d'accueil '''

    perso1 = Persos()
    perso2 = Persos()
    perso3 = Persos()
    perso4 = Persos()
    gaming = PacmanApp()
    gaming.load_kv()

    def photo(self):
        self.perso1.photo_im = ["Images/ectoplasma_right.gif", "Images/ectoplasma_left.gif"]
        self.perso1.im = self.perso1.photo_im[0]
        self.perso2.photo_im = ["Images/spectrum_right.gif", "Images/spectrum_left.gif"]
        self.perso2.im = self.perso2.photo_im[0]
        self.perso3.photo_im = ["Images/fantominus_right.gif", "Images/fantominus_left.gif"]
        self.perso3.im = self.perso3.photo_im[0]
        self.perso4.photo_im = ["Images/sacha_right.gif", "Images/sacha_left.gif"]
        self.perso4.im = self.perso4.photo_im[0]

    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.pop = p


    def update(self, dt):
        self.perso1.move()
        self.perso2.move()
        self.perso3.move()
        self.perso4.move()

class TestApp(App):
    title = "Pacman - Grasset/Randrianarisoa"
    def build(self):
        sm = ScreenManager(transition=FallOutTransition(duration=0.1))
        men = MenuScreen(name='menu')
        sm.add_widget(men)
        men.photo()
        Clock.schedule_interval(men.update, 1.0 / 6000.0)
        return sm

#####################################################################

if __name__ == '__main__':
    TestApp().run()