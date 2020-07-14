import kivy

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.utils import rgba
from kivy.uix.carousel import Carousel
from kivy.uix.boxlayout import BoxLayout

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
        max = Member(["max","nax","wlasax"],[],["ja ich wars"])
        oli = Member(["schmolli","wolli","trolli"],[],["lel"])
        simon = Member(["simon","riemon","ziehmon"],[],["ich weiß"])

        self.members.append(max)
        self.members.append(oli)
        self.members.append(simon)

    #buildes the different pages of the members carousel
    def buildMembersCarousel(self):
        for member in self.members:
            #creating the layout that holds all the fields
            layout = BoxLayout(orientation='vertical')

            child1_layout_names = BoxLayout(orientation='horizontal')
            child1_firstname = Label(text=member.getName(1))
            child1_middlename = Label(text=member.getName(2))
            child1_lastname = Label(text=member.getName(3))
            child1_layout_names.add_widget(child1_firstname)
            child1_layout_names.add_widget(child1_middlename)
            child1_layout_names.add_widget(child1_lastname)
            
            layout.add_widget(child1_layout_names)

            self.members_carousel.add_widget(layout)



if __name__ == '__main__':
    BierlaApp().run()