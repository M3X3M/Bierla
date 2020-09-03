from kivy.animation import Animation
from kivy.uix.image import Image

from functools import partial

# a class for all the animation that are used in the app
class Animator():
    ############################################################################
    ############################################################################
    # MAIN METHODES
    ############################################################################
    ############################################################################

    ############################################################################
    # changing the source of the picture. By fading in and out using opacity
    # @widget the image of which the source should be changed
    # @duration the total duration the animation should take
    # @path the path of the new image
    ############################################################################
    def changePicture(self, widget, duration, path):
        self.fadeOutAnimImage(widget, duration/2 , path)

    ############################################################################
    # changing the text of a label by fading in and out using opacity
    # @widget the label which text should be changed
    # @duration the total duration the animation should take
    # @text the new text
    ############################################################################
    def changeText(self, widget, duration, text):
        self.fadeOutAnimLabel(widget, duration/2 , text)


    ############################################################################
    ############################################################################
    # SIDE METHODES
    ############################################################################
    ############################################################################

    ############################################################################
    # fading out the picture and binding the on complete method that will change 
    # source and refade the new image
    ############################################################################
    def fadeOutAnimImage(self, widget, duration, path):
        fadeOutAnim = Animation(opacity = 0, duration = duration)
        fadeOutAnim.bind(on_complete = partial(self.changeAndRefadeImage, 
            widget, duration, path))
        fadeOutAnim.start(widget)

    ############################################################################
    # changing the source of the image and fading it back in
    ############################################################################
    def changeAndRefadeImage(self, widget, duration, path, a, b):
        widget.source = path
        fadeInAnim = Animation(opacity = 1, duration = duration)
        fadeInAnim.start(widget)

    ############################################################################
    # fading out the label and binding the on complete method that will change 
    # text and refade the new label
    ############################################################################
    def fadeOutAnimLabel(self, widget, duration, text):
        fadeOutAnim = Animation(opacity = 0, duration = duration)
        fadeOutAnim.bind(on_complete = partial(self.changeAndRefadeLabel, 
            widget, duration, text))
        fadeOutAnim.start(widget)

    ############################################################################
    # changing the text of the label and fading it back in
    ############################################################################
    def changeAndRefadeLabel(self, widget, duration, text, a, b):
        widget.text = text
        fadeInAnim = Animation(opacity = 1, duration = duration)
        fadeInAnim.start(widget)
