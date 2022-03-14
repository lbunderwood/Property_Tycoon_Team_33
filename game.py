import numpy
import pygame
import ctypes
import os
import random
import csv
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
        if self.shape == 'boot':
            self.position = (790, 790)
            self.image = pygame.image.load('graphics/boot.png')
        elif self.shape == 'ship':
            self.position = (860, 790)
            self.image = pygame.image.load('graphics/ship.png')
        elif self.shape == 'hatstand':
            self.position = (860, 835)
            self.image = pygame.image.load('graphics/hatstand.png')
        elif self.shape == 'smartphone':
            self.position = (790, 870)
            self.image = pygame.image.load('graphics/smartphone.png')
        elif self.shape == 'cat':
            self.position = (860, 870)
            self.image = pygame.image.load('graphics/cat.png')
        elif self.shape == 'iron':
            self.position = (790, 835)
            self.image = pygame.image.load('graphics/iron.png')
        else:
            print("\nNot a valid player shape, check player info")
            pygame.quit()
            exit()
    # def move(self):

    def draw_card(self, stack):
        card = stack.draw()

        if card == "Bank pays you divided of £50":
            self.balance += 50
        elif card == "You have won a lip sync battle. Collect £100":
            self.balance += 100
        elif card == "Advance to Turing Heights":
            # TODO: add movement
            pass
        elif card == "Advance to Han Xin Gardens. If you pass GO, collect £200":
            # TODO: add movement
            pass
        elif card == "Fined £15 for speeding":
            self.balance -= 15
            # TODO: add payment to free parking
        elif card == "Pay university fees of £150":
            self.balance -= 150
        elif card == "Take a trip to Hove station. If you pass GO collect £200":
            # TODO: add movement
            pass
        elif card == "Loan matures, collect £150":
            self.balance += 150
        elif card == "You are assessed for repairs, £40/house, £115/hotel":
            # TODO: add calculation, property class needs houses/hotels
            pass
        elif card == "Advance to GO":
            # TODO: add movement
            pass
        elif card == "You are assessed for repairs, £25/house, £100/hotel":
            # TODO: add calculation, property class needs houses/hotels
            pass
        elif card == "Go back 3 spaces":
            # TODO: add movement
            pass
        elif card == "Advance to Skywalker Drive. If you pass GO collect £200":
            # TODO: add movement
            pass
        elif card == "Go to jail. Do not pass GO, do not collect £200":
            # TODO: add movement (and jail)
            pass
        elif card == "Drunk in charge of a hoverboard. Fine £30":
            self.balance -= 30
            # TODO: add payment to free parking
        elif card == "Get out of jail free":
            # TODO: add get out of jail free
            pass
        elif card == "You inherit £200":
            self.balance += 200
        elif card == "You have won 2nd prize in a beauty contest, collect £50":
            self.balance += 50
        elif card == "You are up the creek with no paddle - go back to the Old Creek":
            # TODO: add movement
            pass
        elif card == "Student loan refund. Collect £20":
            self.balance += 20
        elif card == "Bank error in your favour. Collect £200":
            self.balance += 200
        elif card == "Pay bill for text books of £100":
            self.balance -= 100
        elif card == "Mega late night taxi bill pay £50":
            self.balance -= 50
        elif card == "Advance to go":
            # TODO: add movement
            pass
        elif card == "From sale of Bitcoin you get £50":
            self.balance += 50
        elif card == "Bitcoin assets fall - pay off Bitcoin short fall":
            self.balance -= 50
        elif card == "Pay a £10 fine or take opportunity knocks":
            # TODO: add interface for decision
            # the tenner goes to free parking
            pass
        elif card == "Pay insurance fee of £50":
            self.balance -= 50
            # TODO: add payment to free parking
        elif card == "Savings bond matures, collect £100":
            self.balance += 100
        elif card == "Go to jail. Do not pass GO, do not collect £200":
            # TODO: add movement
            pass
        elif card == "Received interest on shares of £25":
            self.balance += 25
        elif card == "It's your birthday. Collect £10 from each player":
            # TODO: add deduction from other players and way of knowing how many players
            player_count = 4
            self.balance += 10 * player_count
            pass
        else:
            print("\nInvalid card description passed to Player.draw_card()")
            pygame.quit()
            exit()

# for now, we will simply use strings as only the description is needed
#class Card:
#    def __init__(self, description):
#        self.description = description


class CardStack:
    def __init__(self, card_type):
        if card_type == "Opportunity Knocks":
            self.cards = numpy.genfromtxt("cards/Opportunity_Knocks.txt", dtype=str, delimiter=';')
            self.type = card_type
        elif card_type == "Pot Luck":
            self.cards = numpy.genfromtxt("cards/Pot_Luck.txt", dtype=str, delimiter=';')
            self.type = card_type
        else:
            print("\nInvalid card type given to CardStack")
            pygame.quit()
            exit()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        card = self.cards[0]
        self.cards = numpy.roll(self.cards, -1)
        return card


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
    def roll(self):
        return random.randint(1, 6)


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

        # Player pieces
        smartphone = pygame.image.load('graphics/smartphone.png')
        hatstand = pygame.image.load('graphics/hatstand.png')
        ship = pygame.image.load('graphics/ship.png')
        iron = pygame.image.load('graphics/iron.png')
        cat = pygame.image.load('graphics/cat.png')

        # Corners
        free_parking = pygame.image.load('graphics/free_parking.png')
        go = pygame.image.load('graphics/go.png')
        go_to_jail = pygame.image.load('graphics/go_to_jail.png')
        jail = pygame.image.load('graphics/jail.png')

        # Tax Spaces
        supertax = pygame.image.load('graphics/supertax.png')
        incometax = pygame.image.load('graphics/incometax.png')

        # Card Spaces on Board
        opportunityH = pygame.image.load('graphics/opportunityH.png')
        opportunityV = pygame.image.load('graphics/opportunityV.png')
        potluckH = pygame.image.load('graphics/potluckH.png')
        potluckV = pygame.image.load('graphics/potluckV.png')

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

        # turn function displays a prompt popup, how do I make the prompt disappear after keypress?
        def turn():
            popup = pygame.Surface((500, 200))
            popup.fill('Black')
            screen.blit(popup, (205, 350))
            popup_font = pygame.font.Font(None, 30)
            popup_text = popup_font.render('Roll Dice ----> SPACE', True, 'White')
            popup_text_rect = popup_text.get_rect(center=(455, 400))
            screen.blit(popup_text, popup_text_rect)
            pygame.display.update()

        def move_player(player, property):
            player.position = property.position

        # Updates and displays player pieces
        def blit_players():
            for player in self.players:
                screen.blit(player.image, player.position)

        # Updates and displays the static game board 60 times a second
        def blit_board():
            # place corners
            screen.blit(free_parking, (0, 0))
            screen.blit(go, (770, 770))
            screen.blit(go_to_jail, (770, 0))
            screen.blit(jail, (0, 770))
            screen.blit(centre, (140, 140))
            # place title text
            screen.blit(centre_text, centre_text_rect)
            # place card stacks
            screen.blit(opportunityCards, (150, 140))
            screen.blit(potluckCards, (540, 550))
            # place card action places
            screen.blit(opportunityH, (770, 490))
            screen.blit(opportunityV, (210, 0))
            screen.blit(opportunityV, (280, 770))
            screen.blit(potluckH, (0, 280))
            screen.blit(potluckH, (770, 280))
            screen.blit(potluckV, (630, 770))
            # place tax pieces
            screen.blit(incometax, (490, 770))
            screen.blit(supertax, (770, 630))
            for item in properties.values():
                screen.blit(item.image, item.position)

        run = True
        blit_board()
        pygame.display.update()
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        print('Space')
                        #turn()
                        move_player(players.get('Mario'), properties.get('wookie'))
                        blit_players()
                        pygame.display.update()
                # draw & update
                #clock.tick(10)


# This if statement makes it so that when running the test suite, the game does not launch
if __name__ == '__main__':
    players = {
        'Dan': Player('iron'),
        'Mario': Player('cat'),
        'Luigi': Player('boot'),
        'Wario': Player('hatstand'),
        'Waluigi': Player('smartphone')
    }
    game = Game(players.values())
    game.main()
