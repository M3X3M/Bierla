import random

class Member:
    def __init__(self, names, birthday, pictures, statements):
        #initialising the names of the member, they need to be provided
        try:
            self.first_name = names[0]
            self.middle_name = names[1]
            self.last_name = names[2]
        except:
            print("Name-setting-Error")
            return

        self.birthday = birthday
        
        #TODO: Bilder aus den Ordnern holen
        #initialising the locations where the pictures are stored
        self.pictures = []
        if pictures[0] != None:
            for picture in pictures:
                self.pictures.append(picture)

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
        current_pos = self.picture_iterator

        #checking if we reached the end of the array
        if self.picture_iterator + 1 < len(self.pictures):
            self.picture_iterator = self.picture_iterator + 1
        else:
            self.picture_iterator = 0

        return self.pictures[current_pos]


    #getting a statement of the statement array. Is aware of its position in 
    #the array and will give the next statement each time it is called
    #if we reach the end of the array we just restart
    def getNextStatement(self):
        current_pos = self.statement_iterator

        #checking if we reached the end of the array
        if self.statement_iterator + 1 < len(self.statements):
            self.statement_iterator = self.statement_iterator + 1
        else:
            self.statement_iterator = 0

        return self.statements[current_pos]

    #getting the birthday of the member
    def getBirthday(self):
        return self.birthday



