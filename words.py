"""
Module for all word based mechanics
"""


class Word:
    """
    Abstract class to represent all words
    Words are used in encounter scenarios to construct sentences which represent actor actions
    Attributes:
        freshness: a measure of how often the word has been used, most words should scale in effect with freshness
        tags: a list of strings associated with the word, eg "power" or "cost"
              tags are used to determine whether or not two words can interact, to do so they must share a tag
        is_infinite: boolean that determines whether or not the actor has a finite use of the word
        is_universal: if true, will cause two words to be viable regardless of tags, should only be used on adjectives
        description: text description of the word that should give the player an idea of what it does
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

    @staticmethod
    def get_word_from_name(name):
        """
        returns a default word object from a passed string
        :param name: string of the word name
        :return: a word object if the word is found, or none if not
        """
        for word in Verb.get_all_verbs() + Adjective.get_all_adjectives():
            if word.name == name:
                return word
        return None

    def modify_freshness(self, value):
        self.freshness += value
        if self.freshness < 0:
            self.freshness = 0
        if self.freshness > 1.0:
            self.freshness = 1.0

    def __str__(self):
        return self.name


class Verb(Word):
    """
    Abstract implementation of a Verb, derived from Word
    Verbs represent actions an actor can perform
    Verbs have tags that all modify the verbs performance in some way
    Verb execution is broken into 2 phases, setup and execute
    Setup is performed before actions are executed, and allows for things like blocking incoming damage
    Execute performs the action
    """

    def setup(self, subject, target=None, adjective=None):
        raise NotImplementedError

    def execute(self, subject, target=None, adjective=None):
        raise NotImplementedError

    @staticmethod
    def get_all_verbs():
        """
        todo: cache this?
        :return: a list of objects each representing a default verb
        """
        return [verb() for verb in Verb.__subclasses__()]


class Adjective(Word):
    """
    Abstract implementation of an adjective
    Adjectives have tags, just like verbs
    If an adjective's tag matches the tag of a verb, it means the adjective can modify that verb in some way
    modify_verb is called before setup to modify the tags of the verb itself
    currently all tags are implemented as floats representing a percentage of effectiveness
    eg) a verb with power = 1.0 will be 100% effective, multiplying the power by 2 will double it's effect
    """

    def modify_verb(self, subject, verb, target=None):
        raise NotImplementedError

    def setup(self, subject, target=None, verb=None):
        raise NotImplementedError

    def execute(self, subject, target=None, verb=None):
        raise NotImplementedError

    @staticmethod
    def get_all_adjectives():
        """
        todo: cache this
        :return: a list of objects each representing a default verb
        """
        return [adjective() for adjective in Adjective.__subclasses__()]
