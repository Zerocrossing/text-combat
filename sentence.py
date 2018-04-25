"""
Sentence creates a sentence object from a verb and (optionally) and adjective
It contains methods for setup and execution of the full sentence
"""
import copy


class Sentence:

    def __init__(self, subject, verb, adjective=None, target=None):
        """
        creates a sentence
        creates copies of the verb and adjective to modify their values
        :param subject: whoever is making the action
        :param verb: the action to take
        :param adjective: modifies the verb
        :param target: another actor the verb interacts with
        """
        self.subject = subject
        self.target = target
        self.verb = copy.deepcopy(verb)
        self.adjective = copy.deepcopy(adjective)

    def setup(self):
        if self.adjective is not None:
            self.adjective.modify_verb(self.verb)
            self.adjective.setup(self.subject, self.target, self.verb)
        self.verb.setup(self.subject, self.target, self.adjective)

    def execute(self):
        if self.adjective is not None:
            self.adjective.execute(self.subject, self.target, self.verb)
        self.verb.execute(self.subject, self.target, self.adjective)

    def __str__(self):
        if self.adjective is None:
            sentence = "{!s} used {!s}".format(self.subject, self.verb)
        else:
            sentence = "{!s} used {!s} {!s}".format(self.subject, self.adjective, self.verb)
        if self.target:
            sentence += " on {!s}".format(self.target)
        sentence += '\n' + '-'*25
        return sentence
