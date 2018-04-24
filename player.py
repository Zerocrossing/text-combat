"""
Main Module for the Player
verbs and adverbs:
    stored in a dictionary keyed off the word name
    the value is a list of size 2, the first element is the word object, the second the count of words available

"""

from stats import Stats
from verbs import Verb
from adjectives import Adjective


class Player:
    def __init__(self):
        self.name = None
        self.stats = Stats()
        self.health = 0
        self.stamina = 100
        self.verbs = {}
        self.adjectives = {}
        self.next_sentence = None

    # region Stat-based Getters
    def get_max_health(self):
        return self.stats.endurance * 10

    def get_initiative(self):
        return self.stats.cunning

    # endregion

    # region Attribute Setters

    def take_damage(self, value):
        # todo: find a way to have effects proc on dmg, eg a stoneskin effect
        value = round(value)
        print("{} took {} damage.".format(self.name,value))
        self.health -= value

    def modify_stamina(self, value):
        value = round(value)
        self.stamina += value
        if self.stamina < 0:
            self.negative_stamina()

    def negative_stamina(self):
        # todo: temp implementation
        diff = abs(self.stamina)
        self.stamina = 0
        print("You have overexerted yourself!")
        self.take_damage(diff)
        pass

    def is_dead(self):
        return self.health <= 0

    # endregion

    # region Sentence Methods

    def add_word(self, word, count=1):
        """
        adds a word to the appropriate dictionary for it's class type
        Returns true if word was successfully added
        :word: object of word type (verb, adverb ect.)
        """
        if isinstance(word, Verb):
            self.add_verb(word, count)
            return True
        if isinstance(word, Adjective):
            self.add_adverb(word, count)
            return True
        return False

    def decrement_word(self, word, count=1):
        """
        When a word is "used" it's count is decremented
        The word is removed from the dictionary if it's uses are depleted
        :param word:
        :return:
        """
        raise NotImplementedError

    def remove_word(self, word):
        """
        Removes a word entirely from it's dict, regardless of count remaining
        :param word:
        :return:
        """
        raise NotImplementedError

    def add_verb(self, word, count=1):
        """
        if the verb already exists, add 1 to the count
        if the verb doesn't exist, add it with count 1
        """
        name = word.name
        if name in self.verbs.keys():
            self.verbs[name][1] += count
        else:
            self.verbs[name] = [word, count]

    def add_adverb(self, word, count=1):
        """
        if the adverb already exists, add 1 to the count
        if the adverb doesn't exist, add it with count 1
        """
        name = word.name
        if name in self.adjectives.keys():
            self.adjectives[name][1] += count
        else:
            self.adjectives[name] = [word, count]

    # endregion

    # region Combat Methods

    def take_turn(self):
        raise NotImplementedError

    # endregion

    def __str__(self):
        if self.name is None:
            return "Nameless One"
        return self.name
