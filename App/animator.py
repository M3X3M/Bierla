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
        self.fadeOutAnim(widget, duration/2 , path)

    ############################################################################
    ############################################################################
    # SIDE METHODES
    ############################################################################
    ############################################################################

    ############################################################################
    # fading out the picture and binding the on complete method that will change 
    # source and refade the new image
    ############################################################################
    def fadeOutAnim(self, widget, duration, path):
        fadeOutAnim = Animation(opacity = 0, duration = duration)
        fadeOutAnim.bind(on_complete = partial(self.changeAndRefade, 
            widget, duration, path))
        fadeOutAnim.start(widget)

    ############################################################################
    # changing the source of the image and fading it back in
    ############################################################################
    def changeAndRefade(self, widget, duration, path, a, b):
        widget.source = path
        fadeInAnim = Animation(opacity = 1, duration = duration)
        fadeInAnim.start(widget)
