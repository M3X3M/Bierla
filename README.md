# ForFriends
## Information:
The ForFriends App is built using Python and the [Kivy](https://kivy.org/#home) library. As you can see here it is open source software, which means anyone can adapt and use this app as he wishes. I will slowly add all the mandatory to know things to join the developement for this app in this readme file.  
This project started out because I wanted to create an app for me and my friends. At the moment all the application does is displaying images, statements and birthdays of our friends.  
The aim for this app later on is that it helps managing our group by displaying events and managing polls, but this will still take a lot of time.  
If you like the idea of a friend managing software feel free to join developement. Feel free to open issues and requests if you encounter anything.
## How to use:
If you are just here to use the App, then look no further. Here are the basic instruction to install and use the app.
### 1) Installation
In the [Builds](/Builds) Folder you will find the finished applications that are ready to use. Currently the only prebuild package that are supplied are .apk files for Android.
### 2) App Data
For different reasons I decided that the app uses a dedicated folder on the normally accesible storage of the users device to get its data. I know it is far from perfect but this currently allows for quick manipulation from any user.
I prepaired the folder for our group but will share it with them on another platform to avoid putting personal data here on Github. The [prebuild folder](/ExampleFolder) shows how such a prebuild folder should be structured. A more detailed explanation will be added in another subsection.  
When you launch the app, swipe to the settings tab and press the button to select the path. This will open a file chooser. From here navigate to the location on your device where you saved the prepaired folder. Head into that folder and tap the select button. The App should now load all its data from the folder.
### 3) Adding Data
A member in this app is a kind of profile, including pictures, three names, birthdate and statements. Properties that are strings can be changed in the members.json file that lays in the root of the [prebuild folder](/ExampleFolder). First-, middle- and lastname must not be an array. However it is possible to have multiple statements, that will be shuffled in the app and can be skipped through within the app.  
Pictures are handled differently. For each member in members.json file there has to be a folder named exactly like the firstname property. These folders are holding the pictures for the corresponding members. At the start of the application it will search these folders for .png and .jpg files and add them to the members. So it is possible to add new pictures anytime.  
However it is recommended to add the pictures not only locally because the other users of the app won't see them. In our group we will have the prebuild folder laying in a cloud and new pictures should be added there, so any member can just override the old prebuild folder with the updated one.
## Known Issues
- Leaving the app on android without completely closing it and then trying to resume the app will result in a black screen. Just close the app completely and open it again and it should work. I'm trying to fix this issue asap.
- The font sizes are not properly tested on devices with different dpis and are not changing dynamically yet. Thus some lables go out of bounds. 
