"""
pits the player against a random goblin
"""
import actor
import player
import random
from verbs import *
from adjectives import *
from sentence import *
from util import *


def begin(fighter):
    difficulty = 0
    while True:
        difficulty +=1
        clear_screen()
        print_banner("Welcome To The Arena")
        print("You are at level {}".format(difficulty))
        g = create_goblin(difficulty)
        print("You will be fighting {}".format(g.name))
        combat(fighter, g)


def combat(fighter, opponent):
    clear_screen()
    while True:
        if fighter.is_dead():
            game_over()
        if opponent.is_dead():
            victory()
            return
        print("Your health: {:<15} \t Your Stamina: {}".format(fighter.health, fighter.stamina))
        print("Opponent health: {:<15} \t Opponent Stamina: {}".format(opponent.health, opponent.stamina))
        player_sentence = player_turn(fighter, opponent)
        opponent_sentence = opponent.take_turn(fighter)
        player_sentence.setup()
        opponent_sentence.setup()
        print(player_sentence)
        player_sentence.execute()
        print(opponent_sentence)
        opponent_sentence.execute()


def player_turn(fighter, opponent):
    if any(fighter.verbs):
        print("Your Verbs: ")
        for key, val in fighter.verbs.items():
            print('\t' + key + '\t' + str(val[1]))
    while True:
        verb = input("What would you like to do? (choose a verb)")
        if verb not in fighter.verbs.keys():
            print("That is not a valid action.")
            continue
        verb = fighter.verbs[verb][0]
        # print("You have selected {}".format(verb.name))
        break
    if any(fighter.adjectives):
        print("Your adjectives: ")
        for key, val in fighter.adjectives.items():
            print('\t' + key + '\t' + str(val[1]))
    while True:
        adjective = input("What kind of {}? (choose an adjective)".format(verb.name))
        if adjective not in fighter.adjectives.keys():
            print("That is not a valid action.")
            continue
        adjective = fighter.adjectives[adjective][0]
        # print("You have selected {}".format(adjective.name))
        break

    sentence = Sentence(fighter, verb, adjective, opponent)
    return sentence


def game_over():
    clear_screen()
    print_banner("YOU DIED")
    quit()


def victory():
    print_banner("VICTORY")
    input()
    return


def create_goblin(difficulty):
    g = Goblin(difficulty)
    return g


class Goblin(actor.Actor):

    def __init__(self, difficulty=1):
        """
        creates a random goblin using a difficulty seed
        stats are randomized with 4*difficulty (roughly +1 to all stats per level)
        goblins are given all words
        when they attack they pick an adjective and verb randomly
        """
        super().__init__()
        self.random_name()
        rand_stats = [1, 1, 1, 1]
        points = 4 * difficulty
        while points > 0:
            num = random.randint(0, 3)
            rand_stats[num] += 1
            points -= 1
        self.stats.set_stats(rand_stats)
        self.give_all_words()
        self.health = 10 * self.stats.endurance

    def take_damage(self, dmg):
        value = round(dmg)
        print("{} took {} damage.".format(self.name, value))
        self.health -= value

    def take_turn(self, target):
        """
        creates a random sentence for the goblin
        :param target: player presumably
        :return: the created sentence
        """
        sentence = self.create_random_sentence(target)
        return sentence

    def give_all_words(self):
        for verb in Verb.__subclasses__():
            word = verb()
            self.verbs[word.name] = [word, 99]
        for adjective in Adjective.__subclasses__():
            word = adjective()
            self.adjectives[word.name] = [word, 99]

    def create_random_sentence(self, target):
        verb = random.choice([v[0] for v in self.verbs.values()])
        adjective = random.choice([adv[0] for adv in self.adjectives.values()])
        sentence = Sentence(self, verb, adjective, target)
        return sentence

    def __str__(self):
        return self.name

    def random_name(self):
        prefix = ['grok', 'bim', 'urk', 'grak', 'frag', 'kul']
        suffix = ['nar', 'strok', 'dun', 'lok', 'klok', 'dorn']
        name = random.choice(prefix) + random.choice(suffix)
        self.name = name


if __name__ == "__main__":
    p = create_goblin(5)
    begin(p)
    # player = player.Player()
    # g = goblin(1)
    # print("Creating goblin:\n" + str(g.stats))
    # print("Health: {}".format(g.health))
    # print(g.take_turn(player))
