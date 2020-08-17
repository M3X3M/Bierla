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
from error import Error

from functools import partial

import json

# very important see documentation
kivy.require("1.11.1")

class DesignElements(Widget):
    pass

class BierlaApp(App):

    ############################################################################
    # first function called in when the program is launched. It is used to 
    # map all objects
    ############################################################################
    def build(self):
        #initializing the elements from the .kv file
        self.designElements = DesignElements()
        self.main_carousel = self.designElements.ids['crsMain']
        self.btn_set_file_path = self.designElements.ids['btnSetFilepath']
        self.lbl_file_path = self.designElements.ids['lblFilePath']
        self.btn_refresh_members = self.designElements.ids['btnRefreshMembers']
        self.lbl_members_count = self.designElements.ids['lblMembersCount']

        #the json store where permanent data is stored
        self.app_data_name = 'AppData.json'

        #creating the members carousel, to access it later in members carousel
        self.members_carousel = Carousel(direction='bottom', loop='True')

        #binding buttons with their callbacks
        self.btn_set_file_path.bind(on_press=self.showSetFilepathPopup)
        self.btn_refresh_members.bind(on_press=self.refreshCallback)

        #loading the currently stored data (if there is any)
        self.loadDataPath()

        #setting up the members by adding them into an array and then filling 
        # the array in the method
        self.members = []
        self.refreshMembers()

        #initialising the errors class // Not Functional at the moment
        self.error = Error()

        #kivy thing
        return self.designElements

    ############################################################################
    # loading the already safed paths of the appData (permantently saved data)
    # if there is none, all the paths are set as stated in this function
    ############################################################################
    def loadDataPath(self):
        store = JsonStore(self.app_data_name)

        #recalling path where the data of the app is stored
        try:
            self.current_selected_path = store.get('path')['value']
            self.lbl_file_path.text = self.current_selected_path
        except:
            self.current_selected_path = ""
            self.lbl_file_path.text = ""

    ############################################################################
    # adding all the members out of the stored appdata into the members array
    # if there is none it will just print to console
    ############################################################################
    #filling the members array with members from the members.json file  
    def fillMembersArray(self):
        self.loadDataPath()
        try:
            with open(self.current_selected_path + '/members.json', 
                'r') as file:
                data = file.read()

            members_dict = json.loads(data)

            for member in members_dict:
                tmp_member = Member([member['firstname'], member['middlename'], 
                    member['lastname']], member['birthday'], 
                    member['statements'], self.current_selected_path)

                self.members.append(tmp_member)
        except:
            print('No path')

    ############################################################################
    # TODO: Split further, methode is too long
    # rebuilding the memberscarousel from scratch by wiping the old one and 
    # filling the new one with the current state of the members array. For the 
    # different members there are different buttons so they need to by binded 
    # to functions with some different attributes. The whole design of the 
    # carousel is designed here
    ############################################################################
    def buildMembersCarousel(self):
        #removing the memberscarousel from the main one to rebuild it properly
        self.main_carousel.remove_widget(self.members_carousel)

        #removing all contend from the current members carousel
        self.members_carousel.clear_widgets()

        #checking if there are members in the array, if not creating a 
        #page showing that there are no members detected
        if len(self.members) == 0:
            no_members_label = Label(text="No members found", font_size='50dp')
            self.members_carousel.add_widget(no_members_label)
        else:
            loop_counter = 0
            for member in self.members:
                #creating the layout that holds all the fields
                layout = FloatLayout()

                person_image = Image(source=member.getNextPicture(), 
                    allow_stretch=True, 
                    pos_hint={'x':.2, 'top':.99}, size_hint=(.6,.3))

                btn_next_picture = Button(background_normal='', 
                    background_color=rgba(0,0,0,0), 
                    pos_hint={'x':.2, 'top':.99}, size_hint=(.6,.3))

                btn_next_picture.bind(on_press=partial(self.nextPictureCallback, 
                    loop_counter, person_image))

                layout_names = BoxLayout(orientation='horizontal', 
                    pos_hint={'x':.1, 'y':.6}, size_hint=(.8,.1))
                lbl_names = Label(text=member.getName(1) + " " + '[i]' + 
                    member.getName(2) + '[/i]' + " " + member.getName(3), 
                    markup=True, font_size='40dp')
                layout_names.add_widget(lbl_names)

                btn_statement = Button(text=member.getNextStatement(), 
                    font_size='25dp', background_normal='', 
                    background_color=rgba(0,0,0,0),
                    pos_hint={'x':.1, 'y':.2}, size_hint=(.8,.4))

                btn_statement.bind(on_press=partial(self.nextStatementCallback, 
                    loop_counter, btn_statement))

                lbl_birthday = Label(text=member.getBirthday(), 
                    font_size='20dp', pos_hint={'x':.2, 'bottom':1}, 
                    size_hint=(.6,.1))

                #adding a vertical row of buttons to quickly navigate to 
                # specific members
                layout_scroller = BoxLayout(orientation='vertical', 
                    pos_hint={'right':1, 'bottom':1}, size_hint=(.1,1))

                #using a counter var for the position of the members in 
                # their array
                count = 0

                #looping through the members and creating a button for each one
                for member_btn in self.members:
                    #if we are on the specific slide of a member the specific 
                    # button should be colored accordingly
                    if member.getName(1) == member_btn.getName(1):
                        tmp_button = Button(text=member_btn.getName(1), 
                            id='btnJump' + member_btn.getName(1), 
                            font_size='25dp', background_color=rgba(0,0,0,0))
                    else:
                        tmp_button = Button(text=member_btn.getName(1), 
                            id='btnJump' + member_btn.getName(1), 
                            font_size='25dp', background_normal = '', 
                            background_color=rgba('0F0F0F'))

                    tmp_button.bind(on_press=partial(self.jumpToMember, count))
                    layout_scroller.add_widget(tmp_button)
                    count = count + 1
                
                layout.add_widget(layout_scroller)
                layout.add_widget(lbl_birthday)
                layout.add_widget(btn_statement)
                layout.add_widget(person_image)
                layout.add_widget(layout_names)
                layout.add_widget(btn_next_picture)

                self.members_carousel.add_widget(layout)

                loop_counter = loop_counter + 1
        
        #either way we add the newly created members_carousel to the main one
        self.main_carousel.add_widget(self.members_carousel)

    ############################################################################
    # showing the new popup to chose the filepath where the app should look for 
    # its data
    ############################################################################
    def showSetFilepathPopup(self, instance):
        popup_layout = FloatLayout()

        self.file_chooser = FileChooserIconView(pos_hint={'x':0,'top':1}, 
            size_hint=(1,.9))
        select_button = Button(text="select", pos_hint={'x':.4, 'bottom':.5}, 
            size_hint=(.2,.1))
        select_button.bind(on_press=self.saveSelectedPath)

        popup_layout.add_widget(self.file_chooser)
        popup_layout.add_widget(select_button)

        self.popup = Popup(title='Select where the Data for the app is stored',
            content=popup_layout, size_hint=(.9,.9))
        self.popup.open()

    ############################################################################
    # callback for the button that confirms the selection of the apps path
    ############################################################################
    def saveSelectedPath(self, instance):
        path = self.file_chooser.path

        #storing the path in a jsonStore as said in kivy-documentation
        store = JsonStore(self.app_data_name)
        store.put('path', value=path)

        #refreshing the label showing the current path
        self.lbl_file_path.text = path

        #closing the popup
        self.popup.dismiss()

        #refreshing membersarry
        self.refreshMembers()

    ############################################################################
    # used to refresh the whole members array and all connected attributes. 
    # Automatically called after path changed and start. 
    # Also callback for refresh button in settings
    ############################################################################
    def refreshMembers(self):
        #refreshing the members array
        self.members.clear()
        self.fillMembersArray()

        self.buildMembersCarousel()

        #setting the label that counts detected members
        self.lbl_members_count.text = ("currently " + 
            str(len(self.members)) + " members detected")

    ############################################################################
    # direct callback for refresh button
    # TODO: Change with the other method "partial"
    ############################################################################
    def refreshCallback(self,instance):
        self.refreshMembers()      

    ############################################################################
    # jumping to a specific member in the carousel, where member number 
    # defines the number in the array
    ############################################################################
    def jumpToMember(self, memberNumber, instance):
        self.members_carousel.index = memberNumber 

    ############################################################################
    # callback fot the next statement Label/Button that changes to the next
    # next statement
    ############################################################################
    #on tap on the label, the next statement of a member is displayed
    def nextStatementCallback(self, memberNumber, label, instance):
        label.text = self.members[memberNumber].getNextStatement()

    ############################################################################
    # callback fot the next picture Label/Button that changes to the next
    # next picture
    ############################################################################
    def nextPictureCallback(self, memberNumber, image, instance):
        image.source = self.members[memberNumber].getNextPicture()

if __name__ == '__main__':
    BierlaApp().run()