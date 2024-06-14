import kivy

# kivy.require('2.1.0') # replace with your current kivy version !

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock as KivyClock

import random
import copy
import time

from Clock import CountdownClock

from Words import Words

GAME_TITLE = "Unscramword"


class GameScreen(Screen):
    score = NumericProperty(0)
    timer_countdown_label = ObjectProperty()
    mixed_letters_label = ObjectProperty()
    word_definition_label = ObjectProperty()
    word_input = ObjectProperty()
    submit_button = ObjectProperty()
    history_list = ObjectProperty()

    def __init__(self, difficulty="easy", leveltype="letter", gametime=120, **kwargs):
        super(GameScreen, self).__init__(**kwargs)

        self.difficulty = difficulty
        self.leveltype = leveltype
        self.gametime = gametime

        self.current_state = "before_game"

        self.game_words = Words()
        self.wordlist = copy.copy(
            self.game_words.get_words(difficulty, leveltype == "syllable")
        )
        self.current_word = ""

    def before_game(self):
        self.clock = CountdownClock(
            self.mixed_letters_label, 5, self.start_game, onlySeconds=True
        )
        self.clock.start()

    def start_game(self):
        self.current_state = "in_game"
        self.clock = CountdownClock(
            self.timer_countdown_label, self.gametime, self.finish_game
        )
        self.clock.start()
        self.choose_word()

    def finish_game(self):
        self.timer_countdown_label.text = "Time is up!"
        self.word_input.disabled = True
        time.sleep(1)
        self.manager.switch_to(
            ScoreScreen(self.difficulty, self.leveltype, self.gametime, self.score),
            direction="up",
        )

    def choose_word(self):
        if self.current_state != "in_game":
            return
        # choose a word from the list
        word = random.choice(self.wordlist)
        # ensure no same words
        self.wordlist.remove(word)
        # save current word
        self.current_word = word
        # shuffle presentation
        scrambled, definition = self.shuffle_word(word)
        # update label
        self.mixed_letters_label.text = scrambled
        self.word_definition_label.text = definition
        # focus on input
        KivyClock.schedule_once(self.focus_textbox, 0.1)

    def focus_textbox(self, _):
        self.word_input.focus = True

    def shuffle_word(self, word):
        wordinfo = self.game_words.get_word(word)
        match self.leveltype:
            case "letter":
                return (
                    " · ".join(random.sample(word, len(word))),
                    wordinfo["definition"],
                )
            case "syllable":
                shuffled = random.sample(
                    wordinfo["syllable"].split(";"),
                    len(wordinfo["syllable"].split(";")),
                )
                # avoid same order as presented
                if shuffled == wordinfo["syllable"].split(";"):
                    shuffled = [
                        shuffled[-1],
                        *random.sample(
                            wordinfo["syllable"].split(";")[:-1],
                            len(wordinfo["syllable"].split(";")) - 1,
                        ),
                    ]
                return (" · ".join(shuffled), wordinfo["definition"])

    def check_word(self, input_widget: TextInput, show_answer=False):
        if show_answer:
            result = {"text": f"Skipped: {self.current_word}", "color": "orange"}
        else:
            if not input_widget.text.strip():
                # do not parse empty string
                return

            word_correct = input_widget.text.strip() == self.current_word
            # prepare item in history list
            result = {
                "text": input_widget.text
                + (f" ({self.current_word})" if not word_correct else ""),
                "color": "green" if word_correct else "red",
            }

            # update score
            if word_correct:
                self.score += 1

        # add word to history list
        self.history_list.insert_data(result)

        # move to next word
        self.choose_word()

        # reset the input widget
        input_widget.text = ""


class ScoreScreen(Screen):
    score = NumericProperty(0)

    def __init__(self, difficulty, leveltype, gametime, score, **kwargs):
        super(ScoreScreen, self).__init__(**kwargs)
        self.difficulty = difficulty
        self.leveltype = leveltype
        self.gametime = gametime
        self.score = score


# list showing all the words that have been input
class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = []

    def insert_data(self, res):
        self.data.insert(0, res)
        self.refresh_from_data()


class MainScreen(Screen):
    pass


class game(App):
    def build(self):
        self.title = GAME_TITLE

    def on_start(self):
        self.screen_manager = self.root.ids["screen_manager"]

    def start_game(self, difficulty, leveltype, gametime):
        gameScreen = GameScreen(
            difficulty,
            leveltype,
            gametime,
            name="game_screen_" + difficulty + "_" + leveltype,
        )
        self.screen_manager.add_widget(gameScreen)
        self.screen_manager.switch_to(gameScreen, direction="left")
        self.root.ids["level_label"].text = (
            f"{difficulty.capitalize()} - {leveltype.capitalize()}"
        )
        gameScreen.before_game()

    def back_to_main(self):
        self.screen_manager.switch_to(MainScreen(name="main_screen"), direction="right")
        self.root.ids["level_label"].text = GAME_TITLE


if __name__ == "__main__":
    game().run()
