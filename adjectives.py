"""
Adjectives Module
Contains all classes derived from Adjective
Adjectives are used in sentences to modify verbs
This is done by linking tags on the two objects, if a tag is shared, the adjective can modify the verb in some way
"""

from words import *


class Powerful(Adjective):
    """
    Powerful doubles power and cost
    """
    name = 'powerful'
    description = 'Increases power but also increases cost'

    def __init__(self):
        super().__init__()
        self.name = 'powerful'
        self.tags = ['power', 'cost']
        self.power_mod = 2.0
        self.cost_mod = 2.0

    def modify_verb(self, verb):
        verb.power *= self.power_mod
        verb.cost *= self.cost_mod

    def setup(self, subject, target=None, verb=None):
        pass

    def execute(self, subject, target=None, verb=None):
        pass


class Restrained(Adjective):
    """
    Restrained halves dmg and cost
    """
    def __init__(self):
        super().__init__()
        self.name = 'restrained'
        self.description = 'Decreases power and cost'
        self.tags = ['power', 'cost']
        self.power_mod = 0.5
        self.cost_mod = 0.5

    def modify_verb(self, verb):
        verb.power *= self.power_mod
        verb.cost *= self.cost_mod

    def setup(self, subject, target=None, verb=None):
        pass

    def execute(self, subject, target=None, verb=None):
        pass


class Stealthy(Adjective):
    """
    Stealthy increases damage by 5% for each point of cunning
    it increases cost for 2.5% for each point of cunning
    """
    name = 'stealthy'
    description = 'Increases power and cost based on cunning'

    def __init__(self):
        super().__init__()
        self.name = 'stealthy'
        self.tags = ['power', 'cost']
        self.power_mod = 0.05
        self.cost_mod = 0.025

    def modify_verb(self, verb):
        pass

    def setup(self, subject, target=None, verb=None):
        verb.power += self.power_mod * subject.stats.cunning
        verb.cost += self.cost_mod * subject.stats.cunning

    def execute(self, subject, target=None, verb=None):
        pass
