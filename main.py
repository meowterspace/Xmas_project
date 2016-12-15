"""
==================================================
Xmas Code project
Written by Cat.
Graphics by Paul, Ryan & Sean.
Team supervisor - Jamie
==================================================
CHANGE LOG
+ Ported Honeycomb summer project - CAT
-

TODO Eat food


"""

# IMPORTS
import random
from math import floor

import os
import pygame
import sys
from pygame.locals import *

# STATICS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
TILE_COLUMNS = 45
TILE_ROWS = 45
MAP_WIDTH = 10
MAP_HEIGHT = 10
player_positions = [[135, 135], [135, 135], [135, 135], [135, 135], [135, 135], [135, 135]]
hor = 0
vert = 0
idx = 0
idy = 0

# IMAGES LD
TOP = pygame.image.load('images/tiletop.png')
FLOORX = pygame.image.load('images/tilered.png')
FLOORO = pygame.image.load('images/tilegreen.png')
FLOORY = pygame.image.load('images/tilegold.png')
FLOORW = pygame.image.load('images/tilewhite.png')
SIDE = pygame.image.load('images/tilewall.png')
GOAL = pygame.image.load('images/goal.png')
# BLACK = pygame.image.load('images/black.png')
player = [pygame.image.load('images/santa.png'),]
display = (TILE_COLUMNS * MAP_WIDTH, TILE_ROWS * MAP_HEIGHT)
fog_of_war = pygame.Surface(display)

TILEMAP = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 4, 4, 4, 4, 4, 4, 4, 0, 0,
    0, 1, 2, 1, 2, 1, 2, 1, 0, 0,
    0, 2, 1, 2, 1, 2, 1, 2, 5, 9,
    0, 1, 2, 1, 2, 1, 2, 1, 6, 10,
    0, 2, 1, 2, 1, 2, 1, 2, 7, 11,
    0, 1, 2, 1, 2, 1, 2, 1, 8, 12,
    0, 2, 1, 2, 1, 2, 1, 2, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    4, 4, 4, 4, 4, 4, 4, 4, 4, 4,

]

HOUSES = [pygame.image.load('images/house1.png'),
          pygame.image.load('images/house2.png'),
          pygame.image.load('images/house3.png'),
          pygame.image.load('images/house4.png')]

PEOPLE = [pygame.image.load('images/santadoggo.png'),
          pygame.image.load('images/billy.png'),
          pygame.image.load('images/vader.png'),
          pygame.image.load('images/francine.png')]

PRESENTS = [pygame.image.load('images/presentg.png'),
            pygame.image.load('images/present1.png'),
            pygame.image.load('images/present2.png'),
            pygame.image.load('images/present3.png')]

OBJECTS = [pygame.image.load('images/bone.png'),
           pygame.image.load('images/chainsaw.png'),
           pygame.image.load('images/deathstar.png'),
           pygame.image.load('images/pizza.png')]

delPeeps = []
delPres = []
PRESPOS = []
delcount = 0
gifts = ["bone", "chainsaw", "deathstar", "pizza"]
holding = []
inventory = []
# =======================================================================================================================
# FUNCTIONS
# =======================================================================================================================

def readRoomsfile(filename):
    assert os.path.exists(filename), 'No found level file'
    mapFile = open(filename, 'r')
    content = mapFile.readlines()
    mapFile.close()


# y * 10 + x
def draw_map(screen):
    for index, tile in enumerate(TILEMAP):
        idy = int(floor(index / 10) * 45)
        idx = int((index % 10) * 45)   # TODO changed
        if tile == 0:
            screen.blit(TOP, (idx, idy))
        elif tile == 1:
            screen.blit(FLOORX, (idx, idy))
        elif tile == 2:
            screen.blit(FLOORO, (idx, idy))
        elif tile == 3:
            screen.blit(GOAL, (idx, idy))
        elif tile == 4:
            screen.blit(SIDE, (idx, idy))
        elif tile == 5:
            screen.blit(HOUSES[0], (idx, idy))
        elif tile == 6:
            screen.blit(HOUSES[1], (idx, idy))
        elif tile == 7:
            screen.blit(HOUSES[2], (idx, idy))
        elif tile == 8:
            screen.blit(HOUSES[3], (idx, idy))
        elif tile == 9:
            screen.blit(PEOPLE[0], (idx, idy))
        elif tile == 10:
            screen.blit(PEOPLE[1], (idx, idy))
        elif tile == 11:
            screen.blit(PEOPLE[2], (idx, idy))
        elif tile == 12:
            screen.blit(PEOPLE[3], (idx, idy))
        else:
            print "No known tiles found"


def check_block(x, y):
    print x, y
    px = x /45
    py = y / 45
    check_index = TILEMAP[py * 10 + px]

    for i in range(0, len(PRESPOS)):
        if x == PRESPOS[i][0] and y == PRESPOS[i][1]:  # TODO - Change pos to match player's feet rather than head
            return i  # PRESENT
            print "PRESENT: " + str(i)
    if check_index == 5:
        return -5
    elif check_index == 6: return -6
    elif check_index == 7: return -7
    elif check_index == 8: return -8
    elif check_index != 0:
        print delPres
        return -1  # True
    else:
        print ("Move invalid")
        return -2  # False


def move(start_x, start_y, x, y):  # 25, 25
    global delcount
    end_x = start_x + x
    end_y = start_y + y
    if check_block(end_x, end_y) == -1:
        return (end_x, end_y)
    elif check_block(end_x, end_y) >= 0:
        present(check_block(end_x, end_y), pygame.display.set_mode((MAP_WIDTH * TILE_COLUMNS, MAP_HEIGHT * TILE_ROWS)))
        return (end_x, end_y)
    elif check_block(end_x, end_y) == -5: # TODO fix...
        if len(inventory) > 0:
            inventory.pop(0)
            print "delivered "+str(holding[0])+" to Festive Doggo"
            delPeeps.append("festive doggo")
            delPres.append(str(holding[0]))
            holding.pop(0)
            delcount = delcount + 1
            return (end_x, end_y)
        else:
            print "you can't deliver without a gift? What kind of santa are you?"
            return (start_x, start_y)
    elif check_block(end_x, end_y) == -6: # TODO fix...
        if len(inventory) > 0:
            inventory.pop(0)
            print "delivered "+str(holding[0])+" to Billy"
            delPeeps.append("Billy")
            delPres.append(str(holding[0]))
            holding.pop(0)
            delcount = delcount + 1
            return (end_x, end_y)
        else:
            print "you can't deliver without a gift? What kind of santa are you?"
            return (start_x, start_y)
    elif check_block(end_x, end_y) == -7: # TODO fix...
        if len(inventory) > 0:
            inventory.pop(0)
            print "delivered "+str(holding[0])+" to Vader"
            delPeeps.append("Darth Vader")
            delPres.append(str(holding[0]))
            holding.pop(0)
            delcount = delcount + 1
            return (end_x, end_y)
        else:
            print "you can't deliver without a gift? What kind of santa are you?"
            return (start_x, start_y)
    elif check_block(end_x, end_y) == -8: # TODO fix...
        if len(inventory) > 0:
            inventory.pop(0)
            print "delivered "+str(holding[0])+" to Francine"
            delPeeps.append("Francine")
            delPres.append(str(holding[0]))
            holding.pop(0)
            delcount = delcount + 1
            return (end_x, end_y)
        else:
            print "you can't deliver without a gift? What kind of santa are you?"
            return (start_x, start_y)
    else:
        return (start_x, start_y)
        # DISPLAYSURF.blit(player, (playerx, playery))
        # pygame.display.update()


def present(index, screen):
    PRESPOS.pop(index)
    # TODO display item
    inventory.append(index)
    holding.append(gifts[index])
    print "inventory"+str(inventory)
    screen.blit(OBJECTS[index], (90, 90))
    print PRESPOS


def init():
    pygame.init()
    screen = pygame.display.set_mode((MAP_WIDTH * TILE_COLUMNS, MAP_HEIGHT * TILE_ROWS))
    # fog_of_war.fill((0, 0, 0))
    return screen


def update(player, x, y, screen):
    screen.blit(player, (x, y))
    pygame.display.flip()


# =======================================================================================================================
# MAIN
# =======================================================================================================================

def main():
    screen = init()
    FONT = pygame.font.SysFont("monospace", 15)
    clock = pygame.time.Clock()

    for index, item in enumerate(PRESENTS):
        ax = random.randint(2, 7) # TODO - Change ax range so it doesn't blit into a wall
        ay = random.randint(3, 8) # TODO - Change ay range so it doesn't blit into a wall
        bx = ax * 45
        by = ay * 45
        PRESPOS.append([bx, by])
    print PRESPOS
    while True:


        clock.tick(30)

        if delcount <= 3:

            draw_map(screen)
            for index, item in enumerate(PRESPOS):
                screen.blit(PRESENTS[index], (PRESPOS[index][0], PRESPOS[index][1]))
            label = FONT.render("Inventory:", 1, (0,0,0))
            screen.blit(label, (315, 20))
            if len(inventory) > 0:
               #screen.blit(PRESENTS[1], (450, 0)) # TODO blit presents top right
               screen.blit(PRESENTS[1], (405, 20))
             # pygame.draw.rect(fog_of_war, (60, 60, 60), (playerx,playery+45,50,50))
             # fog_of_war.set_colorkey((60, 60, 60))

             # print inventory


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif not hasattr(event, 'key'):
                    continue
                elif event.type == pygame.KEYDOWN:
                    current_x, current_y = player_positions[0]
                    if event.key == K_ESCAPE:
                        sys.exit(0)
                    elif event.key == K_LEFT:
                        current_x, current_y = move(current_x, current_y, -45, 0)  # LEFT = (-45,0)  RIGHT = (45, 0)  UP = (0,-45)  DOWN=(0, 45)

                        update(player[0], current_x, current_y, screen)
                        player_positions[0] = [current_x, current_y]
                    elif event.key == K_RIGHT:
                        current_x, current_y = move(current_x, current_y, 45, 0)

                        update(player[0], current_x, current_y, screen)
                        player_positions[0] = [current_x, current_y]
                    elif event.key == K_UP:

                        update(player[0], current_x, current_y, screen)
                        player_positions[0] = [current_x, current_y]
                        current_x, current_y = move(current_x, current_y, 0, -45)

                        update(player[0], current_x, current_y, screen)
                        player_positions[0] = [current_x, current_y]
                    elif event.key == K_DOWN:
                        current_x, current_y = move(current_x, current_y, 0, 45)

                        update(player[0], current_x, current_y, screen)
                        player_positions[0] = [current_x, current_y]

        else:
            print("It was a busy christmas for santa clause. As he lay down in bed after a hard nights work, he wondered what everyone was thinking...")
            print("")
            print("")
            print (len(delPres))
            for i in range(1,4):
                if delPres[i] == "bone":
                    print(delPeeps[i]+" tore off the wrapping paper, revealing a glorious shiny bone. "+delPeeps[i]+" chewed and knarled the bone all day. Truly a christmas to remember")
                elif delPres[i] == "chainsaw":
                    print(delPeeps[i]+" knew what it was before even unwrapping it. They had been waiting for this day their entire lives. "+delPeeps[i]+" wielded the chainsaw, as they had dreamed of many times before.")
                    print("'Time to visit a friend' "+delPeeps[i]+" said laughing")
                elif delPres[i] == "deathstar":
                    print(delPeeps[i]+" wasn't really sure what to do with their moon sized planet destroyer. ")
                elif delPres[i] == "pizza":
                    print(delPeeps[i]+" stared hungrily into the now empty pizza box. 'I'm such a pig' they proclaimed. Slowly, "+delPeeps[i]+" became even more depressed")
            print("")
            print("")
            print("")
            print ("MERRY XMAS")
            sys.exit(0)
                    #          update(player[current_index], current_x, current_y, screen)
                    #               current_x, current_y = player_positions[0]
                    #               update(player[0], current_x, current_y, screen)


if __name__ == '__main__':
    main()
