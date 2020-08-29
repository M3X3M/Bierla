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
from kivy.utils import platform
from kivy.uix.filechooser import FileSystemLocal
from kivy.clock import Clock
from kivy.animation import Animation

from member import Member
from error import Error

from functools import partial

from animator import Animator

import random

import json

# needed for kivy, see requirements
kivy.require("1.11.1")

if platform == 'android':
    from android.permissions import request_permissions, Permission
    request_permissions([
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.READ_EXTERNAL_STORAGE,
        Permission.INTERNET,
    ])
    from android.storage import primary_external_storage_path
    primary_ext_storage = primary_external_storage_path()

#TODO: Make config File
GROUP_FOLDER = 'Group'

class DesignElements(Widget):
    pass

class ForFriendsApp(App):

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
        self.im_group_pic = self.designElements.ids['imGroup']
        self.btn_next_group_pic = self.designElements.ids['btnNextGroup']

        #binding the corresponding callback to the button
        self.btn_next_group_pic.bind(on_press = partial(self.changeGroupPic))

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

        self.getGroupPictures()

        #initialising the animator
        self.animator = Animator()

        #setting the first image on the main page and starting the animation 
        # to animate the widget if there are multiple images
        if self.group_pictures == []:
            self.im_group_pic.source = "Resources/questionmark.png"
        elif len(self.group_pictures) == 1:
            self.im_group_pic.source = self.group_pictures[0]
        else:
            self.im_group_pic.source = self.group_pictures[0]
            self.last_group_picture_pos = 0
            self.group_loop_clock = Clock.schedule_once(self.changeGroupPic, 10)

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

        self.members_carousel = Carousel(direction='bottom', loop='True')

        #checking if there are members in the array, if not creating a 
        #page showing that there are no members detected
        if len(self.members) == 0:
            no_members_label = Label(text="No members found", font_size='20sp')
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
                    markup=True, font_size='20sp')
                layout_names.add_widget(lbl_names)

                btn_statement = Button(text=member.getNextStatement(), 
                    font_size='15sp', background_normal='', 
                    background_color=rgba(0,0,0,0),
                    pos_hint={'x':.1, 'y':.2}, size_hint=(.8,.4))

                btn_statement.bind(on_press=partial(self.nextStatementCallback, 
                    loop_counter, btn_statement))

                lbl_birthday = Label(text=member.getBirthday(), 
                    font_size='15sp', pos_hint={'x':.2, 'bottom':1}, 
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
                            font_size='5sp', background_color=rgba(0,0,0,0))
                    else:
                        tmp_button = Button(text=member_btn.getName(1), 
                            id='btnJump' + member_btn.getName(1), 
                            font_size='5sp', background_normal = '', 
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

        if platform == 'android':
            self.file_chooser = FileChooserIconView(pos_hint={'x':0,'top':1}, 
               size_hint=(1,.9), path=primary_ext_storage)
        else:
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

        #refreshing membersarry
        self.refreshMembers()

        #closing the popup
        self.popup.dismiss()

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
        self.animator.changePicture(image, 1, 
            self.members[memberNumber].getNextPicture())
        #image.source = self.members[memberNumber].getNextPicture()

    ############################################################################
    # building the array of available pictures in the all folder for the 
    # "featured" pictures on the main page
    ############################################################################
    def getGroupPictures(self):
        #creating an array holding all the paths
        self.group_pictures = []
        file_system = FileSystemLocal()

        try:
            # this returns a list of files in dir
            files = file_system.listdir(self.current_selected_path + '/' + 
                GROUP_FOLDER)

        except:
            # returnung an empty array
            files = []

            #DEBUG:
            print("no folder")

        #adding all .jpg or png files to the pictures array
        for file in files:
            #checking filetype
            if file[-4:] == '.jpg' or file[-4:] == '.png':
                complete_filepath = (self.current_selected_path + '/' + 
                    GROUP_FOLDER + '/' + file)
                self.group_pictures.append(complete_filepath)

        print(self.group_pictures)

    ############################################################################
    # callback for changing the picture on the main page. Called in intervals
    # doing all the preperation to start use the animator to change the 
    # picture with the according animation
    ############################################################################
    def changeGroupPic(self, instance):
        #unscheduling the running clock (if there is one)
        Clock.unschedule(self.group_loop_clock)

        #picking a random number, which cannot be last number that has been 
        # picked
        rand_num = self.pickRandomExcludingLast(0, len(self.group_pictures)-1, 
            self.last_group_picture_pos)
        
        #translating the number into a path of our array
        new_path = self.group_pictures[rand_num]

        #resetting the last number
        self.last_group_picture_pos = rand_num

        #completing the animation using the animator
        self.animator.changePicture(self.im_group_pic, 2, new_path)

        #scheduling the new clock to redo the whole animation
        self.group_loop_clock = Clock.schedule_once(self.changeGroupPic, 10)

    ############################################################################
    # recursivly finding a random number in a specified range, one number from 
    # the range is excluded for example for avoiding picking the last picked 
    # one
    ############################################################################
    def pickRandomExcludingLast(self, rangeStart, rangeEnd, exclusion):
        random_num = random.randint(rangeStart, rangeEnd)
        if random_num == exclusion:
            random_num = self.pickRandomExcludingLast(rangeStart, rangeEnd, 
                exclusion)
        
        return random_num

if __name__ == '__main__':
    ForFriendsApp().run()