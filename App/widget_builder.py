import kivy

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label

# see documentation
kivy.require("1.11.1")


def buildMemberView(name, id, text):
    main_layout = FloatLayout()

    header = Label(text=name, pos_hint={'x':.4, 'top':1}, 
        size_hint=(.2,.1))

    body = Label(text=text, pos_hint={'center_x':.1, 'center_y':.5}, 
        size_hint=(.8,.5))

    main_layout.add_widget(header)
    main_layout.add_widget(body)

    return main_layout


    
