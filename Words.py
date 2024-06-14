import json

# for one file exe
import os, sys
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class Words():
    def __init__(self) -> None:
        self.easy_words = json.load(open(resource_path('easy_words.json'), 'r'))
        self.medium_words = json.load(open(resource_path('medium_words.json'), 'r'))
        self.hard_words = json.load(open(resource_path('adv_words.json'), 'r'))
        self.syllable_easy_words = self.filter_syllable(self.easy_words)
        self.syllable_medium_words = self.filter_syllable(self.medium_words)
        self.syllable_hard_words = self.filter_syllable(self.hard_words)
        
        self.level = 'easy'

    def filter_syllable(self, dict) -> list:
        return [word for word in dict if dict[word]['syllable'].count(';') > 1]
    
    def get_words(self, level, syllable=False):
        self.level = level
        match level:
            case 'easy':
                if syllable:
                    return self.syllable_easy_words
                return list(self.easy_words.keys())
            case 'medium':
                if syllable:
                    return self.syllable_medium_words
                return list(self.medium_words.keys())
            case 'hard':
                if syllable:
                    return self.syllable_hard_words
                return list(self.hard_words.keys())
    
    def get_word(self, word) -> dict:
        match self.level:
            case 'easy':
                return self.easy_words[word]
            case 'medium':
                return self.medium_words[word]
            case 'hard':
                return self.hard_words[word]
        
