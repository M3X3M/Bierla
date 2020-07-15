import kivy

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.utils import rgba
from kivy.uix.carousel import Carousel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.button import Button
from kivy.storage.jsonstore import JsonStore

from member import Member

import json

# very important see documentation
kivy.require("1.11.1")

class DesignElements(Widget):
    pass

class BierlaApp(App):

    def build(self):
        #initializing the elements from the .kv file
        self.designElements = DesignElements()
        self.main_carousel = self.designElements.ids['crsMain']
        self.members_carousel = self.designElements.ids['crsMembers']
        self.btn_set_file_path = self.designElements.ids['btnSetFilepath']
        self.lbl_file_path = self.designElements.ids['lblFilePath']

        #the json store where permanent data is stored
        self.app_data_name = 'AppData.json'

        #binding buttons with their callbacks
        self.btn_set_file_path.bind(on_press=self.showSetFilepathPopup)

        #loading the currently stored data (if there is any)
        self.loadDataPath()

        #setting up the members
        self.members = []
        self.fillMembersArray()
        self.buildMembersCarousel()

        return self.designElements

    def loadDataPath(self):
        store = JsonStore(self.app_data_name)

        #recalling path where the data of the app is stored
        self.current_selected_path = store.get('path')['value']
        self.lbl_file_path.text = self.current_selected_path

    #filling the members array with the members. Will be used to read
    #json file later     
    def fillMembersArray(self):
        with open(self.current_selected_path + '/members.json', 'r') as file:
            data = file.read()

        obj = json.loads(data)

        
        #max = Member(["max","nax","wlasax"],['Test.jpg','Test2.jpg'],["ja ich wars"])
        #oli = Member(["schmolli","wolli","trolli"],['Test.jpg','Test2.jpg'],["lel"])
        #simon = Member(["simon","riemon","ziehmon"],['Test.jpg','Test2.jpg'],["ich weiß"])

        #self.members.append(max)
        #self.members.append(oli)
        #self.members.append(simon)

    #buildes the different pages of the members carousel
    def buildMembersCarousel(self):
        for member in self.members:
            #creating the layout that holds all the fields
            layout = FloatLayout()

            person_image = Image(source=member.getNextPicture(), allow_stretch=True, 
                pos_hint={'x':.2, 'top':.99}, size_hint=(.6,.3))

            layout_names = BoxLayout(orientation='horizontal', 
                pos_hint={'x':.1, 'y':.6}, size_hint=(.8,.1))
            lbl_names = Label(text=member.getName(1) + " " + '[i]' + 
                member.getName(2) + '[/i]' + " " + member.getName(3), markup=True, 
                font_size='40dp')
            layout_names.add_widget(lbl_names)

            lbl_statement = Label(text=member.getNextStatement(), font_size='25dp', 
                pos_hint={'x':.1, 'y':.2}, size_hint=(.8,.4))
            
            layout.add_widget(lbl_statement)
            layout.add_widget(person_image)
            layout.add_widget(layout_names)

            self.members_carousel.add_widget(layout)

    #creating the popup that lets the user select the path to the apps datafiles
    def showSetFilepathPopup(self, instance):
        popup_layout = FloatLayout()

        self.file_chooser = FileChooserIconView(pos_hint={'x':0,'top':1}, size_hint=(1,.9))
        select_button = Button(text="select", pos_hint={'x':.4, 'bottom':.5}, size_hint=(.2,.1))
        select_button.bind(on_press=self.saveSelectedPath)

        popup_layout.add_widget(self.file_chooser)
        popup_layout.add_widget(select_button)

        self.popup = Popup(title='Select where the Data for the app is stored',
            content=popup_layout, size_hint=(.9,.9))
        self.popup.open()

    #callback for button on selectpath popup
    def saveSelectedPath(self, instance):
        path = self.file_chooser.path

        #storing the path in a jsonStore as said in kivy-documentation
        store = JsonStore(self.app_data_name)
        store.put('path', value=path)

        #refreshing the label showing the current path
        self.lbl_file_path.text = path

        #closing the popup
        self.popup.dismiss()

if __name__ == '__main__':
    BierlaApp().run()