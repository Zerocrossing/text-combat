"""
Module for all word based mechanics
"""


class Word:
    """
    Abstract class to represent all words
    Words are used in encounter scenarios to construct sentences which represent actor actions
    """

    def __init__(self):
        self.freshness = 1.0
        self.tags = []
        self.is_infinite = True
        self.is_universal = False
        self.description = None

    @staticmethod
    def works_with(word1, word2):
        """
        checks if two words share a similar tag
        :return: True if words are compatible, false otherwise
        """
        if word1.is_universal or word2.is_universal:
            return True
        for tag1 in word1.tags:
            for tag2 in word2.tags:
                if tag1 == tag2:
                    return True
        return False

    def setup(self, subject, target=None, other_word=None):
        """
        setup is run before damage and effects are assigned
        damage reduction, blocks, and checks can be done here
        it is not required and can be passed
        """
        raise NotImplementedError

    def execute(self, subject, target=None, other_word=None):
        """
        execute assigns damage and effects after setup is run
        it is not required and can be passed
        """
        raise NotImplementedError


class Verb(Word):
    """
    Abstract implementation of a Verb
    Verbs represent actions an actor can perform
    Verbs have tags representing attributes
    These attributes modify the verb's performance in some way
    Verb execution is broken into 2 phases, setup and execute
    Setup is performed before actions are executed, and allows for things like blocking incoming damage
    Execute performs the action
    attributes:
        freshness:      a metric that modifies power and decreases with each usage of the word
        tags:           a list of keywords used to associate adverbs and verbs
        is_infinite:    bool that sets if the word has finite usage
    """

    def setup(self, subject, target=None, other_word=None):
        raise NotImplementedError

    def execute(self, subject, target=None, other_word=None):
        raise NotImplementedError

    @staticmethod
    def get_all_verbs():
        """
        :return: a list of objects each representing a default verb
        """
        return [verb() for verb in Verb.__subclasses__()]


class Adjective(Word):
    """
    Abstract implementation of an adjective
    Adjectives have tags, just like verbs
    If an adjective's tag matches the tag of a verb, it means the adjective can modify that verb in some way
    """

    def setup(self, subject, target=None, other_word=None):
        raise NotImplementedError

    def execute(self, subject, target=None, other_word=None):
        raise NotImplementedError

    @staticmethod
    def get_all_adjectives():
        """
        :return: a list of objects each representing a default verb
        """
        return [adjective() for adjective in Adjective.__subclasses__()]
