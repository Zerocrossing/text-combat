"""
Actors represent entities who can be the subjects and targets of sentences
verbs and adverbs:
    stored in a dictionary keyed off the word name
    the value is a list of size 2, the first element is the word object, the second the count of words available
"""
from stats import *


class Actor:
    def __init__(self):
        self.name = None
        self.stats = Stats()
        self.health = 0
        self.stamina = 100
        self.verbs = {}
        self.adjectives = {}
        self.next_sentence = None

    def take_damage(self, dmg):
        raise NotImplementedError

    def get_max_health(self):
        return self.stats.endurance * 10

    def take_turn(self):
        raise NotImplementedError

    def modify_stamina(self, value):
        value = round(value)
        self.stamina += value
        if self.stamina < 0:
            self.negative_stamina()

    def negative_stamina(self):
        # todo: temp implementation
        diff = abs(self.stamina)
        self.stamina = 0
        print(self.name + " overexerted themselves!")
        self.take_damage(diff)
        pass

    def is_dead(self):
        return self.health <= 0
