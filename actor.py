"""
Actors represent entities who can be the subjects and targets of sentences
verbs and adverbs:
    stored in a dictionary keyed off the word name
    the value is a list of size 2, the first element is the word object, the second the count of words available
    if the word is infinite count is a meaningless number
"""
from stats import *
from words import *
import random


class Actor:
    def __init__(self):
        # general attributes
        self.name = None
        # stats and combat attributes
        self.stats = Stats()
        self.health = 0
        self.stamina = 100
        # words and sentence attributes
        self.verbs = {}
        self.adjectives = {}
        self.next_sentence = None
        # constants and privates
        self._freshness_loss = 0.25

    # region Stat and Stat-Based Getters
    def get_max_health(self):
        return self.stats.endurance * 10

    def get_initiative(self):
        """
        initiate determines a character's order in combat
        1-5 per 2 points of cunning
        :return: initiative value as int
        """
        return (self.cunning / 2) * random.randint(1, 5)

    def is_dead(self):
        return self.health <= 0

    # endregion

    # region Stat and stat-based setters

    def modify_stat(self, stat, value):
        """
        Modifies stats, permanently or temporarily
        Recalculates values when appropriate
        :param stat: name of the stat (string)
        :param value: value to modify the stat by (positive or negative)
        :return: new value of stat if successful, None if not possible or blocked
        """
        raise NotImplementedError

    def modify_stamina(self, value):
        """
        Lowers stamina by the passed amount
        """
        value = round(value)
        self.stamina += value
        if self.stamina < 0:
            self.negative_stamina()

    def negative_stamina(self):
        """
        Called when stamina is reduced below 0
        Sets stamina to 0 and causes the actor to take 1 damage per negative point
        """
        diff = abs(self.stamina)
        self.stamina = 0
        print(self.name + " was exhausted!")
        self.take_damage(diff)
        pass

    def take_damage(self, dmg):
        # todo: find a way to have effects proc on dmg, eg a stoneskin effect
        value = round(dmg)
        print("{} took {} damage.".format(self.name, value))
        self.health -= value

    # endregion

    def take_turn(self):
        raise NotImplementedError

    # region word and sentence methods

    def add_word(self, word_name):
        """
        adds a word if it doesnt exist
        if the word does exist, increment it's value by 1
        :param word_name: name of the word (will also accept word object directly)
        :return:
        """
        # if word_name is a word object, get it's name
        if type(word_name) is not str:
            word_name = word_name.name
        # check if the word already exists in verbs or adjectives
        if word_name in self.verbs:
            self.verbs[word_name][1] += 1
        elif word_name in self.adjectives:
            self.adjectives[word_name][1] += 1
        # add word if it doesn't exist
        else:
            word_obj = Word.get_word_from_name(word_name)
            if word_obj is None:
                raise Exception("Word not found")
            if isinstance(word_obj, Verb):
                self.verbs[word_obj.name] = [word_obj, 1]
            elif isinstance(word_obj, Adjective):
                self.adjectives[word_obj.name] = [word_obj, 1]
            else:
                raise Exception("Attempting to add a word of an unknown type", type(word_obj))

    def use_word(self, word_name):
        """
        Called whenever a word is used
        Decrements the value if the word is finite
        Decreases the words freshness
        :param word_name: string name of word or reference to object/type
        :return: None
        """
        # make sure word_name is a string to key the dict
        if type(word_name) is not str:
            word_name = word_name.name
        # get reference to the object from the lists
        word_obj = None
        word_dict = None
        if word_name in self.verbs:
            word_obj = self.verbs[word_name][0]
            word_dict = self.verbs
        elif word_name in self.adjectives:
            word_obj = self.adjectives[word_name][0]
            word_dict = self.adjectives
        if word_obj is None or word_dict is None:
            raise Exception("Word not found")
        # decrement count if object isn't infinite, remove obj if count is 0
        if not word_obj.is_infinite:
            word_dict[word_name][1] -= 1
            if word_dict[word_name][1] == 0:
                self.remove_word(word_name)
        word_obj.modify_freshness(-self._freshness_loss)

    def remove_word(self, word_name):
        raise NotImplementedError

    # endregion
