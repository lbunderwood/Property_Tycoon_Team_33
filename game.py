import numpy
import pygame
import ctypes
import os
import random
from sys import exit

WIDTH = HEIGHT = 910

# Makes our window ignore Windows OS application scaling
ctypes.windll.user32.SetProcessDPIAware()

# Makes the window appear in the middle of a 1920 x 1080 display
x = 505
y = 50
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)


class Player:
    def __init__(self, shape):
        self.balance = 1500
        self.properties = {}
        self.shape = shape
        self.position = (770, 770)
        if self.shape == 'boot':
            # self.position = (790, 790)
            self.image = pygame.image.load('graphics/boot.png')
        elif self.shape == 'ship':
            # self.position = (860, 790)
            self.image = pygame.image.load('graphics/ship.png')
        elif self.shape == 'hatstand':
            # self.position = (860, 835)
            self.image = pygame.image.load('graphics/hatstand.png')
        elif self.shape == 'smartphone':
            # self.position = (790, 870)
            self.image = pygame.image.load('graphics/smartphone.png')
        elif self.shape == 'cat':
            # self.position = (860, 870)
            self.image = pygame.image.load('graphics/cat.png')
        elif self.shape == 'iron':
            # self.position = (790, 835)
            self.image = pygame.image.load('graphics/iron.png')
        else:
            print("\nNot a valid player shape, check player info")
            pygame.quit()
            exit()

    # takes card stack as input, draws card, applies result of card, and returns pygame image object
    def draw_card(self, stack):
        card = stack.draw()
        cardImage = "VAR INIT"

        if card == "Bank pays you divided of £50":
            self.balance += 50
            cardImage = pygame.image.load('graphics/opportunity knocks 1.png')
        elif card == "You have won a lip sync battle. Collect £100":
            self.balance += 100
            cardImage = pygame.image.load('graphics/opportunity knocks 2.png')
        elif card == "Advance to Turing Heights":
            self.move_to('turing')
            cardImage = pygame.image.load('graphics/opportunity knocks 3.png')
        elif card == "Advance to Han Xin Gardens. If you pass GO, collect £200":
            self.move_to('hanxin')
            cardImage = pygame.image.load('graphics/opportunity knocks 3(1).png')
        elif card == "Fined £15 for speeding":
            self.balance -= 15
            # TODO: add payment to free parking
            cardImage = pygame.image.load('graphics/opportunity knocks 4.png')
        elif card == "Pay university fees of £150":
            self.balance -= 150
            cardImage = pygame.image.load('graphics/opportunity knocks 5.png')
        elif card == "Take a trip to Hove station. If you pass GO collect £200":
            self.move_to('hove')
            cardImage = pygame.image.load('graphics/opportunity knocks 6.png')
        elif card == "Loan matures, collect £150":
            self.balance += 150
            cardImage = pygame.image.load('graphics/opportunity knocks 7.png')
        elif card == "You are assessed for repairs, £40/house, £115/hotel":
            # TODO: add calculation, property class needs houses/hotels
            cardImage = pygame.image.load('graphics/opportunity knocks 8.png')
        elif card == "Advance to GO":
            self.move_to('go')
            if stack.type == "Opportunity Knocks":
                cardImage = pygame.image.load('graphics/opportunity knocks 9.png')
            else:
                cardImage = pygame.image.load('graphics/pot luck 8.png')
        elif card == "You are assessed for repairs, £25/house, £100/hotel":
            # TODO: add calculation, property class needs houses/hotels
            cardImage = pygame.image.load('graphics/opportunity knocks 10.png')
        elif card == "Go back 3 spaces":
            self.move_x(-3)
            cardImage = pygame.image.load('graphics/opportunity knocks 11.png')
        elif card == "Advance to Skywalker Drive. If you pass GO collect £200":
            self.move_to('skywalker')
            cardImage = pygame.image.load('graphics/opportunity knocks 12.png')
        elif card == "Go to jail. Do not pass GO, do not collect £200":
            self.move_to('jail')
            if stack.type == "Opportunity Knocks":
                cardImage = pygame.image.load('graphics/opportunity knocks 13.png')
            else:
                cardImage = pygame.image.load('graphics/pot luck 14.png')
        elif card == "Drunk in charge of a hoverboard. Fine £30":
            self.balance -= 30
            cardImage = pygame.image.load('graphics/opportunity knocks 14.png')
        elif card == "Get out of jail free":
            # TODO: add get out of jail free
            if stack.type == "Opportunity Knocks":
                cardImage = pygame.image.load('graphics/opportunity knocks 15.png')
            else:
                cardImage = pygame.image.load('graphics/pot luck 17.png')
        elif card == "You inherit £200":
            self.balance += 200
            cardImage = pygame.image.load('graphics/pot luck 1.png')
        elif card == "You have won 2nd prize in a beauty contest, collect £50":
            self.balance += 50
            cardImage = pygame.image.load('graphics/pot luck 2.png')
        elif card == "You are up the creek with no paddle - go back to the Old Creek":
            self.move_to('creek')
            cardImage = pygame.image.load('graphics/pot luck 3.png')
        elif card == "Student loan refund. Collect £20":
            self.balance += 20
            cardImage = pygame.image.load('graphics/pot luck 4.png')
        elif card == "Bank error in your favour. Collect £200":
            self.balance += 200
            cardImage = pygame.image.load('graphics/pot luck 5.png')
        elif card == "Pay bill for text books of £100":
            self.balance -= 100
            cardImage = pygame.image.load('graphics/pot luck 6.png')
        elif card == "Mega late night taxi bill pay £50":
            self.balance -= 50
            cardImage = pygame.image.load('graphics/pot luck 7.png')
        elif card == "From sale of Bitcoin you get £50":
            self.balance += 50
            cardImage = pygame.image.load('graphics/pot luck 9.png')
        elif card == "Bitcoin assets fall - pay off Bitcoin short fall":
            self.balance -= 50
            cardImage = pygame.image.load('graphics/pot luck 10.png')
        elif card == "Pay a £10 fine or take opportunity knocks":
            # TODO: add interface for decision
            # the tenner goes to free parking
            cardImage = pygame.image.load('graphics/pot luck 11.png')
        elif card == "Pay insurance fee of £50":
            self.balance -= 50
            cardImage = pygame.image.load('graphics/pot luck 12.png')
        elif card == "Savings bond matures, collect £100":
            self.balance += 100
            cardImage = pygame.image.load('graphics/pot luck 13.png')
        elif card == "Received interest on shares of £25":
            self.balance += 25
            cardImage = pygame.image.load('graphics/pot luck 15.png')
        elif card == "It's your birthday. Collect £10 from each player":
            # TODO: add deduction from other players and way of knowing how many players
            player_count = 4
            self.balance += 10 * player_count
            cardImage = pygame.image.load('graphics/pot luck 16.png')
        else:
            print("\nInvalid card description \""+card+"\" passed to Player.draw_card()")
            pygame.quit()
            exit()

        return cardImage

    def move_x(self, spaces):
        current = tiles.index(self.position)
        destination_index = current - spaces

        if destination_index > len(tiles) - 1:
            destination_index -= len(tiles) - 1

        self.position = tiles[destination_index]
        print('current: ', destination_index)

    def move_to(self, space):
        if space in properties:
            destination = properties[space].position
        elif space in card_spaces:
            destination = card_spaces[space].position
        elif space in taxes:
            destination = taxes[space].position
        elif space in corners:
            destination = corners[space].position
        else:
            print("\nInvalid space \"" + space + "\" passed to Player.move_to()")
            pygame.quit()
            exit()

        self.position = destination

class CardStack:
    def __init__(self, card_type):
        if not (card_type == "Opportunity Knocks" or card_type == "Pot Luck"):
            print("\nInvalid card type \""+card_type+"\" given to CardStack")
            pygame.quit()
            exit()

        rawCards = numpy.genfromtxt("cards/"+card_type.replace(' ', '_')+".txt", dtype=str, delimiter=';')
        self.cards = rawCards[0:, 0]
        self.type = card_type

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        card = self.cards[0]
        self.cards = numpy.roll(self.cards, -1)
        return card


# class separate for just tracking positions
class Tile:
    def __init__(self, position, image):
        self.position = position
        self.image = image


class Property:
    def __init__(self, price, position, colour, rent, image):
        self.price = price
        self.position = position
        self.colour = colour
        self.rent = rent
        self.owner = ''
        self.mortgaged = False
        self.image = image


class Dice:
    def __init__(self):
        self.number = random.randint(1, 6)
        if self.number == 1:
            self.image = pygame.image.load('graphics/dice_1.png')
        elif self.number == 2:
            self.image = pygame.image.load('graphics/dice_2.png')
        elif self.number == 3:
            self.image = pygame.image.load('graphics/dice_3.png')
        elif self.number == 4:
            self.image = pygame.image.load('graphics/dice_4.png')
        elif self.number == 5:
            self.image = pygame.image.load('graphics/dice_5.png')
        elif self.number == 6:
            self.image = pygame.image.load('graphics/dice_6.png')


class Game:
    def __init__(self, players):
        self.players = players

    def main(self):
        # Initialise pygame
        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Property Tycoon")

        # CREATE BOARD SECTIONS

        # NON INTERACTIVE PIECES
        centre = pygame.Surface((630, 630))
        centre.fill('White')
        # Text
        title_font = pygame.font.Font('fonts/monoton.ttf', 45)
        centre_text = title_font.render('Property     Tycoon', True, 'Black')
        centre_text_rect = centre_text.get_rect(center=(455, 455))
        # Card Stacks
        opportunityCards = pygame.image.load('graphics/opportunitycards.png')
        potluckCards = pygame.image.load('graphics/potluckcards.png')

        # Updates and displays player pieces
        def blit_players():
            for player in self.players.values():
                screen.blit(player.image, player.position)
            pygame.display.update()

        # Updates and displays the static game board 60 times a second
        def blit_board():
            # place corners
            screen.blit(centre, (140, 140))
            for tile in corners.values():
                screen.blit(tile.image, tile.position)
            # place title text
            screen.blit(centre_text, centre_text_rect)
            # place card stacks
            for tile in card_spaces.values():
                screen.blit(tile.image, tile.position)
            # place tax tiles
            for tile in taxes.values():
                screen.blit(tile.image, tile.position)
            # place tax pieces
            for tile in properties.values():
                screen.blit(tile.image, tile.position)
            pygame.display.update()

        def update_board():
            blit_board()
            blit_players()

        # turn function displays a prompt popup, how do I make the prompt disappear after keypress?
        def turn():
            popup = pygame.image.load('graphics/turn start.png')
            screen.blit(popup, (250, 350))
            pygame.display.update()

        def roll():
            dice1 = Dice()
            dice2 = Dice()
            screen.blit(dice1.image, (340, 550))
            screen.blit(dice2.image, (455, 550))
            pygame.display.update()
            return dice1.number + dice2.number

        run = True
        update_board()
        turn()

        player_names = []
        for name in players.keys():
            player_names.append(name)
        current_player_num = 0
        turn_state = "start"

        potLuck = CardStack("Pot Luck")
        opportunityKnocks = CardStack("Opportunity Knocks")
        potLuck.shuffle()
        opportunityKnocks.shuffle()

        while run:
            current_player = players.get(player_names[current_player_num])

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE] and turn_state == "start":
                    dice_results = roll()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE and turn_state == "start":
                        current_player.move_x(dice_results)
                        turn_state = "moved"
                        update_board()

                    elif event.key == pygame.K_SPACE and turn_state == "space action":
                        current_player_num += 1
                        if current_player_num == 5:
                            current_player_num = 0
                        print("Current Player: ", current_player_num)
                        update_board()
                        turn_state = "start"
                """
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                """
            # draw & update
            clock.tick(60)

            # check if player has landed on card space
            if turn_state == "moved":
                for space in card_spaces:
                    if card_spaces[space].position == current_player.position:
                        if "opportunity" in space:
                            card_img = current_player.draw_card(opportunityKnocks)
                        elif "potluck" in space:
                            card_img = current_player.draw_card(potLuck)

                        screen.blit(card_img, (278, 366))
                        pygame.display.update()

                turn_state = "space action"


# Global Board Information

# Corners
corners = {
    'free_parking': Tile((0, 0), pygame.image.load('graphics/free_parking.png')),
    'go': Tile((770, 770), pygame.image.load('graphics/go.png')),
    'go_to_jail': Tile((770, 0), pygame.image.load('graphics/go_to_jail.png')),
    'jail': Tile((0, 770), pygame.image.load('graphics/jail.png'))
}

# Tax spaces
taxes = {
    'supertax': Tile((770, 630), pygame.image.load('graphics/supertax.png')),
    'incometax': Tile((490, 770), pygame.image.load('graphics/incometax.png'))
}

# Card Spaces on Board
card_spaces = {
    'opportunity1': Tile((770, 490), pygame.image.load('graphics/opportunityH.png')),
    'opportunity2': Tile((210, 0), pygame.image.load('graphics/opportunityV.png')),
    'opportunity3': Tile((280, 770), pygame.image.load('graphics/opportunityV.png')),
    'potluck1': Tile((0, 280), pygame.image.load('graphics/potluckH.png')),
    'potluck2': Tile((770, 280), pygame.image.load('graphics/potluckH.png')),
    'potluck3': Tile((630, 770), pygame.image.load('graphics/potluckV.png'))
}

# PROPERTIES (PRICE, POSITION, GROUP, RENT, IMAGE)
properties = {
    'brighton': Property(200, (420, 770), 'station', 25, pygame.image.load('graphics/brighton.png')),
    'falmer': Property(200, (420, 0), 'station', 25, pygame.image.load('graphics/falmer.png')),
    'portslade': Property(200, (770, 420), 'station', 25, pygame.image.load('graphics/portslade.png')),
    'hove': Property(200, (0, 420), 'station', 25, pygame.image.load('graphics/hove.png')),
    'edison': Property(150, (630, 0), 'utility', 0, pygame.image.load('graphics/edison.png')),
    'tesla': Property(150, (0, 630), 'utility', 0, pygame.image.load('graphics/tesla.png')),
    'broyles': Property(200, (0, 140), 'orange', 16, pygame.image.load('graphics/broyles.png')),
    'dunham': Property(180, (0, 210), 'orange', 14, pygame.image.load('graphics/dunham.png')),
    'bishop': Property(180, (0, 350), 'orange', 14, pygame.image.load('graphics/bishop.png')),
    'rey': Property(160, (0, 490), 'purple', 12, pygame.image.load('graphics/rey.png')),
    'wookie': Property(140, (0, 560), 'purple', 10, pygame.image.load('graphics/wookie.png')),
    'skywalker': Property(140, (0, 700), 'purple', 10, pygame.image.load('graphics/skywalker.png')),
    'hanxin': Property(240, (350, 0), 'red', 20, pygame.image.load('graphics/hanxin.png')),
    'mulan': Property(220, (280, 0), 'red', 18, pygame.image.load('graphics/mulan.png')),
    'yuefei': Property(220, (140, 0), 'red', 18, pygame.image.load('graphics/yuefei.png')),
    'crusher': Property(280, (700, 0), 'yellow', 22, pygame.image.load('graphics/crusher.png')),
    'picard': Property(260, (560, 0), 'yellow', 22, pygame.image.load('graphics/picard.png')),
    'shatner': Property(260, (490, 0), 'yellow', 22, pygame.image.load('graphics/shatner.png')),
    'ibis': Property(320, (770, 350), 'green', 28, pygame.image.load('graphics/ibis.png')),
    'ghengis': Property(300, (770, 210), 'green', 26, pygame.image.load('graphics/ghengis.png')),
    'sirat': Property(300, (770, 140), 'green', 26, pygame.image.load('graphics/sirat.png')),
    'turing': Property(400, (770, 700), 'dark blue', 50, pygame.image.load('graphics/turing.png')),
    'james': Property(350, (770, 560), 'dark blue', 35, pygame.image.load('graphics/james.png')),
    'gangsters': Property(60, (560, 770), 'brown', 4, pygame.image.load('graphics/gangsters.png')),
    'creek': Property(60, (700, 770), 'brown', 2, pygame.image.load('graphics/creek.png')),
    'granger': Property(120, (140, 770), 'light blue', 8, pygame.image.load('graphics/granger.png')),
    'potter': Property(100, (210, 770), 'light blue', 6, pygame.image.load('graphics/potter.png')),
    'angels': Property(100, (350, 770), 'light blue', 6, pygame.image.load('graphics/angels.png'))
}

# Get list of all tile positions to help move players around
tiles = [(770, 770), (770, 700), (770, 630), (770, 560), (770, 490), (770, 420), (770, 350), (770, 280),
         (770, 210), (770, 140), (770, 0), (700, 0), (630, 0), (560, 0), (490, 0), (350, 0), (280, 0), (210, 0),
         (140, 0), (0, 0), (0, 140), (0, 210), (0, 280), (0, 350), (0, 420), (0, 490), (0, 490), (0, 560),
         (0, 630), (0, 700), (0, 770), (140, 770), (210, 770), (280, 770), (350, 770), (420, 770), (490, 770),
         (560, 770), (630, 770), (700, 770), (770, 770)]

# This if statement makes it so that when running the test suite, the game does not launch
if __name__ == '__main__':
    players = {
        'Dan': Player('iron'),
        'Mario': Player('cat'),
        'Luigi': Player('boot'),
        'Wario': Player('hatstand'),
        'Waluigi': Player('smartphone')
    }
    game = Game(players)
    game.main()
