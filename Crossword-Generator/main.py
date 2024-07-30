import random
from modules.conversion import time_convert
import time
import csv
from modules.letter_link import letter_link
from modules.word_select import word_select
from modules.first_time_setup import first_time_setup, on_start
from modules.updatefile import stattrack
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from functools import partial

on_start()


class HomePage(Screen):
    settingsbtn = ListProperty()
    Window.clearcolor = (1, 1, 1, 1)
    title_text = ObjectProperty()


monkeys = ['*', '*', '*', 'a', 'p', 'e', '*', '*', '*']


class CrosswordPage(Screen):
    text_input = ObjectProperty()
    image_widget = ObjectProperty()
    monkey_widget = ObjectProperty()
    label1 = ObjectProperty()
    my_buttons = ListProperty()
    downclues = ListProperty()
    my_downs = ListProperty()
    acrossclues = ListProperty()
    my_across = ListProperty()
    cwordbox = ListProperty()
    cwordenter = ObjectProperty()
    timestart = ObjectProperty()
    lastSelected = ListProperty([-1, -1, "no"])
    crossword = ListProperty()
    directionsdown = ListProperty()
    directionsacross = ListProperty()

    def highlight(self, *largs):

        if self.lastSelected[2] == "down":
            for m in range(self.lastSelected[1]):
                self.my_buttons[self.lastSelected[0] + 30 * m].background_color = \
                    self.manager.get_screen("settings").palette[3]
                self.my_buttons[self.lastSelected[0] + 30 * m].color = self.manager.get_screen("settings").palette[4]
        if self.lastSelected[2] == "across":
            for m in range(self.lastSelected[1]):
                self.my_buttons[self.lastSelected[0] + m].background_color = \
                    self.manager.get_screen("settings").palette[3]
                self.my_buttons[self.lastSelected[0] + m].color = self.manager.get_screen("settings").palette[4]
        if largs[0][2] == "down":
            for l in range(largs[0][1]):
                self.my_buttons[largs[0][0] + 30 * l].background_color = self.manager.get_screen("settings").palette[2]
                self.my_buttons[largs[0][0] + 30 * l].color = self.manager.get_screen("settings").palette[5]
        if largs[0][2] == "across":
            for l in range(largs[0][1]):
                self.my_buttons[largs[0][0] + l].background_color = self.manager.get_screen("settings").palette[2]
                self.my_buttons[largs[0][0] + l].color = self.manager.get_screen("settings").palette[5]
        self.text_input.text = ""
        self.lastSelected = [largs[0][0], largs[0][1], largs[0][2]]

    def on_pre_enter(self, *largs):
        self.lastSelected = [-1, -1, "no"]
        self.ids.thegrid.clear_widgets(children=None)
        self.ids.downclues.clear_widgets(children=None)
        self.ids.acrossclues.clear_widgets(children=None)
        self.my_buttons = []
        for i in range(900):
            p1 = (i // 30)
            p2 = i % 30
            btn = Button(text=str(self.crossword[p1][p2]))
            if str(self.crossword[p1][p2]) != "*":
                btn = Button(text="", background_color=self.manager.get_screen("settings").palette[3],
                             color=self.manager.get_screen("settings").palette[4])

            self.ids.thegrid.add_widget(btn)

            self.my_buttons.append(btn)
            if str(self.crossword[p1][p2]) == "*":
                self.my_buttons[i].background_color = 0, 0, 0, 1

        for k in range(0, len(self.directionsdown)):
            btn = Button(text=str(k + 1) + ":    " + self.directionsdown[k][3],
                         background_color=self.manager.get_screen("settings").palette[1],
                         color=self.manager.get_screen("settings").palette[4])
            btn.bind(on_press=partial(self.highlight, self.directionsdown[k]))
            self.ids.downclues.add_widget(btn)
            self.my_downs.append(btn)
        for k in range(0, len(self.directionsacross)):
            btn = Button(text=str(k + 1) + ":    " + self.directionsacross[k][3],
                         background_color=self.manager.get_screen("settings").palette[1],
                         color=self.manager.get_screen("settings").palette[4])
            btn.bind(on_press=partial(self.highlight, self.directionsacross[k]))
            self.ids.acrossclues.add_widget(btn)
            self.my_across.append(btn)

        self.timestart = time.time()

    def grid(self):
        for i in range(0, 3):
            self.my_buttons[i].text = (self.text_input.text)[i]

    def color_change(self):

        self.text_input.background_color = (1, 0, 1, 1)

    def crossword_append(self):
        if len(self.text_input.text) == (self.lastSelected[1]) and self.text_input.text.isalpha():
            if self.lastSelected[2] == "across":
                for j in range(self.lastSelected[1]):
                    self.my_buttons[self.lastSelected[0] + j].text = self.text_input.text[j]
            if self.lastSelected[2] == "down":
                for j in range(self.lastSelected[1]):
                    self.my_buttons[self.lastSelected[0] + 30 * j].text = self.text_input.text[j]

    def verify(self):
        success = True
        for i in range(len(self.directionsdown)):
            length = self.directionsdown[i][1]
            pos = self.directionsdown[i][0]

            for j in range(int(length)):

                if self.my_buttons[int(pos) + 30 * j].text != self.crossword[(int(pos)) // 30 + j][((int(pos)) % 30)]:
                    success = False

        for i in range(len(self.directionsacross)):
            length = self.directionsacross[i][1]
            pos = self.directionsacross[i][0]

            for j in range(int(length)):
                if self.my_buttons[int(pos) + j].text != self.crossword[(int(pos)) // 30][(int(pos)) % 30 + j]:
                    success = False

        if success:
            self.my_buttons.color = 0, 1, 1, 1
            App.get_running_app().root.current = "victory"  # stattrack and winning screen

    def givehint(self):
        if random.randint(0, 1) == 0:

            i = random.randint(0, len(self.directionsdown) - 1)
            length = self.directionsdown[i][1]
            pos = self.directionsdown[i][0]

            j = random.randint(0, int(length))

            self.my_buttons[int(pos) + 30 * j].text = self.crossword[(int(pos)) // 30 + j][((int(pos)) % 30)]

        else:
            i = random.randint(0, len(self.directionsacross) - 1)
            length = self.directionsacross[i][1]
            pos = self.directionsacross[i][0]

            j = random.randint(0, int(length))

            self.my_buttons[int(pos) + j].text = self.crossword[(int(pos)) // 30][(int(pos)) % 30 + j]


class DifficultySelect(Screen):
    difficulty = ObjectProperty()

    def wordGen(self, *largs):
        extreme = False
        with open("scores.csv", 'r', newline='') as csvfile:
            for line in csv.reader(csvfile.readlines()):
                if line[0] == "Hard Completions":
                    if int(line[1]) > 1:
                        extreme = True

        self.difficulty = largs[0]
        words = word_select(*largs)

        self.manager.get_screen("cword").crossword, self.manager.get_screen(
            "cword").directionsdown, self.manager.get_screen("cword").directionsacross = letter_link(words)


class WindowManager(ScreenManager):
    pass


class RecordsPage(Screen):
    individual = ListProperty()
    cumulative = ListProperty()

    def on_pre_enter(self, *args):
        stats = []
        with open('scores.csv', newline='') as csvfile:
            reader = (csv.reader(csvfile.readlines()))
            for line in reader:

                if line[1] == "-1":
                    line[1] = "N/A"
                else:
                    if line[0] in (
                            "Total Time", "Average Time", "Fastest Easy", "Fastest Medium", "Fastest Hard",
                            "Fastest Extreme"):
                        line[1] = str(time_convert(int(line[1])))

                stats.append(line)
        for i in range(0, 5):
            self.ids.cumulative.children[4 - i].text = stats[i][0] + ":  " + stats[i][1]
        for i in range(0, 8):
            self.ids.individual.children[7 - i].text = stats[5 + i][0] + ":  " + stats[5 + i][1]

    def reset_data(self):
        first_time_setup()


class SettingsPage(Screen):
    misc = ObjectProperty()
    tutorial = ObjectProperty()
    settingsreturn = ObjectProperty()
    settingsbox2 = ListProperty()
    default = ListProperty(
        [(1, 1, 1, 1), (153 / 255, 255 / 255, 255 / 255, 1), (255 / 255, 102 / 255, 255 / 255, 1), (1, 1, 1, 1),
         (0, 0, 0, 1), (0, 0, 0, 1)])  # default, constant
    colourblind = ListProperty(
        [(1, 1, 1, 1), (.85, .85, .85, 1), (.5, .5, 0, 1), (1, 1, 1, 1), (0, 0, 0, 1), (0, 0, 0, 1)])
    dark = ListProperty(
        [(31 / 255, 41 / 255, 51 / 255, 1), (50 / 255, 63 / 255, 75 / 255, 1), (252 / 255, 207 / 255, 250 / 255, 1),
         (82 / 255, 96 / 255, 109 / 255, 1), (1, 1, 1, 1), (0, 0, 0, 1)])  # dark mode, constant
    highcontrast = ListProperty(
        [(0, 0, 0, 1), (0, 255 / 255, 255 / 255, 1), (0, 0, 255 / 255, 1), (255 / 255, 255 / 255, 0, 1), (0, 0, 0, 1),
         (1, 1, 1, 1)])
    palette = ListProperty(
        [(1, 1, 1, 1), (153 / 255, 255 / 255, 255 / 255, 1), (255 / 255, 102 / 255, 255 / 255, 1), (1, 1, 1, 1),
         (0, 0, 0, 1), (0, 0, 0, 1)])  # colour variable
    font = ObjectProperty("comic")

    # colour_bg = palette[0]
    # colour_widget = palette[1]
    # colour_highlight = palette[2]
    # colour_grid = palette[3]
    # colour_text = palette[4]
    # highlight_text = palette[5]

    def colour_update(self):

        for i in self.manager.get_screen("home").ids.homefloat.children:
            i.background_color = self.palette[1]  # widget
            i.color = self.palette[4]  # text
            i.font_name = self.font  # font
        for i in self.manager.get_screen("difficulty").ids.difficultyfloat.children:
            i.background_color = self.palette[1]  # widget
            i.color = self.palette[4]  # text
            i.font_name = self.font
        for i in self.manager.get_screen("cword").ids.cwordbox.children:
            i.background_color = self.palette[1]  # widget
            i.color = self.palette[4]  # text
            i.font_name = self.font
        self.manager.get_screen("cword").ids.cwordenter.background_color = self.palette[1]
        for i in self.manager.get_screen("record").ids.recordsbox.children:
            i.background_color = self.palette[1]  # widget
            i.color = self.palette[4]  # text
            i.font_name = self.font
        for i in self.manager.get_screen("record").ids.cumulative.children:
            i.color = self.palette[4]
        for i in self.manager.get_screen("record").ids.individual.children:
            i.color = self.palette[4]

        self.manager.get_screen("victory").ids.victorytext.color = self.palette[4]
        self.manager.get_screen("victory").ids.victoryreturn.color = self.palette[4]
        self.manager.get_screen("victory").ids.victoryreturn.background_color = self.palette[1]

        for i in self.ids.settingsbox1.children:
            i.background_color = self.palette[1]  # widget
            i.color = self.palette[4]  # text
            i.font_name = self.font
        for i in self.ids.settingsbox2.children:
            i.background_color = self.palette[1]  # widget
            i.color = self.palette[4]  # text
            i.font_name = self.font
        self.ids.settingsreturn.background_color = self.palette[1]

        self.ids.settingsreturn.color = self.palette[4]
        self.ids.settingsreturn.font_name = self.font
        self.ids.tutorial.background_color = self.palette[1]
        self.ids.tutorial.color = self.palette[4]
        self.ids.misc.color = self.palette[4]
        self.ids.misc.font_name = self.font
        Window.clearcolor = self.palette[0]  # bg

    def colour_change(self, *largs):

        if largs[0] == "dark":
            self.palette = self.dark
        if largs[0] == "default":
            self.palette = self.default
        if largs[0] == "highcontrast":
            self.palette = self.highcontrast
        if largs[0] == "colourblind":
            self.palette = self.colourblind

        # colour_bg = palette[0]
        # colour_widget = palette[1]
        # colour_highlight = palette[2]
        # colour_grid = palette[3]
        # colour_text = palette[4]

    def font_change(self):
        if self.font == "comic":
            self.font = "arial"
        else:
            self.font = "comic"

    def tutorial(self):  # tutorial popup
        box = BoxLayout(orientation="vertical")
        box.add_widget(Label(text="Thank you for using W-ord, the digital crossword generating software.\n\n\n"
                                  "To get started go to difficulty select and select a difficulty. After generated your crossword will be shown on screen.\n\n"
                                  "From here you have the crossword on the left, down and across clues on the right and below that a text box for you to input your answers.\n\n"
                                  "Each clue highlights on the board when clicked. If you type in a word of the same length as the clue it will appear on the grid.\n\n"
                                  "If you're stuck, press the hint button to randomly fill in one spot. Press verify to see if your grid is complete. If it is you will be directed to the victory screen.\n\n"
                                  "To see your performance stats.\n\n"
                                  "If you want to see your lifetime results, head over to the records page.\n\n"
                                  "To change skin or any accessibility options head over to settings and press any buttons you want.",
                             color=(1, 1, 1, 1)
                             ))
        btn1 = Button(text="Return", size_hint=(1, 0.1), background_color=(0, 0, 0, 1), color=(1, 1, 1, 1))
        box.add_widget(btn1)
        popup = Popup(title="Tutorial", content=box)
        btn1.bind(on_press=popup.dismiss)
        popup.open()


class VictoryPage(Screen):
    stats = ListProperty()
    gamerd = ListProperty()

    def homereturn(self, *largs):
        App.get_running_app().root.current = "home"

    def on_pre_enter(self, *args):
        self.ids.stats.clear_widgets()
        timeelapsed = time.time() - self.manager.get_screen("cword").timestart
        timed = Button(text=("Time taken:   " + str(time_convert(int(timeelapsed)))),
                       background_color=self.manager.get_screen("settings").palette[1],
                       color=self.manager.get_screen("settings").palette[4])
        self.ids.stats.add_widget(timed)
        wordsanswered = len(self.manager.get_screen("cword").directionsdown) + len(
            self.manager.get_screen("cword").directionsacross)
        lettersanswered = 0
        for i in self.manager.get_screen("cword").directionsdown:
            lettersanswered = lettersanswered + i[1]
        for i in self.manager.get_screen("cword").directionsacross:
            lettersanswered = lettersanswered + i[1]

        self.ids.stats.add_widget(Button(text="Words answered:  " + str(wordsanswered),
                                         background_color=self.manager.get_screen("settings").palette[1],
                                         color=self.manager.get_screen("settings").palette[4]))
        self.ids.stats.add_widget(Button(text="Letters answered:    " + str(lettersanswered),
                                         background_color=self.manager.get_screen("settings").palette[1],
                                         color=self.manager.get_screen("settings").palette[4]))
        stattrack(self.manager.get_screen("difficulty").difficulty, timeelapsed, wordsanswered, lettersanswered)


kv = Builder.load_file("my.kv")


class MyApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    MyApp().run()
