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
from kivy.uix.modalview import ModalView

from member import Member
from error import Error
from rule import Rule
import rule

from functools import partial

from datetime import date

from animator import Animator

import widget_builder

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

#TODO: implement going on when parts of a member a missing

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
        self.lbl_news = self.designElements.ids['lblNews']
        self.lay_rules = self.designElements.ids['layRules']

        #the json store where permanent data is stored
        self.app_data_name = 'AppData.json'

        #creating the members carousel, to access it later in members carousel
        self.members_carousel = Carousel(direction='bottom', loop='True')

        #binding buttons with their callbacks
        self.btn_set_file_path.bind(on_press=self.showSetFilepathPopup)
        self.btn_refresh_members.bind(on_press=self.refreshCallback)
        self.btn_next_group_pic.bind(on_press = partial(self.changeGroupPic))

        #loading the currently stored data (if there is any)
        self.loadDataPath()

        #initialising the animator
        self.animator = Animator()

        #setting up the members by adding them into an array and then filling 
        # the array in the method
        self.members = []
        self.refresh()

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
                    member['lastname'], member['shortname']], 
                    member['birthday'], member['statements'], 
                    self.current_selected_path)

                self.members.append(tmp_member)
        except:
            print('No path')

    ############################################################################
    # rebuilding the memberscarousel from scratch by wiping the old one and 
    # filling the new one with the current state of the members array. The 
    # widget builder does is used for building new carousel
    ############################################################################
    def buildMembersCarousel(self):
        #removing the memberscarousel from the main one to rebuild it properly
        self.main_carousel.remove_widget(self.members_carousel)

        #refreshing the members carousel by reinitializing it
        self.members_carousel = Carousel(direction='bottom', loop='True')
        
        #either way we add the newly created members_carousel to the main one
        self.main_carousel.add_widget(widget_builder.buildMembersCarousel(
            self.members_carousel, self.members, self))

    ############################################################################
    # showing the new popup to chose the filepath where the app should look for 
    # its data
    # TODO: Update to widgetbuilder
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
        self.refresh()

        #closing the popup
        self.popup.dismiss()

    ############################################################################
    # used to refresh all the different arrays and pages
    ############################################################################
    def refresh(self):
        #refreshing the members array
        self.members.clear()
        self.fillMembersArray()

        self.buildMembersCarousel()

        #setting the label that counts detected members
        self.lbl_members_count.text = ("currently " + 
            str(len(self.members)) + " members detected")

        self.getGroupPictures()

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
        
        #setting the news array
        self.buildNews()
        #setting the first position of news Text is 0 ("Welcome")
        self.last_news_pos = 0

        #setting a clock to change news (if we have more than 1)
        if len(self.news_array) > 1:
            self.news_loop_clock = Clock.schedule_once(self.updateNewsLabel, 7)

        #building the rules page
        rules = rule.scanRules(self.current_selected_path + '/rules.json')
        widget_builder.buildRules(rules, self.lay_rules)

    ############################################################################
    # direct callback for refresh button
    # TODO: Change with the other method "partial"
    ############################################################################
    def refreshCallback(self,instance):
        self.refresh()    

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

    ############################################################################
    # searching for the birthday that is closest in the future to the current
    # date
    ############################################################################
    def getNextBirthday(self, membersArray):
        #getting the values for the current date seperatly forced to int
        current_day = int(date.today().strftime('%d'))
        current_month = int(date.today().strftime('%m'))
        current_year = int(date.today().strftime('%Y'))

        #building the date
        current_date = date(current_year, current_month, current_day)

        #currently closest in days
        closest_days = 365
        
        #postion of for loop
        member_index = 0

        closest_member = membersArray[0]

        for member in membersArray:
            birth_month = int(member.getBirthdayMonth())
            birth_day = int(member.getBirthdayDay())

            #we now need to check what year we add to the birthday in order to 
            # calculate the correct amount of days that each birthday is away
            # from the current date
             
            # if the month is smaller it will set it to next year
            if int(birth_month) < current_month:
                birthdate_whole = date(current_year + 1, int(birth_month), 
                    int(birth_day))

            # if the month is bigger it will set it to this year
            elif int(birth_month) > current_month:
                birthdate_whole = date(current_year, int(birth_month), 
                    int(birth_day))

            # if the month is equal we check the days
            else:
                #if the day is smaller it will set it to next year
                if int(birth_day) < current_day:
                    birthdate_whole = date(current_year + 1, int(birth_month), 
                        int(birth_day))

                # if the day is bigger or equal it will set it to this year
                else:
                    birthdate_whole = date(current_year, int(birth_month), 
                        int(birth_day))

            #we use the datetime library to calculate the amount of days between 
            # the dates
            delta = birthdate_whole - current_date
            
            #if the current members birthday is less days away, we set it to the 
            # closest members birthday
            if delta.days < closest_days:
                closest_days = delta.days
                closest_member = membersArray[member_index]


            member_index = member_index + 1

        #returning the member with the closest birthdate
        return closest_member

    ############################################################################
    # building the array of different news to display on the main page
    ############################################################################
    def buildNews(self):
        self.news_array = []
        self.news_array.append("Welcome!")

        # checking if the membersarray is empty first
        if self.members != []:
            birthday_member = self.getNextBirthday(self.members)

            birthday_text = ("Next birthday: " + birthday_member.getBirthdayDay() + 
                "." + birthday_member.getBirthdayMonth() + " (" + 
                birthday_member.getName(1) + ")")

            self.news_array.append(birthday_text)


    ############################################################################
    # updating the news label
    ############################################################################
    def updateNewsLabel(self, instance):
        #unscheduling the running clock (if there is one)
        Clock.unschedule(self.news_loop_clock)

        rand_num = self.pickRandomExcludingLast(0, len(self.news_array)-1, 
            self.last_news_pos)

        #translating the number into a text of our array
        new_text = self.news_array[rand_num]

        #resetting the last number
        self.last_news_pos = rand_num

        #completing the animation using the animator
        self.animator.changeText(self.lbl_news, 2, new_text) 

        #scheduling the new clock to redo the whole animation
        self.news_loop_clock = Clock.schedule_once(self.updateNewsLabel, 10)

    def on_pause(self):
        return False

    def on_resume(self):
        pass
        


if __name__ == '__main__':
    ForFriendsApp().run()