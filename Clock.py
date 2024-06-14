 
# The Clock object allows you to schedule
# a function call in the future; once or
# repeatedly at specified intervals.
from kivy.clock import Clock
from kivy.uix.label import Label
from typing import Callable

# Class that updates a countdown timer label with the given time
# calls the callback function when finished
class CountdownClock():
    def __init__(self, label: Label, countdowntime: int, callback: Callable = None, onlySeconds: bool = False):
        self.label = label
        self.countdowntime = countdowntime
        self.callback = callback
        self.onlySeconds = onlySeconds
    
    def start(self):
        self.update_label()
        Clock.schedule_interval(self.callback_clock_update, 1)
    
    def pause(self):
        Clock.unschedule(self.callback_clock_update)
 
    def callback_clock_update(self, dt):
        self.countdowntime = self.countdowntime - 1
        self.update_label()
        if self.countdowntime <= 0:
            self.callback_clock_finished()
            
    
    def update_label(self):
        if self.onlySeconds:
            self.label.text = str(self.countdowntime)
        else:
            self.label.text = "%d:%02d" % (self.countdowntime // 60, self.countdowntime % 60)

    def callback_clock_finished(self):
        Clock.unschedule(self.callback_clock_update)
        if self.callback is not None:
            self.callback()
 