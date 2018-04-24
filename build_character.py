import os
import combat_arena
from player import Player
from stats import *
from verbs import *
from adverbs import *
from util import *

# evil globals
player = Player()


# region Character Creation
def intro():
    """
    Prompts for character name and moves to stat selection
    """
    print_banner('Character Creation')
    while (True):
        usrin = input('Enter your character name: ')
        if usrin is None or usrin == "" or usrin[0] == " ":
            print("That name makes no goddamn sense. Try again: ")
        else:
            player.name = usrin
            break
    choose_stats()


def choose_stats(points=25):
    """
    Point buy system for stats
    After points are reduced to 0 choose_words is executed
    """
    while (True):
        clear_screen()
        print_banner(player.name.title() + "'s stats")
        print(str(points) + " Points Remaining")
        print(player.stats)
        print("Change your stats by entering 'add/remove' 'number' 'stat name' \n"
              "for example 'add 3 strength'\n")
        if points == 0:
            break
        points = parse_stats(points)
    player.health = player.get_max_health()
    choose_words()


def parse_stats(points):
    """parses stats and adds them to player"""
    while (True):
        usrin = input()
        usrin = usrin.split()
        # error checking
        if len(usrin) != 3:
            print("Sorry, I don't understand")
            continue
        direction = usrin[0].lower()
        number = usrin[1]
        stat_name = usrin[2].lower()
        if direction != 'add' and direction != 'remove':
            print('you need to add or remove stats')
            continue
        if not number.isdigit():
            print("you need to add or remove by a number")
            continue
        number = int(number)
        if direction == 'remove':
            number *= -1
        if stat_name not in stat_names:
            print("sorry " + usrin[2] + " is not a valid stat name")
            continue
        if (points - number) < 0:
            print("you don't have enough points for that")
            continue
        # add stats
        curr_val = getattr(player.stats, stat_name.lower())
        setattr(player.stats, stat_name.lower(), curr_val + number)
        points = points - number
        return points


def choose_words(points=100):
    """
    Goes into a point-buy system where the player is allowed to purchase words
    :param points:
    :return:
    """
    verb_list = Verb.__subclasses__()
    adverb_list = Adverb.__subclasses__()
    valid_words = [x.name.lower() for x in Verb.__subclasses__()] + [x.name.lower() for x in
                                                                     Adverb.__subclasses__()]
    while True:
        clear_screen()
        print_banner("Purchase Words")
        print("Your points: " + str(points))
        print("\nVerbs: (10 each)")
        for verb in verb_list:
            out = "\t{:<15}: {}".format(verb.name, verb.description)
            print(out)
        print("\nAdverbs: (10 each)")
        for adverb in adverb_list:
            out = "\t{:<15}: {}".format(adverb.name, adverb.description)
            print(out)
        print('*'*10)
        if any(player.verbs):
            print("Your Verbs: ")
            for key, val in player.verbs.items():
                print('\t' + key + '\t' + str(val[1]))
        if any(player.adverbs):
            print("Your Adverbs: ")
            for key, val in player.adverbs.items():
                print('\t' + key + '\t' + str(val[1]))
        # get user input
        word_name, count = parse_words(points, valid_words)
        for word in verb_list + adverb_list:
            if word.name.lower() == word_name.lower():
                new_word = word()
                player.add_word(new_word, count)
                points -= (count * 10)
        if points == 0:
            break
    combat_arena.begin(player)



def parse_words(points, valid_words):
    """
    User interface for purchasing words
    todo: have a cost associated with words?
    :param points: remaining points
    :param valid_words: a list of valid word names
    :return: a list with [0] being the string word name and [1] being the count
    """
    while (True):
        usrin = input()
        usrin = usrin.split(' ', 2)
        # error checking
        if len(usrin) < 3:
            print("Sorry, I don't understand")
            continue
        direction = usrin[0].lower()
        number = usrin[1]
        word_name = usrin[2].lower()
        if direction != 'add' and direction != 'remove':
            print('command must start with add or remove')
            continue
        if not number.isdigit():
            print("you need to add or remove by a number")
            continue
        number = int(number)
        if direction == 'remove':
            number *= -1
        if word_name not in valid_words:
            print("sorry " + usrin[2] + " is not a valid word name")
            continue
        if (points - number * 10) < 0:
            print("you don't have enough points for that")
            continue
        # add stats
        return [word_name, number]


# endregion


# region Word Selection



# endregion


if __name__ == "__main__":
    print("garbage")
    clear_screen()
    intro()
    os.system('clear')
