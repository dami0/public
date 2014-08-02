#!/usr/bin/python

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.uix.popup import Popup

from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty, ObjectProperty
from getpass import getuser
from socket import gethostname
import JsonInfoReader, State, Outputer
import time
import os


file = JsonInfoReader.JsonInfoReader("info.json")
state = State.State()

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class TitleBar(BoxLayout):

    def __init__(self, **kwargs):
        super(TitleBar, self).__init__(**kwargs)
        self.orientation = 'horizontal'


class Prompt(Label):

    def __init__(self, **kwargs):
        super(Prompt, self).__init__(**kwargs)
        self.text = getuser() + "@" + gethostname()


class SwitchScreen(BoxLayout):
#    global file
#    inst = file
    accordion = ObjectProperty(None)
    infos = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(SwitchScreen, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.create()
#        self.scrollinfo.add_widget(InfoScreen(self.inst.listCategories()[0]))

    def viewitem(self, object, text):
        self.remove_widget(self.infos)
        self.infos = InfoScreen(text)
        self.add_widget(self.infos)

    def create(self):
        self.accordion.bind(selected=self.viewitem)


class InfoScreen(BoxLayout):

    def __init__(self, value = "", **kwargs):
        super(InfoScreen, self).__init__(**kwargs)
        if not value: return
        self.orientation = "vertical"
        width = self.width
        height = self.height

        self.add_widget(HeadInfo(value))

        global file
        inst = file
        inf = inst.getInfo(value)
        txts = TextInput(text = inf, background_color = (0.15, 0.15, 0.15, 1),
            foreground_color = (1, 1, 1, 1), multiline = True, readonly = True,
            size_hint = (1.0, None))
        txts.bind(minimum_height=txts.setter('height'))
        scroll = ScrollView(size_hint = (1, 1),
                size = (width, height))
        scroll.add_widget(txts)
        self.add_widget(scroll)
        self.add_widget(Label(text = "Comments", size_hint_y = 0.05))
        scroll2 = ScrollView(size_hint = (1, 0.2),
                size = (width, height))
        comments = TextInput(multiline=True, foreground_color = (1, 1, 1, 1), 
            size_hint = (1.0, None), background_color = (0.15, 0.15, 0.15))
        comments.bind(minimum_height=comments.setter('height'))
        if value in state.comments.keys():
            comments.text = state.comments[value]
        else: comments.text = "Put some text here, bruh."
        scroll2.add_widget(comments)
        self.add_widget(scroll2)
#        self.add_widget(comments)

        self.add_widget(ButtonBar())


class HeadInfo(Widget):
    header = ObjectProperty(None)

    def __init__(self, value, **kwargs):
        super(HeadInfo, self).__init__(**kwargs)
        self.header.text = value
#        self.add_widget(Label(text = value, font_size = "28sp",
#            size_hint_y = 0.05))
        


class AccordionThing(Accordion):
    selected = StringProperty("")

    def __init__(self, **kwargs):
        super(AccordionThing, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.draw()

    def switch(self, object):
        self.selected = object.text

    def draw(self):
        global file
        inst = file
        blades = []
        for cat in inst.listCategories():
            blades.append(AccordionItem(title = cat, font_size = "20sp"))
            box = BoxLayout(orientation = 'vertical')
            subs = inst.listInsideCategories(cat)
            for sub in subs:
                butt = Button(text = sub, background_color = [0.35, 0.35, 0.35,
                    1], font_size = "16sp")
                butt.bind(on_press = self.switch)
                box.add_widget(butt)
            blades[-1].add_widget(box)
            self.add_widget(blades[-1])
        blades[-1].collapse = True
        blades[0].collapse = False


class ButtonBar(BoxLayout):

    def __init__(self, **kwargs):
        super(ButtonBar, self).__init__(**kwargs)
        self.orientation = 'horizontal'

    def showImport(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content, size_hint=(0.9,
            0.9))
        self._popup.open()

    def load(self, path, filename):
        state.load(os.path.join(path,filename[0]))
        self.dismiss_popup()

    def dismiss_popup(self):
        self._popup.dismiss()


class MainScreen(BoxLayout):

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        titleb = TitleBar()
        switch = SwitchScreen()
        self.add_widget(titleb)
        self.add_widget(switch)


class RiceApp(App):

    def build(self):
        win = MainScreen()
        Window.clearcolor = (0.15, 0.15, 0.15, 1)
        return win


if __name__ == '__main__':
  RiceApp().run()
