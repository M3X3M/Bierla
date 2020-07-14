import kivy

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.utils import rgba
from kivy.uix.carousel import Carousel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image

from member import Member

# very important see documentation
kivy.require("1.11.1")

class DesignElements(Widget):
    pass

class BierlaApp(App):

    def build(self):
        self.designElements = DesignElements()
        self.main_carousel = self.designElements.ids['crsMain']
        self.members_carousel = self.designElements.ids['crsMembers']
        self.members = []
        self.fillMembersArray()
        self.buildMembersCarousel()

        return self.designElements

    #filling the members array with the members. Will be used to read
    #json file later     
    def fillMembersArray(self):
        max = Member(["max","nax","wlasax"],['Test.jpg','Test2.jpg'],["ja ich wars"])
        oli = Member(["schmolli","wolli","trolli"],['Test.jpg','Test2.jpg'],["lel"])
        simon = Member(["simon","riemon","ziehmon"],['Test.jpg','Test2.jpg'],["ich weiß"])

        self.members.append(max)
        self.members.append(oli)
        self.members.append(simon)

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



if __name__ == '__main__':
    BierlaApp().run()