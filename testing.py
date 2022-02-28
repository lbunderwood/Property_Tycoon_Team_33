# Created 2022-02-24 by Luke Underwood
# testing.py
# script for running unit tests on Property Tycoon classes and functions

# Import everything from game.py so we can do some sweet sweet testing
from game import *
import unittest
import io
import sys
import numpy


# Test case for testing the Player class
class TestPlayer(unittest.TestCase):
    # Checks that all the proper player pieces are possible
    # and all variables are assigned correctly
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
            self.assertEqual(player.image.get_size(), (24, 24))
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


# Test Case for testing the Card class
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


# Test Case for testing the Property class
class TestProperty(unittest.TestCase):
    def test_property_init(self):
        name, price, position, colour, rent, image = "test name", 5, 10, "red", 1000, "img"
        prop = Property(name, price, position, colour, rent, image)
        self.assertEqual(prop.name, name)
        self.assertEqual(prop.price, price)
        self.assertEqual(prop.position, position)
        self.assertEqual(prop.colour, colour)
        self.assertEqual(prop.rent, rent)
        self.assertEqual(prop.image, image)
        self.assertFalse(prop.mortgaged)
        self.assertEqual(prop.owner, "")


# Test Case for testing the Dice class
class TestDice(unittest.TestCase):

    # tests that die always rolls between 1 and 6, and has fairly uniform distribution
    def test_dice_roll(self):
        die = Dice()
        test_size = 1000
        tests = range(test_size)
        results = numpy.zeros_like(tests)
        for i in tests:
            result = die.roll()
            self.assertTrue(1 <= result <= 6)
            results[i] = result

        count = numpy.bincount(results)
        for i in range(1, 7):
            # dice must roll each number between 1/12 - 3/12 of the time
            self.assertAlmostEqual(test_size/6, count[i], delta=test_size/(6*2))


# Test Case for testing the Game class
class TestGame(unittest.TestCase):
    def test_game_init(self):
        _players = [Player('Waluigi', 'iron'), Player('Luigi', 'cat'), Player('Mario', 'boot'),
                    Player('Wario', 'hatstand'), Player('Toad', 'smartphone')]
        _game = Game(_players)
        self.assertEqual(_game.players, _players)


# popped this here just in case we want to have our test suite span multiple files in future
if __name__ == '__main__':
    unittest.main()
