#!/usr/bin/env python

__author__ = "Alonso Vidales"
__email__ = "alonso.vidales@tras2.es"
__date__ = "2013-01-13"

class ReversedBinary:
    __numberToReverse = None

    def resolve(self):
        """
        Returns the integer that corresponds to the reversed binary
        representation of the given integer at the constructor
        """
        # Get the binary representation as a string without the prefix 0b
        binStr = bin(self.__numberToReverse)[2:]
        # Reverse the string and convert it to integer
        return int(binStr[::-1], 2)

    def __init__(self, inNumber):
        self.__numberToReverse = int(inNumber)

if __name__ == "__main__":
    print ReversedBinary(raw_input()).resolve()
