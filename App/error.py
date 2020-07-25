import kivy

from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

# very important see documentation
kivy.require("1.11.1")

class Error:

    def __init__(self):
        pass

    def membersJsonParsingError(self):
        message = "An Error occured while trying to parse the Members.json File"
        self.showPopup(message)

    def showPopup(self, message):
        popup_layout = BoxLayout(orientation='vertical')

        button = Button(text="Fuck")
        text = Label(text=message)

        popup_layout.add_widget(text)
        popup_layout.add_widget(button)

        popup = Popup(title='ERROR',
            content=popup_layout, size_hint=(.5,.5))
        popup.open()

        button.bind(on_press=popup.dismiss)