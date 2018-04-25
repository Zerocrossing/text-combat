"""
Actors represent entities who can be the subjects and targets of sentences
words are stored in a dict keyed by word objects, where value is the count (int or math.inf)
"""
from stats import *
import random
import math
from words import *
from verbs import *
from adjectives import *


class Actor:
    def __init__(self):
        # general attributes
        self.name = None
        # stats and combat attributes
        self.stats = Stats()
        self.health = 0
        self.stamina = 100
        # words and sentence attributes
        self.words = {}
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

    # region word and sentence methods

    def get_verbs(self, usable=False):
        """
        Returns a list of all the verb objects this actor has
        :param usable: If True will only return words with a count > 0
        :return: list of Verb objects
        """
        if not usable:
            return [word for word in self.words if isinstance(word, Verb)]
        else:
            return [word for word in self.words if isinstance(word, Verb) and self.words[word] > 0]

    def get_adjectives(self, usable=False):
        """
        Returns a list of all the verb objects this actor has
        :param usable: If True will only return words with a count > 0
        :return: list of Verb objects
        """
        if not usable:
            return [word for word in self.words if isinstance(word, Adjective)]
        else:
            return [word for word in self.words if isinstance(word, Adjective) and self.words[word] > 0]

    def get_word_by_name(self, word_name):
        """
        Checks if this actor has a word called word_name
        :param word_name: string name of a word
        :return: The word object if it exists, None if it does not
        """
        for word in self.words:
            if word.name == word_name:
                return word
        return None

    def add_word(self, word, count=1):
        """
        adds a word if it doesnt exist
        if the word does exist, increment it's value by 1
        :param word: word object or string name of word
        """
        # if a string is passed, check if the actor has the word, if not get it from the master word list
        if type(word) is str:
            word_obj = self.get_word_by_name(word)
            if word_obj is None:
                word_obj = Word.get_word_from_name(word)
                if word_obj is None:
                    raise Exception("Cannot find word in master word list", word)
            word = word_obj
        # word should now be a word type object, increment it if it's already in the word list, or add it if not
        if not isinstance(word, Word):
            raise Exception("Unable to add word", word)
        if word in self.words:
            self.words[word] += count
        else:
            if word.is_infinite:
                self.words[word] = math.inf
            else:
                self.words[word] = count

    def use_word(self, word):
        """
        Called whenever a word is used
        Decrements the value if the word is finite
        Removes the word if it is finite and decremented to 0 count
        Decreases the words freshness
        :param word: word object to use or name of word to search for word in actor's word list
        """
        # if a string is passed, check if the actor has the word
        if type(word) is str:
            word = self.get_word_by_name(word)
        if word not in self.words:
            raise Exception("Actor does not have word to use", word)
        if self.words[word] <= 0:
            raise Exception("Cannot use finite word with no uses", word)
        self.words[word] -= 1
        word.modify_freshness(self._freshness_loss)

    def remove_word(self, word):
        """
        Removes a word from the actor's list of words
        :param word:
        :return:
        """
        if type(word) is str:
            word = self.get_word_by_name(word)
        if word not in self.words:
            raise Exception("Actor does not have word to remove", word)
        del self.words[word]

    # endregion

    def take_turn(self):
        raise NotImplementedError

    def __str__(self):
        return self.name
