class Member:
    def __init__(self, names, pictures, statements):
        #initialising the names of the member, they need to be provided
        try:
            self.first_name = names[0]
            self.middle_name = names[1]
            self.last_name = names[2]
        except:
            print("Name-setting-Error")
            return
        
        #initialising the location where the pictures are stored
        self.pictures = []
        for picture in pictures:
            self.pictures.append(picture)

        #initialising the statements of the member
        self.statements = []
        for statement in statements:
            self.statements.append(statement)

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

    def getPictures(self):
        return self.pictures

#max = Member(["max","lol","sack"], [], ["halo"])
#print(max.getName(2))

