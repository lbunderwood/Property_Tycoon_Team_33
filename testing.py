# Created 2022-02-24 by Luke Underwood
# testing.py
# script for running unit tests on Property Tycoon classes and functions

# Import everything from game.py so we can do some sweet sweet testing
from game import *
import unittest
import io
import sys


# Test case for testing the player class
class TestPlayer(unittest.TestCase):
    # Checks that all the proper player pieces are possible
    # and names and shapes are assigned correctly
    def test_player_init_valid(self):
        player_pieces = ["boot", "ship", "hatstand", "smartphone", "cat", "iron"]
        idx = 0
        for pieces in player_pieces:
            player = Player("Player " + str(idx), pieces)
            self.assertEqual(player.name, "Player " + str(idx))
            self.assertEqual(player.shape, pieces)
            idx = idx + 1

    # Tests error handling for invalid piece shape
    # by checking that it will call exit and print the proper error message
    def test_player_init_error(self):
        console_out = io.StringIO()
        sys.stdout = console_out
        try:
            self.assertRaises(SystemExit, Player("Name", "invalid piece"))
        except SystemExit:
            pass
        sys.stdout == sys.__stdout__    # ignore warning message this is important
        self.assertEqual(console_out.getvalue(), "\nNot a valid player shape, check player info\n")


# popped this here just in case we want to have our test suite span multiple files in future
if __name__ == '__main__':
    unittest.main()
