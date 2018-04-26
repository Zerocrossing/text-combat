"""
Build Character
Running main will start a simple text based interface that prompts the user to create a character
After the character is created combat_arena.begin() is called to test the character in a dummy arena
"""

import os
from actor import Actor
import combat_arena
from stats import *
from verbs import *
from adjectives import *
from util import *

# evil globals
player = Actor()


# region Character Creation
def intro():
    """
    Prompts for character name and moves to stat selection
    """
    print_banner('Character Creation')
    while True:
        usrin = input('Enter your character name: ')
        if usrin is None or usrin == "" or usrin[0] == " ":
            print("Invalid name. Try again: ")
        else:
            player.name = usrin
            break
    choose_stats()


def choose_stats(points=25):
    """
    Point buy system for stats
    After points are reduced to 0 choose_words is executed
    """
    while True:
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


def choose_words(points=4):
    """
    Goes into a point-buy system where the player is allowed to purchase words
    """
    verb_list = Verb.get_all_verbs()
    adjective_list = Adjective.get_all_adjectives()

    while True:
        clear_screen()
        print_banner("Purchase Words")
        print("Purchases Available: " + str(points))
        print("\nVerbs:")
        for verb in verb_list:
            out = "\t{:<15}: {}".format(verb.name, verb.description)
            print(out)
        print("\nAdjectives:")
        for adjective in adjective_list:
            out = "\t{:<15}: {}".format(adjective.name, adjective.description)
            print(out)
        print('*' * 10)
        print("Your Verbs: ")
        for word, count in player.words.items():
            if isinstance(word, Verb):
                print("{:<10}: {}".format(word.name, count))
        print("\nYour Adjectives: ")
        for word, count in player.words.items():
            if isinstance(word, Adjective):
                print("{:10}: {}".format(word.name, count))
        # get user input
        word_name, count = parse_words(points)
        if count == 1:
            player.add_word(word_name, count=count)
        if count == -1:
            player.remove_word(word_name)
        points -= count
        if points == 0:
            break
    combat_arena.begin(player)


def parse_words(points):
    """
    User interface for purchasing words
    todo: have a cost associated with words?
    :param points: remaining points
    :return: a valid word name
    """
    while (True):
        usrin = input("add or remove words: eg) 'add kick': ")
        usrin = usrin.split(' ', 1)
        # error checking
        if len(usrin) < 2:
            print("Sorry, I don't understand")
            continue
        direction = usrin[0].lower()
        word_name = usrin[1].lower()
        if direction != 'add' and direction != 'remove':
            print('command must start with add or remove')
            continue
        number = 1
        if direction == 'remove':
            number = -1
        if Word.get_word_from_name(word_name) is None:
            print("sorry " + usrin[1] + " is not a valid word name")
            continue
        if (points - number) < 0:
            print("you don't have enough points for that")
            continue
        return [word_name, number]


# endregion


# region Word Selection


# endregion


if __name__ == "__main__":
    clear_screen()
    intro()
