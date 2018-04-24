class Adverb:
    """
    Abstract implementation of an Adverb
    Adverbs have tags, just like verbs
    If an adverb's tag matches the tag of a verb, it means the adverb can modify that verb in some way
    is_universal means the adverb doesn't need to match tags to be used
        eg) an adverb that makes you block a portion of the next attack can be used regardless of action
    """

    def __init__(self):
        self.name = __class__
        self.is_universal = False
        self.freshness = 1.0
        self.tags = []

    def modify_verb(self, verb):
        """
        modify verb takes a verb and modifies it's attributes
        which attributes are modified depends
        """
        raise NotImplementedError

    def setup(self, subject, target=None, verb=None):
        """
        setup is run before damage and effects are assigned
        damage reduction, blocks, and checks can be done here
        it is not required and can be passed
        """
        raise NotImplementedError

    def execute(self, subject, target=None, verb=None):
        """
        execute assigns damage and effects one setup has established
        it is not required and can be passed
        """
        raise NotImplementedError

    def get_description(self):
        raise NotImplementedError

    def __str__(self):
        return self.name


class Powerful(Adverb):
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


class Restrained(Adverb):
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

class Stealthy(Adverb):
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
        verb.power *= 0.5 * subject.stats.cunning
        verb.cost *= 0.25 * subject.stats.cunning

    def execute(self, subject, target=None, verb=None):
        pass
