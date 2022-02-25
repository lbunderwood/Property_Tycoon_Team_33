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
        for piece in player_pieces:
            player = Player("Player " + str(idx), piece)
            self.assertEqual(player.name, "Player " + str(idx))
            self.assertEqual(player.shape, piece)
            self.assertEqual(player.balance, 1500)
            self.assertEqual(player.properties, {})
            self.assertTrue(player.position[0] == 790 or 860)
            self.assertTrue(player.position[1] == 790 or 835 or 870)
            idx += 1

    # Tests error handling for invalid piece shape
    # by checking that it will call exit and print the proper error message
    def test_player_init_error(self):
        invalid_pieces = ["invalid piece", "", "©"]
        for piece in invalid_pieces:
            console_out = io.StringIO()
            sys.stdout = console_out
            try:
                self.assertRaises(SystemExit, Player("Name", piece))
            except SystemExit:
                pass
            self.assertEqual(console_out.getvalue(), "\nNot a valid player shape, check player info\n")
        sys.stdout = sys.__stdout__


# Test Case for testing the Dice class
class TestCard(unittest.TestCase):
    # Tests that initialization of values works
    def test_card_init(self):
        types = ["Pot Luck", "Opportunity Knocks"]
        descriptions = ["You are up the creek with no paddle - go back to the Old Creek", "You inherit £200",
                        "Bank pays you divided of £50", "Advance to Turing Heights"]
        for card_type in types:
            for description in descriptions:
                card = Card(card_type, description)
                self.assertEqual(card.card_type, card_type)
                self.assertEqual(card.description, description)


# Test Case for testing the Dice class
class TestProperty(unittest.TestCase):
    def test_property_init(self):
        #TODO: replace dummy code
        self.assertTrue(True)


# Test Case for testing the Dice class
class TestDice(unittest.TestCase):
    def test_dice_init(self):
        #TODO: replace dummy code
        self.assertTrue(True)


# Test Case for testing the Dice class
class TestGame(unittest.TestCase):
    def test_game_init(self):
        #TODO: replace dummy code
        self.assertTrue(True)


# popped this here just in case we want to have our test suite span multiple files in future
if __name__ == '__main__':
    unittest.main()
