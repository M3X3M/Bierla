import random

import kivy
from kivy.uix.filechooser import FileSystemLocal

# very important see documentation
kivy.require("1.11.1")

class Member:
    def __init__(self, names, birthday, statements, path):
        #initialising the names of the member, they need to be provided
        try:
            self.first_name = names[0]
            self.middle_name = names[1]
            self.last_name = names[2]
        except:
            print("Name-setting-Error")
            return

        self.birthday = birthday

        self.birth_day = self.birthday[0:2]

        self.birth_month = self.birthday[3:5]
        
        self.pictures = []
        self.findPictures(path)

        #initialising the statements of the member
        self.statements = []
        if statements != None:
            for statement in statements:
                self.statements.append(statement)
        else:
            self.statements.append("-")
        
        #starting to iterate at the first position of the corresponding arrays
        self.picture_iterator = 0
        self.statement_iterator = 0

        self.ShufflePictures()
        self.ShuffleStatements()

    #for getting a specific name. 1 = first-, 2 = middle-, 3 = last-name
    def getName(self, nameType):
        if nameType == 1:
            return self.first_name
        elif nameType == 2:
            return self.middle_name
        elif nameType == 3:
            return self.last_name

    def getStatements(self):
        return self.statements
    
    #shuffeling the pictures-array of this member, to get a new order
    def ShufflePictures(self):
        random.shuffle(self.pictures)

    #shuffeling the statements-array of this member, to get a new order
    def ShuffleStatements(self):
        random.shuffle(self.statements)

    #getting a picture of the picture array. Is aware of its position in 
    #the array and will give the next picture each time it is called
    #if we reach the end of the array we just restart
    def getNextPicture(self):
        #checking if we reached the end of the array
        #if there are no pics for this member, return ''
        if self.pictures == []:
            self.picture_iterator = 0
            return ''
        elif self.picture_iterator + 1 < len(self.pictures):
            self.picture_iterator = self.picture_iterator + 1
        else:
            self.picture_iterator = 0

        return self.pictures[self.picture_iterator]


    #getting a statement of the statement array. Is aware of its position in 
    #the array and will give the next statement each time it is called
    #if we reach the end of the array we just restart
    def getNextStatement(self):
        #checking if we reached the end of the array
        if self.statement_iterator + 1 < len(self.statements):
            self.statement_iterator = self.statement_iterator + 1
        else:
            self.statement_iterator = 0

        return self.statements[self.statement_iterator]

    #getting the birthday of the member
    def getBirthday(self):
        return self.birthday

    def findPictures(self, path):
        file_system = FileSystemLocal()
        files = file_system.listdir(path + '/' + self.first_name)   # this returns a list of files in dir of each member
        #adding all .jpg or png files to the pictures array
        for file in files:
            #checking filetype
            if file[-4:] == '.jpg' or file[-4:] == '.png':
                complete_filepath = path + '/' + self.first_name + '/' + file
                self.pictures.append(complete_filepath)

    def getBirthdayDay(self):
        return self.birth_day

    def getBirthdayMonth(self):
        return self.birth_month