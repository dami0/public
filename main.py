#!/usr/bin/python

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty
from getpass import getuser
from socket import gethostname
import JsonInfoReader, State, Outputer


class TitleBar(BoxLayout):

    def __init__(self, **kwargs):
        super(TitleBar, self).__init__(**kwargs)
        self.orientation = 'horizontal'


class Prompt(Label):

    def __init__(self, **kwargs):
        super(Prompt, self).__init__(**kwargs)
        self.text = getuser() + "@" + gethostname()


class SwitchScreen(BoxLayout):

    def __init__(self, **kwargs):
        super(SwitchScreen, self).__init__(**kwargs)
        self.orientation = 'horizontal'


class AccordionThing(Accordion):

    def __init__(self, **kwargs):
        super(AccordionThing, self).__init__(**kwargs)
        self.orientation = 'vertical'
        inst = JsonInfoReader.JsonInfoReader("info.json", None)
        cats = inst.listCategories()
        for cat in cats:
            item = AccordionItem(title='%s' % cat)
            box = BoxLayout(orientation = 'vertical')
            subs = inst.listInsideCategories(cat)
            for sub in subs:
                box.add_widget(Label(text="%s" % sub))
            item.add_widget(box)
            self.add_widget(item)

class ButtonBar(BoxLayout):

    def __init__(self, **kwargs):
        super(ButtonBar, self).__init__(**kwargs)
        self.orientation = 'horizontal'


class Splitter(Widget):
    pass


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
