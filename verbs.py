import random
from words import *


class Kick(Verb):
    """
    Kick is a basic physical attack that does 2-4 dmg per strength
    Kicking costs 10 stamina
    Damage scales with freshness, power and damage
    Stamina scales with cost
    tags: power, cost
    """

    def __init__(self):
        super().__init__()
        self.name = 'kick'
        self.description = "A basic kick. Deals damage based on strength."
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


class SneakAttack(Verb):
    """
    sneak_attack is a basic physical attack that does 1-2 dmg per cunning
    it costs 5 stamina
    Damage scales with freshness, power and damage
    Stamina scales with cost
    tags: power, damage, cost
    """

    def __init__(self):
        super().__init__()
        self.name = "sneak attack"
        self.tags = ['power', 'damage', 'cost']
        self.power = 1.0
        self.damage = 1.0
        self.cost = 1.0
        self.description = "A stealthy attack that deals damage based on cunning"

    def setup(self, subject, target=None, adverb=None):
        pass

    def execute(self, subject, target=None, adverb=None):
        """
        Calc damage and stamina
        """
        dmg = random.randint(subject.stats.cunning, 2 * subject.stats.cunning)
        dmg *= self.power
        dmg *= self.damage
        dmg *= self.freshness
        target.take_damage(dmg)
        stam = -5
        stam *= self.cost
        subject.modify_stamina(stam)
