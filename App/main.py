import kivy

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.utils import rgba
from kivy.uix.carousel import Carousel

# very important see documentation
kivy.require("1.11.1")

class DesignElements(Widget):
    pass

class BierlaApp(App):

    def build(self):
        self.designElements = DesignElements()
        return self.designElements


if __name__ == '__main__':
    BierlaApp().run()