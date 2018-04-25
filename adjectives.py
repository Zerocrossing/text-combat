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
        self.power = 2.0
        self.cost = 2.0

    def modify_verb(self, verb):
        verb.power *= self.power
        verb.cost *= self.cost

    def setup(self, subject, target=None, verb=None):
        pass

    def execute(self, subject, target=None, verb=None):
        pass


class Restrained(Adjective):
    """
    Restrained halves dmg and cost
    """
    name = 'restrained'
    description = 'Decreases power and cost'

    def __init__(self):
        super().__init__()
        self.name = 'restrained'
        self.tags = ['power', 'cost']
        self.power = 0.5
        self.cost = 0.5

    def modify_verb(self, verb):
        verb.power *= self.power
        verb.cost *= self.cost

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

    def modify_verb(self, verb):
        pass

    def setup(self, subject, target=None, verb=None):
        verb.power += 0.05 * subject.stats.cunning
        verb.cost += 0.025 * subject.stats.cunning

    def execute(self, subject, target=None, verb=None):
        pass
