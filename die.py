"""Models a single die."""

import os


class Die(object):
    """Models a single die."""

    def __init__(self):
        pass

    def roll(self):
        """Roll the die."""
        theText = os.urandom.get_bytes(1)
        aByte = ord(theText)
        theResult = (aByte % 6) + 1
        return theResult

    
class Dice(object):
    """Models a collection of dice."""

    def __init__(self, count):
        self._dice = [None] * count
        for i in range(count):
            self._dice[i] = Die()

    def roll(self):
        """Role the dice."""
        theResult = [theDie.roll() for theDie in self._dice]
        return theResult
