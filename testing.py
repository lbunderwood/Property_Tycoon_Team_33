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
            player = Player(piece)
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
                self.assertRaises(SystemExit, Player(piece))
            except SystemExit:
                pass
            self.assertEqual(console_out.getvalue(), "\nNot a valid player shape, check player info\n")
        sys.stdout = sys.__stdout__


# Test Case for testing the CardStack class
class TestCardStack(unittest.TestCase):
    # Tests that initialization of values works
    def test_cardstack_init_valid(self):
        potLuck = CardStack("Pot Luck")
        potLuckCards = numpy.genfromtxt("cards/Pot_Luck.txt", dtype=str, delimiter=';')

        self.assertEqual(potLuck.type, "Pot Luck")
        for card in potLuck.cards:
            self.assertIn(card, potLuckCards)

        opportunityKnocks = CardStack("Opportunity Knocks")
        opportunityCards = numpy.genfromtxt("cards/Opportunity_Knocks.txt", dtype=str, delimiter=';')

        self.assertEqual(opportunityKnocks.type, "Opportunity Knocks")
        for card in opportunityKnocks.cards:
            self.assertIn(card, opportunityCards)

    def test_cardstack_init_error(self):
        invalid_types = ["invalid", "", "©"]
        for card_type in invalid_types:
            console_out = io.StringIO()
            sys.stdout = console_out
            try:
                self.assertRaises(SystemExit, CardStack(card_type))
            except SystemExit:
                pass
            self.assertEqual(console_out.getvalue(), "\nInvalid card type given to CardStack\n")
        sys.stdout = sys.__stdout__

    def test_cardstack_shuffle(self):
        cards = CardStack("Pot Luck")
        cards.shuffle()
        shuffled = False
        i = 0

        # check that we have all the cards and they are not in the same order
        potLuckCards = numpy.genfromtxt("cards/Pot_Luck.txt", dtype=str, delimiter=';')[0:, 0]
        for card in cards.cards:
            self.assertIn(card, potLuckCards)
            if card != potLuckCards[i]:
                shuffled = True
            i += 1
        self.assertTrue(shuffled)

    def test_cardstack_draw(self):
        pass


# Test Case for testing the Property class
class TestProperty(unittest.TestCase):
    def test_property_init(self):
        price, position, colour, rent, image = 5, 10, "red", 1000, "img"
        prop = Property(price, position, colour, rent, image)
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
    def test_dice_init(self):
        test_size = 1000
        tests = range(test_size)
        results = numpy.zeros_like(tests)
        for i in tests:
            die = Dice()
            result = die.number
            self.assertIn(result, range(1, 7))
            results[i] = result

        count = numpy.bincount(results)
        for i in range(1, 7):
            # dice must roll each number between 1/12 - 3/12 of the time
            self.assertAlmostEqual(test_size/6, count[i], delta=test_size/(6*2))


# Test Case for testing the Game class
class TestGame(unittest.TestCase):
    def test_game_init(self):
        _players = [Player('iron'), Player('cat'), Player('boot'),
                    Player('hatstand'), Player('smartphone')]
        _game = Game(_players)
        self.assertEqual(_game.players, _players)


# popped this here just in case we want to have our test suite span multiple files in future
if __name__ == '__main__':
    unittest.main()
