"""
Sentences represent actions that actors can take
A sentence is created from a verb and an optional adjective to modify the verb
Sentence execution happens in 3 phases:
    Firstly the setup() method has the adjective modify the verb when appropriate
    Secondly the sentence is executed by calling the execute methods of the words
    Lastly the actor's use_word() method is called which will decrease freshness and count if the word is finite
While not every sentence will use the full list of subject, verb, adjective and target, they should always be passed
"""
import copy


class Sentence:

    def __init__(self, subject, verb, adjective=None, target=None):
        """
        creates a sentence
        creates copies of the verb and adjective to modify their values
        maintains a reference to the subject's original words to call their methods
        :param subject: whoever is making the action
        :param verb: the action to take
        :param adjective: modifies the verb
        :param target: another actor the verb interacts with
        """
        self.subject = subject
        self.target = target
        self.subject_verb = verb
        self.subject_adjective = adjective
        self.verb = copy.deepcopy(verb)
        self.adjective = copy.deepcopy(adjective)

    def setup(self):
        if self.adjective is not None:
            self.adjective.modify_verb(self.verb)
            self.adjective.setup(self.subject, self.target, self.verb)
        self.verb.setup(self.subject, self.target, self.adjective)

    def execute(self):
        """
        Execute performs the actions of the sentence after setup has initialized all values
        It calls the execute() method of the verb and adjective (if available)
        It then calls the actor's use_word() method (using the name because the objects have been copied)
        :return:
        """
        # call execute methods
        if self.adjective is not None:
            self.adjective.execute(self.subject, self.target, self.verb)
        self.verb.execute(self.subject, self.target, self.adjective)
        # call subject's use_word and refresh_all, excluding any words used this round
        exclude = [self.subject_verb]
        self.subject.use_word(self.subject_verb)
        if self.subject_adjective is not None:
            self.subject.use_word(self.subject_adjective)
            exclude.append(self.subject_adjective)
        self.subject.refresh_all(excluded=exclude)

    def __str__(self):
        if self.adjective is None:
            sentence = "{!s} used {!s}".format(self.subject, self.verb)
        else:
            sentence = "{!s} used {!s} {!s}".format(self.subject, self.adjective, self.verb)
        if self.target:
            sentence += " on {!s}".format(self.target)
        sentence += '\n' + '-' * 25
        return sentence
