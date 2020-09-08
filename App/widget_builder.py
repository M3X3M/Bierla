import kivy

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.utils import rgba
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView

from functools import partial

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
# filling the scrollview
################################################################################
def buildRules(rules, widget):
    #starting position
    top_lbl_id = .8

    for rule in rules:
        #spacing in between rows
        top_lbl_id -= .4

        row = FloatLayout(size_hint_y=None, height=50)
        btn_id = Button(text = str(rule.id) + "." + 10*" " + rule.getName(), 
            font_size = "20sp", size_hint_y=None, 
            pos_hint={"x":0, "top":top_lbl_id}, height=75,
            background_normal="Rescources/darktransparent",
            background_color=rgba('#0a5e00'))

        btn_id.bind(on_press = partial(buildRuleView, rule))

        row.add_widget(btn_id)

        widget.add_widget(row)


################################################################################
# building the widget that holds the detailed view of a rule
################################################################################
def buildRuleView(rule, *args):
    main_layout = FloatLayout()

    header = Label(text=rule.getName(), pos_hint={'center_x':.5, 'top':1}, 
        size_hint=(.2,.1), font_size="30sp", bold=True, color = rgba('#0a5e00'))

    body = WrappedLabel(text=rule.getText(), font_size="20sp", 
        pos_hint={'center_x':.5,'center_y':.8}, size_hint=(.9,.9))

    main_layout.add_widget(header)
    main_layout.add_widget(body)

    rule_view = ModalView(size_hint = (.9,.9), background = "Resources/darktransparent", background_color=rgba('#0a5e00'))
    rule_view.add_widget(main_layout)
    rule_view.open()