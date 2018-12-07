"""

Ce script permet d'avoir une molette pour gérer le volume de la musique.

"""

####################################################################

### Imports

#####################################################################

from kivy import require
from kivy.uix.widget import Widget
from kivy.core.audio import SoundLoader
from kivy.uix.slider import Slider
from kivy.app import App

require('1.8.0')

class Volume_Slider(Widget):
    def __init__(self, **kwargs):
        super(Volume_Slider, self).__init__(**kwargs)
        s = SoundLoader.load("Musiques/Monody.mp3")
        slider = Slider(value=s.volume, min=0, max=1, orientation='vertical')
        s.play()
        s.bind(volume=slider.setter('value'))
        slider.bind(value=s.setter('volume'))
        self.add_widget(slider)


class MyApp(App):
    def build(self):
        return Volume_Slider()

if __name__ == '__main__':
    MyApp().run()
