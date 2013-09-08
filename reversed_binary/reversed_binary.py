#!/usr/bin/env python

__author__ = "Alonso Vidales"
__email__ = "alonso.vidales@tras2.es"
__date__ = "2013-01-13"

class ReversedBinary:
    __number_to_reverse = None

    def resolve(self):
        """
        Returns the integer that corresponds to the reversed binary
        representation of the given integer at the constructor
        """
        # Get the binary representation as a string without the prefix 0b
        bin_str = bin(self.__number_to_reverse)[2:]
        # Reverse the string and convert it to integer
        return int(bin_str[::-1], 2)

    def __init__(self, number):
        self.__number_to_reverse = int(number)

if __name__ == "__main__":
    print ReversedBinary(raw_input()).resolve()
