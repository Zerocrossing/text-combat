import random
from words import *


# class Verb:
#     """
#     Abstract implementation of a Verb
#     Verbs represent actions an actor can perform
#     Verbs have tags representing attributes
#     These attributes modify the verb's performance in some way
#     Verb execution is broken into 2 phases, setup and execute
#     Setup is performed before actions are executed, and allows for things like blocking incoming damage
#     Execute performs the action
#     attributes:
#         freshness:      a metric that modifies power and decreases with each usage of the word
#         tags:           a list of keywords used to associate adverbs and verbs
#         is_infinite:    bool that sets if the word has finite usage
#     """
#
#     def __init__(self):
#         self.freshness = 1.0
#         self.tags = []
#         self.is_infinite = False
#
#     def works_with(self, adverb):
#         """
#         Checks if the passed adverb has an interaction with this verb
#         :param adverb: The adverb you want to check
#         :return: Boolean True if the very supports the adverb
#         """
#         if adverb.is_universal:
#             return True
#         for tag in adverb.tags:
#             if tag not in self.tags:
#                 return False
#         return True
#
#     def setup(self, subject, target=None, adverb=None):
#         """
#         setup is run before damage and effects are assigned
#         damage reduction, blocks, and checks can be done here
#         it is not required and can be passed
#         """
#         raise NotImplementedError
#
#     def execute(self, subject, target=None, adverb=None):
#         """
#         execute assigns damage and effects one setup has established
#         it is not required and can be passed
#         """
#         raise NotImplementedError
#
#     def get_description(self):
#         raise NotImplementedError
#
#     @staticmethod
#     def get_all_verbs():
#         """
#         :return: a list of objects each representing a default verb
#         """
#         return [verb() for verb in Verb.__subclasses__()]
#
#
#     def __str__(self):
#         return self.name


class Kick(Verb):
    """
    Kick is a basic physical attack that does 2-4 dmg per strength
    Kicking costs 10 stamina
    Damage scales with freshness, power and damage
    Stamina scales with cost
    tags: power, cost
    """
    name = "kick"
    description = "A basic kick. Deals damage based on strength."

    def __init__(self):
        super().__init__()
        self.name = 'kick'
        self.tags = ['power', 'damage', 'cost']
        self.power = 1.0
        self.damage = 1.0
        self.cost = 1.0

    def setup(self, subject, target=None, adverb=None):
        pass

    def execute(self, subject, target=None, adverb=None):
        """
        Calc damage and stamina
        """
        dmg = random.randint(2 * subject.stats.strength, 4 * subject.stats.strength)
        dmg *= self.power
        dmg *= self.damage
        dmg *= self.freshness
        target.take_damage(dmg)
        stam = -10
        stam *= self.cost
        subject.modify_stamina(stam)


class Sneak_Attack(Verb):
    """
    sneak_attack is a basic physical attack that does 1-2 dmg per cunning
    it costs 5 stamina
    Damage scales with freshness, power and damage
    Stamina scales with cost
    tags: power, damage, cost
    """
    name = "sneak attack"
    description = "A stealthy attack that deals damage based on cunning"

    def __init__(self):
        super().__init__()
        self.name = "sneak attack"
        self.tags = ['power', 'damage', 'cost']
        self.power = 1.0
        self.damage = 1.0
        self.cost = 1.0

    def setup(self, subject, target=None, adverb=None):
        pass

    def execute(self, subject, target=None, adverb=None):
        """
        Calc damage and stamina
        """
        dmg = random.randint(subject.stats.strength, 2 * subject.stats.strength)
        dmg *= self.power
        dmg *= self.damage
        dmg *= self.freshness
        target.take_damage(dmg)
        stam = -5
        stam *= self.cost
        subject.modify_stamina(stam)
