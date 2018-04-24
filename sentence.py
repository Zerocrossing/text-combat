"""
Sentence creates a sentence object from a verb and (optionally) and adverb
It contains methods for setup and execution of the full sentence
"""
import copy


class Sentence:

    def __init__(self, subject, verb, adverb=None, target=None):
        self.subject = subject
        self.verb = copy.deepcopy(verb)
        self.adverb = copy.deepcopy(adverb)
        self.target = target

    def setup(self):
        self.adverb.modify_verb(self.verb)
        self.adverb.setup(self.subject, self.target, self.verb)
        self.verb.setup(self.subject, self.target, self.adverb)

    def execute(self):
        self.adverb.execute(self.subject, self.target, self.verb)
        self.verb.execute(self.subject, self.target, self.adverb)

    def __str__(self):
        sentence = "{!s} used {!s} {!s}".format(self.subject, self.adverb, self.verb)
        if self.target:
            sentence+=" on {!s}".format(self.target)
        return sentence
