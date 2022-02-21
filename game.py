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
    def __init__(self, name, balance, shape):
        self.name = name
        self.balance = balance
        self.properties = {}
        self.shape = shape
        try:
            if self.shape == 'Boot':
                self.position = (790, 790)
            elif self.shape == 'Ship':
                self.position = (860, 790)
            elif self.shape == 'Hatstand':
                self.position = (860, 860)
            elif self.shape == 'Smartphone':
                self.position = (790, 860)
            elif self.shape == 'Cat':
                self.position = (835, 835)
        except ValueError:
            print("Not a valid player shape, redefine player")


class Card:
    def __init__(self, card_type, description):
        self.card_type = card_type
        self.description = description


class Property:
    def __init__(self, name, price, position, colour, rent):
        self.name = name
        self.price = price
        self.position = position
        self.colour = colour
        self.rent = rent
        self.owner = ''
        self.rent = 0
        self.mortgaged = False


class Dice:
    def roll(self):
        return random.randint(1, 6)

class Game:
    def __init__(self, player_count):
        self.player_count = player_count

    def main(self):
        # Initialise pygame
        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Property Tycoon")

        # CREATE BOARD SECTIONS
        centre = pygame.Surface((630, 630))
        centre.fill('White')

        # Text
        title_font = pygame.font.Font('fonts/monoton.ttf', 50)
        title_text = title_font.render('Property Tycoon', True, 'Black')
        title_text_rect = title_text.get_rect(center=(455, 455))

        # Player pieces
        boot_player = Player('Dan', 1500, 'Boot')
        boot = pygame.image.load('graphics/boot.png')
        #smartphone
        #hatstand
        #ship
        #iron
        #cat

        # Corners
        free_parking = pygame.Surface((140, 140))
        free_parking.fill('White')
        go = pygame.image.load('graphics/go.png')
        go_to_jail = pygame.Surface((140, 140))
        go_to_jail.fill('White')
        jail = pygame.image.load('graphics/jail.png')

        # Oranges
        broyles = pygame.Surface((140, 70))
        dunham = pygame.Surface((140, 70))
        bishop = pygame.Surface((140, 70))
        broyles.fill('Orange')
        dunham.fill('Orange')
        bishop.fill('Orange')

        # Purples
        rey = pygame.image.load('graphics/rey.png')
        wookie = pygame.image.load('graphics/wookie.png')
        skywalker = pygame.image.load('graphics/skywalker.png')

        # Reds
        hanxin = pygame.Surface((70, 140))
        mulan = pygame.Surface((70, 140))
        yuefei = pygame.Surface((70, 140))
        hanxin.fill('Red')
        mulan.fill('Red')
        yuefei.fill('Red')

        # Yellows
        crusher = pygame.Surface((70, 140))
        picard = pygame.Surface((70, 140))
        shatner = pygame.Surface((70, 140))
        crusher.fill('Yellow')
        picard.fill('Yellow')
        shatner.fill('Yellow')

        # Greens
        ibis = pygame.Surface((140, 70))
        ghengis = pygame.Surface((140, 70))
        sirat = pygame.Surface((140, 70))
        ibis.fill('Green')
        ghengis.fill('Green')
        sirat.fill('Green')

        # Dark Blues
        turing = pygame.Surface((140, 70))
        james = pygame.Surface((140, 70))
        turing.fill((43, 54, 255))
        james.fill((43, 54, 255))

        # Browns
        gangsters = pygame.Surface((70, 140))
        creek = pygame.Surface((70, 140))
        gangsters.fill((210, 146, 106))
        creek.fill((210, 146, 106))

        # Light Blues
        granger = pygame.Surface((70, 140))
        potter = pygame.Surface((70, 140))
        angel = pygame.Surface((70, 140))
        granger.fill((43, 199, 255))
        potter.fill((43, 199, 255))
        angel.fill((43, 199, 255))

        # Updates and displays player pieces
        def blit_players():
            # place player pieces
            screen.blit(boot, boot_player.position)

        # Updates and displays the game board 60 times a second
        def blit_board():

            # place corners
            screen.blit(free_parking, (0, 0))
            screen.blit(go, (770, 770))
            screen.blit(go_to_jail, (770, 0))
            screen.blit(jail, (0, 770))
            screen.blit(centre, (140, 140))

            # place title text
            screen.blit(title_text, title_text_rect)

            # place location pieces
            # place reds
            screen.blit(yuefei, (140, 0))
            screen.blit(mulan, (280, 0))
            screen.blit(hanxin, (350, 0))
            # place yellows
            screen.blit(shatner, (490, 0))
            screen.blit(picard, (560, 0))
            screen.blit(crusher, (700, 0))
            # place greens
            screen.blit(sirat, (770, 140))
            screen.blit(ghengis, (770, 210))
            screen.blit(ibis, (770, 350))
            # place dark blues
            screen.blit(james, (770, 490))
            screen.blit(turing, (770, 630))
            # place light blues
            screen.blit(granger, (140, 770))
            screen.blit(potter, (210, 770))
            screen.blit(angel, (350, 770))
            # place browns
            screen.blit(gangsters, (560, 770))
            screen.blit(creek, (700, 770))
            # place oranges
            screen.blit(broyles, (0, 140))
            screen.blit(dunham, (0, 210))
            screen.blit(bishop, (0, 350))
            # place purples
            screen.blit(rey, (0, 490))
            screen.blit(wookie, (0, 560))
            screen.blit(skywalker, (0, 700))


        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            blit_board()
            blit_players()
            keys = pygame.key.get_pressed()

            # draw & update
            pygame.display.update()
            clock.tick(60)



game = Game(1)
game.main()
