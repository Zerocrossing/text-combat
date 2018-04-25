"""
Actors represent entities who can be the subjects and targets of sentences
verbs and adverbs:
    stored in a dictionary keyed off the word object
    the value of the dict is -1 if the word is infinite, otherwise it is the number of uses remaining
"""
from stats import *
from words import *
from verbs import *
from adjectives import *
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
        self._freshness_loss = -0.25

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

    def get_word_by_name(self, word_name):
        """
        Checks if this actor has a word called word_name
        :param word_name: string name of a word
        :return: The word object if it exists, None if it does not
        """
        for word in self.verbs.keys():
            if word.name == word_name:
                return word
        for word in self.adjectives.keys():
            if word.name == word_name:
                return word
        return None

    def add_word(self, word):
        """
        adds a word if it doesnt exist
        if the word does exist, increment it's value by 1
        :param word: word object or string name of word
        """
        # if a string is passed, check if the actor has the word, if not get it from the master word list
        if type(word) is str:
            new_word = self.get_word_by_name(word)
            if new_word is None:
                new_word = Word.get_word_from_name(word)
                if new_word is None:
                    raise Exception("Cannot find word to add to actor", word)
            word = new_word
        # get reference to dictionary based on type of word
        word_dict = None
        if isinstance(word, Verb):
            word_dict = self.verbs
        elif isinstance(word, Adjective):
            word_dict = self.adjectives
        else:
            raise Exception("Attempting to add word of unknown type", word)
        # if player already has the word, increment (if it's not infinite)
        if word in self.verbs or word in self.adjectives:
            if not word.is_infinite:
                word_dict[word] += 1
        # otherwise add the word to the dictionary
        else:
            if word.is_infinite:
                word_dict[word] = -1
            else:
                word_dict[word] = 1

    def use_word(self, word):
        """
        Called whenever a word is used
        Decrements the value if the word is finite
        Removes the word if it is finite and decremented to 0 count
        Decreases the words freshness
        :param word: word object to use or name of word
        """
        # if a string is passed, check if the actor has the word
        if type(word) is str:
            word = self.get_word_by_name(word)
            if word is None:
                raise Exception("Actor does not have word to use", word)
        # get reference to dictionary based on type of word
        word_dict = None
        if isinstance(word, Verb):
            word_dict = self.verbs
        elif isinstance(word, Adjective):
            word_dict = self.adjectives
        else:
            raise Exception("Attempting to use word of unknown type", word)
        if word not in word_dict:
            raise Exception("Actor does not have word to use", word)
        # if word is finite, decrement count and remove word if count is 0
        if not word.is_infinite:
            word_dict[word] -= 1
            if word_dict[word] == 0:
                self.remove_word(word)
        word.modify_freshness(self._freshness_loss)

    def remove_word(self, word):
        """
        Removes a word from the actor's list of words
        :param word:
        :return:
        """
        if type(word) is str:
            word = self.get_word_by_name(word)
            if word is None:
                raise Exception("Actor does not have word to use", word)

    # endregion
