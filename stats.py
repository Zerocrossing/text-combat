"""
Stats is a class that represents an actor's Physical Abilities
"""


class Stats:
    def __init__(self):
        self.strength = 0
        self.endurance = 0
        self.cunning = 0
        self.intelligence = 0

    def get_stats(self):
        """
        Gets all the stats for this object
        :return: All stats in a dict
        """
        stats = {
            'strength': self.strength,
            'cunning': self.cunning,
            'endurance': self.endurance,
            'intelligence': self.intelligence
        }
        return stats

    def set_stats(self, stats):
        """
        Sets stats in accordance with a passed list
        Used to randomize stats on NPC creation
        :param stats: a list of size 4
        :return: None
        """
        self.strength = stats[0]
        self.cunning = stats[1]
        self.endurance = stats[2]
        self.intelligence = stats[3]

    def __str__(self):
        """
        Makes a nicely formatted string of stats
        :return: stats as string
        """
        stats = self.get_stats()
        output = ''
        for stat, val in stats.items():
            output += "{:<15}: {}\n".format(stat, val)
        return output


# lowercase stat names in a set used for character creation
stat_names = set(['strength', 'cunning', 'endurance', 'intelligence'])
