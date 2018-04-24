"""
utility methods
"""
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner(text, char='*', padding=2):
    box_len = len(text) + padding * 2 + 2
    output = ''
    output += char * box_len + '\n'
    output += char + " " * padding + text + " " * padding + char + '\n'
    output += char * box_len + '\n'
    print(output)