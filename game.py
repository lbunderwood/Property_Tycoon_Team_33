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

def error(msg):
    print("\n"+msg)
    pygame.quit()
    exit()

class Player:
    def __init__(self, shape):
        self.balance = 1500
        self.properties = []
        self.shape = shape
        self.index = 0
        self.in_jail = False
        self.free_jail_card = 0
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
            error("Not a valid player shape, check player info")

    # takes card stack as input, draws card, applies result of card, and returns pygame image object
    def draw_card(self, stack, player_count):
        card = stack.draw()
        card_image = "VAR INIT"
        fp_money = 0
        further_action = ""

        if card == "Bank pays you divided of £50":
            self.balance += 50
            card_image = pygame.image.load('graphics/opportunity knocks 1.png')
        elif card == "You have won a lip sync battle. Collect £100":
            self.balance += 100
            card_image = pygame.image.load('graphics/opportunity knocks 2.png')
        elif card == "Advance to Turing Heights":
            self.move_to('turing')
            card_image = pygame.image.load('graphics/opportunity knocks 3.png')
        elif card == "Advance to Han Xin Gardens. If you pass GO, collect £200":
            self.move_to('hanxin')
            card_image = pygame.image.load('graphics/opportunity knocks 3(1).png')
        elif card == "Fined £15 for speeding":
            self.balance -= 15
            fp_money = 15
            card_image = pygame.image.load('graphics/opportunity knocks 4.png')
        elif card == "Pay university fees of £150":
            self.balance -= 150
            card_image = pygame.image.load('graphics/opportunity knocks 5.png')
        elif card == "Take a trip to Hove station. If you pass GO collect £200":
            self.move_to('hove')
            card_image = pygame.image.load('graphics/opportunity knocks 6.png')
        elif card == "Loan matures, collect £150":
            self.balance += 150
            card_image = pygame.image.load('graphics/opportunity knocks 7.png')
        elif card == "You are assessed for repairs, £40/house, £115/hotel":
            for prop in self.properties:
                if prop.upgrade < 5:
                    self.balance -= prop.upgrade*40
                elif prop.upgrade == 5:
                    self.balance -= 115
            card_image = pygame.image.load('graphics/opportunity knocks 8.png')
        elif card == "Advance to GO":
            self.move_to('go')
            if stack.type == "Opportunity Knocks":
                card_image = pygame.image.load('graphics/opportunity knocks 9.png')
            else:
                card_image = pygame.image.load('graphics/pot luck 8.png')
        elif card == "You are assessed for repairs, £25/house, £100/hotel":
            for prop in self.properties:
                if prop.upgrade < 5:
                    self.balance -= prop.upgrade * 25
                elif prop.upgrade == 5:
                    self.balance -= 100
            card_image = pygame.image.load('graphics/opportunity knocks 10.png')
        elif card == "Go back 3 spaces":
            self.move_x(-3)
            card_image = pygame.image.load('graphics/opportunity knocks 11.png')
        elif card == "Advance to Skywalker Drive. If you pass GO collect £200":
            self.move_to('skywalker')
            card_image = pygame.image.load('graphics/opportunity knocks 12.png')
        elif card == "Go to jail. Do not pass GO, do not collect £200":
            self.go_to_jail()
            if stack.type == "Opportunity Knocks":
                card_image = pygame.image.load('graphics/opportunity knocks 13.png')
            else:
                card_image = pygame.image.load('graphics/pot luck 14.png')
        elif card == "Drunk in charge of a hoverboard. Fine £30":
            self.balance -= 30
            fp_money = 30
            card_image = pygame.image.load('graphics/opportunity knocks 14.png')
        elif card == "Get out of jail free":
            self.free_jail_card += 1
            stack.remove_card()
            if stack.type == "Opportunity Knocks":
                card_image = pygame.image.load('graphics/opportunity knocks 15.png')
            else:
                card_image = pygame.image.load('graphics/pot luck 17.png')
        elif card == "You inherit £200":
            self.balance += 200
            card_image = pygame.image.load('graphics/pot luck 1.png')
        elif card == "You have won 2nd prize in a beauty contest, collect £50":
            self.balance += 50
            card_image = pygame.image.load('graphics/pot luck 2.png')
        elif card == "You are up the creek with no paddle - go back to the Old Creek":
            self.move_to('creek', pass_go=False)
            card_image = pygame.image.load('graphics/pot luck 3.png')
        elif card == "Student loan refund. Collect £20":
            self.balance += 20
            card_image = pygame.image.load('graphics/pot luck 4.png')
        elif card == "Bank error in your favour. Collect £200":
            self.balance += 200
            card_image = pygame.image.load('graphics/pot luck 5.png')
        elif card == "Pay bill for text books of £100":
            self.balance -= 100
            card_image = pygame.image.load('graphics/pot luck 6.png')
        elif card == "Mega late night taxi bill pay £50":
            self.balance -= 50
            card_image = pygame.image.load('graphics/pot luck 7.png')
        elif card == "From sale of Bitcoin you get £50":
            self.balance += 50
            card_image = pygame.image.load('graphics/pot luck 9.png')
        elif card == "Bitcoin assets fall - pay off Bitcoin short fall":
            self.balance -= 50
            card_image = pygame.image.load('graphics/pot luck 10.png')
        elif card == "Pay a £10 fine or take opportunity knocks":
            further_action = "decision"
            card_image = pygame.image.load('graphics/pot luck 11.png')
        elif card == "Pay insurance fee of £50":
            self.balance -= 50
            card_image = pygame.image.load('graphics/pot luck 12.png')
        elif card == "Savings bond matures, collect £100":
            self.balance += 100
            fp_money = 50
            card_image = pygame.image.load('graphics/pot luck 13.png')
        elif card == "Received interest on shares of £25":
            self.balance += 25
            card_image = pygame.image.load('graphics/pot luck 15.png')
        elif card == "It's your birthday. Collect £10 from each player":
            further_action = "birthday"
            self.balance += 10 * (player_count - 1)
            card_image = pygame.image.load('graphics/pot luck 16.png')
        else:
            error("Invalid card description \"" + card + "\" passed to Player.draw_card()")

        return card_image, fp_money, further_action

    # moves player by number of spaces given by spaces
    # pass_go is an optional parameter that should be set to false when moving to jail, etc
    def move_x(self, spaces, pass_go=True):

        destination_index = self.index + spaces

        if destination_index > len(tiles) - 1:
            destination_index -= len(tiles) - 1
            if pass_go:
                self.balance += 200
        elif destination_index < 0:
            destination_index += len(tiles) - 1

        self.index = destination_index
        print('Moved', spaces, 'spaces to tile n#: ', destination_index)

    # moves player to a space given as a string
    # pass_go is an optional parameter that should be set to false when moving to jail, etc
    def move_to(self, space, pass_go=True):
        if space in properties:
            destination = properties[space]
        elif space in card_spaces:
            destination = card_spaces[space]
        elif space in taxes:
            destination = taxes[space]
        elif space in corners:
            destination = corners[space]
        else:
            error("Invalid space \"" + space + "\" passed to Player.move_to()")

        # calculate number of spaces to move and hand off to move_x
        # this is to follow the Single Responsibility Principle
        # and also makes sure we check if we passed GO
        current = self.index
        destination_index = tiles.index(destination)
        self.move_x(destination_index - current, pass_go)

    def go_to_jail(self):
        self.move_to('jail', pass_go=False)
        self.in_jail = True

    def get_out_jail(self):
        self.in_jail = False


class CardStack:
    def __init__(self, card_type):
        if not (card_type == "Opportunity Knocks" or card_type == "Pot Luck"):
            error("\nInvalid card type \"" + card_type + "\" given to CardStack")

        rawCards = numpy.genfromtxt("cards/" + card_type.replace(' ', '_') + ".txt", dtype=str, delimiter=';')
        self.cards = rawCards[0:, 0]
        self.type = card_type

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        card = self.cards[0]
        self.cards = numpy.roll(self.cards, -1)
        return card

    # intended for use directly after draw() to remove the last card drawn
    # only use for removing get out of jail free card
    def remove_card(self):
        self.cards = self.cards[:-1]

    # adds a get out of jail free card to the bottom of the deck
    def return_card(self):
        self.cards = numpy.append(self.cards, "Get out of jail free")


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
        self.image = image

        # defaults not initialised
        self.owner = 'bank'
        self.mortgaged = False

        # indicates # of houses, hotel = 5
        self.upgrade = 0


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
        prompt_font = pygame.font.Font('fonts/Cinzel-SemiBold.ttf', 20)
        title_font = pygame.font.Font('fonts/monoton.ttf', 45)
        centre_text = title_font.render('Property     Tycoon', True, 'Black')
        centre_text_rect = centre_text.get_rect(center=(455, 455))
        # Card Stacks IMAGE ONLY NOT FUNCTIONAL 'STACK'
        opportunityCards = pygame.image.load('graphics/opportunitycards.png')
        potluckCards = pygame.image.load('graphics/potluckcards.png')

        # Updates and displays player pieces
        def blit_players():
            for player in self.players.values():
                currently_on = tiles[player.index]
                coord = currently_on.position
                if player.in_jail:
                    coord = (coord[0] + 35, coord[1])
                screen.blit(player.image, coord)
            pygame.display.update()

        # Updates and displays the entire static game board WITHOUT PLAYER PIECES
        def blit_board():
            # place corners
            screen.blit(centre, (140, 140))
            screen.blit(opportunityCards, (539, 549))
            screen.blit(potluckCards, (150, 140))
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

        # turn function displays a prompt popup
        def turn_start_popup():
            popup = pygame.image.load('graphics/turn start.png')
            screen.blit(popup, (235, 350))
            pygame.display.update()

        def display_prompt(prompt_str, height=560):
            prompt_text = prompt_font.render(prompt_str, True, 'Black')
            prompt_text_rect = prompt_text.get_rect(center=(455, height))
            screen.blit(prompt_text, prompt_text_rect)
            pygame.display.update()

        def turn_end_popup():
            # popup = pygame.image.load('graphics/turn_end.png')
            # screen.blit(popup, (205, 350))
            display_prompt('Press SPACE to end your turn')

        def roll():
            dice1 = Dice()
            dice2 = Dice()
            screen.blit(dice1.image, (340, 550))
            screen.blit(dice2.image, (455, 550))
            pygame.display.update()
            return dice1, dice2

        run = True
        update_board()
        turn_start_popup()

        player_names = []
        for name in players.keys():
            player_names.append(name)
        current_player_num = 0
        turn_state = "start"

        pot_luck = CardStack("Pot Luck")
        opportunity_knocks = CardStack("Opportunity Knocks")
        pot_luck.shuffle()
        opportunity_knocks.shuffle()

        free_parking = 0

        def draw_card(draw_player, card_stack):
            old_idx = draw_player.index
            card_img, fp, further_action = draw_player.draw_card(card_stack, len(self.players))
            screen.blit(card_img, (278, 366))
            pygame.display.update()

            if further_action == "birthday":
                for p_name in players:
                    player = players[p_name]
                    if player != current_player:
                        player.balance -= 10

            if old_idx != current_player.index:
                display_prompt('Press SPACE to move')
                new_state = 'card'
            elif further_action == "decision":
                display_prompt('Would you like to draw an Opportunity Knocks card?')
                display_prompt('Press Y or N', height=610)
                new_state = "decision card"
            else:
                new_state = "end"
                turn_end_popup()

            return new_state, fp

        while run:

            current_player = players.get(player_names[current_player_num])

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE] and turn_state == "start":
                    dice = roll()
                    print('Rolling...')
                    total = dice[0].number + dice[1].number

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE and turn_state == "start":
                        print("Current Player: ", players.get(player_names[current_player_num]).shape)
                        in_jail = current_player.in_jail
                        if not in_jail:
                            current_player.move_x(total)
                        turn_state = "moved"
                        update_board()

                    elif event.key == pygame.K_SPACE and turn_state == "reset":
                        print('Next Turn!')
                        current_player_num += 1
                        if current_player_num == 5:
                            current_player_num = 0
                        turn_state = "start"
                        update_board()
                        turn_start_popup()

                    elif event.key == pygame.K_SPACE and turn_state == "card":
                        turn_state = 'moved'
                        update_board()

                    elif event.key == pygame.K_y and turn_state == "decision card":
                        turn_state, fp_money = draw_card(current_player, opportunity_knocks)
                        free_parking += fp_money
                        if turn_state == "end":
                            turn_end_popup()

                    elif event.key == pygame.K_n and turn_state == "decision card":
                        current_player.balance -= 10
                        free_parking += 10
                        turn_state = "end"
                        update_board()
                        turn_end_popup()

                    elif event.key == pygame.K_y and turn_state == "buy":
                        print('Property Bought!')
                        prop = tiles[current_player.index]
                        current_player.balance -= prop.price
                        current_player.properties.append(prop)
                        update_board()
                        turn_state = "end"
                        turn_end_popup()

                    elif event.key == pygame.K_n and turn_state == "buy":
                        print('Player passed on property')
                        # auction goes here
                        update_board()
                        turn_state = "end"
                        turn_end_popup()

            # perform the action associated with the space the player landed on
            if turn_state == "moved":
                # card spaces
                for space in card_spaces:
                    if tiles[current_player.index] == card_spaces[space]:
                        if "opportunity" in space:
                            turn_state, fp_money = draw_card(current_player, opportunity_knocks)
                        elif "potluck" in space:
                            turn_state, fp_money = draw_card(current_player, pot_luck)
                        else:
                            error("Invalid card space name used")
                        free_parking += fp_money

                if turn_state != 'moved':
                    continue
                '''
                corner spaces 
                ADDED COLLISION DETECTION FOR PLAYER OVERLAP FIX:
                essentially works by getting a rectangle of each image + coords, then doing a collision detection 
                method built into pygame, believe me there is no easier way
                
                player_location = tiles[current_player.index].position
                jail_location = corners['go_to_jail'].position
                parking_location = corners['free_parking'].position

                player_rect = current_player.image.get_rect(topleft=player_location)
                parking_rect = corners['free_parking'].image.get_rect(topleft=parking_location)
                jail_rect = corners['go_to_jail'].image.get_rect(topleft=jail_location)
    
                if player_rect.colliderect(jail_rect):
                    current_player.go_to_jail()
                    update_board()
                    turn_state = 'end'
                elif player_rect.colliderect(parking_rect):
                    current_player.balance += free_parking
                    free_parking = 0
                    turn_state = 'end'
                    '''
                for space in corners:
                    if tiles[current_player.index] == corners[space]:
                        if space == "go_to_jail":
                            current_player.go_to_jail()
                            update_board()
                        elif space == "free_parking":
                            current_player.balance += free_parking
                            free_parking = 0
                        turn_state = 'end'

                if turn_state != 'moved':
                    continue

                for space in taxes:
                    if tiles[current_player.index] == taxes[space]:
                        # add tax space functionality here
                        turn_state = 'end'

                if turn_state != 'moved':
                    continue

                # property tiles
                for space in properties:
                    prop = properties[space]
                    if tiles[current_player.index] == prop:
                        if prop.owner == 'bank':
                            try:
                                deed = pygame.image.load("graphics/deed_"+space+".png")
                            except Exception:
                                error("There is no deed graphic for "+space)
                            screen.blit(deed, (330, 150))
                            display_prompt('Would you like to purchase this property?')
                            display_prompt('Press Y or N', height=610)
                            turn_state = "buy"
                            break
                        elif prop.owner != current_player.shape:
                            current_player.balance -= prop.rent
                            prop.owner.balance += prop.rent
                        turn_state = 'end'
                        break

            if turn_state == 'end':
                turn_end_popup()
                turn_state = 'reset'

        # draw & update
        clock.tick(60)


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
tiles_old = [(770, 770), (700, 770), (630, 770), (560, 770), (490, 770), (420, 770), (350, 770), (280, 770),
             (210, 770), (140, 770), (0, 770), (0, 700), (0, 630), (0, 560), (0, 490), (0, 490), (0, 420), (0, 350),
             (0, 280), (0, 210), (0, 140), (0, 0), (140, 0), (210, 0), (280, 0), (350, 0), (490, 0), (560, 0),
             (630, 0), (700, 0), (770, 0), (770, 140), (770, 210), (770, 280), (770, 350), (770, 420), (770, 490),
             (770, 560), (770, 630), (770, 700)]

tiles = [corners['go'], properties['creek'], card_spaces['potluck3'], properties['gangsters'], taxes['incometax'],
         properties['brighton'], properties['angels'], card_spaces['opportunity3'], properties['potter'],
         properties['granger'], corners['jail'], properties['skywalker'], properties['tesla'], properties['wookie'],
         properties['rey'], properties['hove'], properties['bishop'], card_spaces['potluck1'], properties['dunham'],
         properties['broyles'], corners['free_parking'], properties['yuefei'], card_spaces['opportunity2'],
         properties['mulan'], properties['hanxin'], properties['falmer'], properties['shatner'], properties['picard'],
         properties['edison'], properties['crusher'], corners['go_to_jail'], properties['sirat'],
         properties['ghengis'], card_spaces['potluck2'], properties['ibis'], properties['portslade'],
         card_spaces['opportunity1'], properties['james'], taxes['supertax'], properties['turing']]


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
