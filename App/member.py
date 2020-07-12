class Member:
    def __init__(self, names, pictures, sayings):
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
