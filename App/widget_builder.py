import kivy

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.utils import rgba
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout

from functools import partial

# see documentation
kivy.require("1.11.1")

#TODO: Create the memberscarousel in this class!

class WrappedLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.halign = "center"
        self.valign = "top"
        self.bind(
            width=lambda *x:
            self.setter('text_size')(self, (self.width, None)),
            texture_size=lambda *x: self.setter('height')(self, self.texture_size[1]))

################################################################################
# filling the scrollview
# @param rules the whole rules array
# @param widget the gridlayout that will be updated/build
################################################################################
def buildRules(rules, widget):
    #starting position
    top_lbl_id = .8

    for rule in rules:
        #spacing in between rows
        top_lbl_id -= 1.2

        row = FloatLayout(size_hint_y=None, height=50)
        lbl_id = Label(text = str(rule.getId()), font_size = "20sp",
            size_hint_y = None, pos_hint = {"center_x":.1, "top":top_lbl_id},
            height = 100, color = rgba('#0a5e00'))

        lbl_name = Label(text = rule.getName(), font_size = "20sp",
            size_hint_y = None, size_hint_x = .6, 
            pos_hint = {"x":.2, "top":top_lbl_id},
            height = 100, halign = "left")

        btn = Button(text = "", size_hint_y=None, 
            pos_hint={"x":0, "top":top_lbl_id}, height=100,
            background_normal="",
            background_color=rgba('#262626'))

        btn.bind(on_press = partial(buildRuleView, rule))

        row.add_widget(btn)
        row.add_widget(lbl_id)
        row.add_widget(lbl_name)

        widget.add_widget(row)


################################################################################
# building the widget that holds the detailed view of a rule
# @param rule, the specific rule that is displayed in this view
################################################################################
def buildRuleView(rule, *args):
    main_layout = FloatLayout()

    header = Label(text=rule.getName(), pos_hint={'center_x':.5, 'top':1}, 
        size_hint=(.2,.1), font_size="30sp", bold=True, color = rgba('#0a5e00'))

    body = WrappedLabel(text=rule.getText(), font_size="20sp", 
        pos_hint={'center_x':.5,'center_y':.5}, size_hint=(.9,.9))

    main_layout.add_widget(header)
    main_layout.add_widget(body)

    rule_view = ModalView(size_hint = (.9,.95), background = "Resources/262626.png", background_color=rgba('#0a5e00'))
    rule_view.add_widget(main_layout)
    rule_view.open()

################################################################################
# building each page of carousel that will be later added
# @param carousel the carousel that will be filled
# @param members the members array
# @param instance whole instance of the .py file where the according methods sit
# @return the newly build widget
################################################################################
def buildMembersCarousel(carousel, members, instance):
        #checking if there are members in the array, if not creating a 
        #page showing that there are no members detected
        if len(members) == 0:
            no_members_label = Label(text="No members found", font_size='30sp')
            carousel.add_widget(no_members_label)
            return carousel

        else:
            loop_counter = 0
            for member in members:
                #creating the layout that holds all the fields
                layout = FloatLayout()

                person_image = Image(source=member.getNextPicture(), 
                    allow_stretch=True, 
                    pos_hint={'x':.2, 'top':.99}, size_hint=(.6,.3))

                btn_next_picture = Button(background_normal='', 
                    background_color=rgba(0,0,0,0), 
                    pos_hint={'x':.2, 'top':.99}, size_hint=(.6,.3))

                btn_next_picture.bind(
                    on_press=partial(instance.nextPictureCallback, 
                    loop_counter, person_image))

                layout_names = BoxLayout(orientation='horizontal', 
                    pos_hint={'x':.1, 'y':.6}, size_hint=(.8,.1))
                lbl_names = Label(text=member.getName(1) + " " + '[i]' + 
                    member.getName(2) + '[/i]' + " " + member.getName(3), 
                    markup=True, font_size='20sp')
                layout_names.add_widget(lbl_names)

                btn_statement = Button(text=member.getNextStatement(), 
                    font_size='15sp', background_normal='', 
                    background_color=rgba(0,0,0,0),
                    pos_hint={'x':.1, 'y':.2}, size_hint=(.8,.4))

                btn_statement.bind(
                    on_press=partial(instance.nextStatementCallback, 
                    loop_counter, btn_statement))

                lbl_birthday = Label(text=member.getBirthday(), 
                    font_size='15sp', pos_hint={'x':.2, 'bottom':1}, 
                    size_hint=(.6,.1))

                #adding a vertical row of buttons to quickly navigate to 
                # specific members
                layout_scroller = BoxLayout(orientation='vertical', 
                    pos_hint={'right':1, 'bottom':1}, size_hint=(.1,1))

                #using a counter var for the position of the members in 
                # their array
                count = 0

                #looping through the members and creating a button for each one
                for member_btn in members:
                    #if we are on the specific slide of a member the specific 
                    # button should be colored accordingly
                    if member.getName(1) == member_btn.getName(1):
                        tmp_button = Button(text=member_btn.getName(1), 
                            id='btnJump' + member_btn.getName(1), 
                            font_size='5sp', background_color=rgba(0,0,0,0))
                    else:
                        tmp_button = Button(text=member_btn.getName(1), 
                            id='btnJump' + member_btn.getName(1), 
                            font_size='5sp', background_normal = '', 
                            background_color=rgba('0F0F0F'))

                    tmp_button.bind(
                        on_press=partial(instance.jumpToMember, count))
                    layout_scroller.add_widget(tmp_button)
                    count = count + 1
                
                layout.add_widget(layout_scroller)
                layout.add_widget(lbl_birthday)
                layout.add_widget(btn_statement)
                layout.add_widget(person_image)
                layout.add_widget(layout_names)
                layout.add_widget(btn_next_picture)

                carousel.add_widget(layout)

                loop_counter = loop_counter + 1

            return carousel