import kivy

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.utils import rgba
from kivy.uix.gridlayout import GridLayout

# see documentation
kivy.require("1.11.1")

#TODO: Create the memberscarousel in this class!

class WrappedLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(
            width=lambda *x:
            self.setter('text_size')(self, (self.width, None)),
            texture_size=lambda *x: self.setter('height')(self, self.texture_size[1]))

################################################################################
# one row of a rule
################################################################################
def buildRules(rules, widget):
    top_lbl_id = 1.4

    for rule in rules:
        top_lbl_id -= .4 

        row = FloatLayout(size_hint_y=None, height=25)
        lbl_id = Label(text = str(rule.id), font_size = "20sp", size_hint_y=None, 
            pos_hint={"x":0, "top":top_lbl_id})

        row.add_widget(lbl_id)

        widget.add_widget(row)


################################################################################
# building the widget that holds the detailed view of a rule
################################################################################
def buildRuleView(name, id, text):
    main_layout = FloatLayout()

    header = Label(text=name, pos_hint={'center_x':.5, 'top':1}, 
        size_hint=(.2,.1), font_size="30sp", bold=True, color = rgba('#0a5e00'))

    body = WrappedLabel(text=text, font_size="20sp", 
        pos_hint={'center_x':.5,'center_y':.8}, size_hint=(.9,.9))

    main_layout.add_widget(header)
    main_layout.add_widget(body)

    return main_layout


    
