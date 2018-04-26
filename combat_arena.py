"""
pits the player against successive random goblins with increasing stats
"""
import actor
import random
from verbs import *
from adjectives import *
from sentence import *
from util import *

# evil globals
difficulty = 0


def begin(fighter):
    while True:
        global difficulty
        difficulty += 1
        fighter.health = fighter.get_max_health()
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
        print('*' * 25)
        print("{:<16} {:<5} \t {:<17} {}".format('Your Health:', fighter.health, 'Your Stamina:', fighter.stamina))
        print(
            "{:<16} {:<5} \t {:<17} {}".format('Opponent Health:', opponent.health, 'Opponent Stamina:',
                                               opponent.stamina))
        print("*" * 25)
        player_sentence = player_turn(fighter, opponent)
        clear_screen()
        opponent_sentence = opponent.take_turn(fighter)
        player_sentence.setup()
        opponent_sentence.setup()
        print(player_sentence)
        player_sentence.execute()
        print(opponent_sentence)
        opponent_sentence.execute()


def player_turn(fighter, opponent):
    print("{:<15} {:<10} {}".format("Your verbs", "Freshness", "Uses"))
    for verb in fighter.get_verbs():
        print("{:<15} {:<10} {}".format(verb.name, int(verb.freshness*100), fighter.words[verb]))
    while True:
        verb = input("\nWhat would you like to do? (choose a verb):")
        verb = fighter.get_word_by_name(verb)
        if verb is None:
            print("That is not a valid action.")
            continue
        break
    if any(fighter.get_adjectives()):
        print("{:<15} {:<10} {}".format("Your Adjectives", "Freshness", "Uses"))
        for adjective in fighter.get_adjectives():
            print("{:<15} {:<10} {}".format(adjective.name, int(adjective.freshness * 100), fighter.words[adjective]))
    while True:
        adjective = input("\nWhat kind of {}? (choose an adjective or None): ".format(verb.name))
        if adjective == "none":
            adjective = None
        elif fighter.get_word_by_name(adjective) is None:
            print("That is not a valid action.")
            continue
        adjective = fighter.get_word_by_name(adjective)
        break
    sentence = Sentence(fighter, verb, adjective, opponent)
    return sentence


def game_over():
    clear_screen()
    print_banner("YOU DIED")
    print("You made it to level {}".format(difficulty))
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
        self.give_all_words()
        # randomize stats
        rand_stats = [1, 1, 1, 1]
        points = 4 * difficulty
        while points > 0:
            num = random.randint(0, 3)
            rand_stats[num] += 1
            points -= 1
        self.stats.set_stats(rand_stats)
        self.health = 10 * self.stats.endurance

    def modify_stat(self, stat, value):
        pass

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
        verbs = Verb.get_all_verbs()
        adjectives = Adjective.get_all_adjectives()
        for word in verbs + adjectives:
            self.add_word(word, 99)

    def create_random_sentence(self, target):
        verb = random.choice(self.get_verbs(usable=True))
        adjective = random.choice(self.get_adjectives(usable=True))
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
