"""
==================================================
Xmas Code project
Written by Cat.
Graphics by Paul & Sean. 
Team supervisor - Jamie
==================================================
CHANGE LOG
+ Ported Honeycomb summer project - CAT
-

TODO Eat food


"""

# IMPORTS
import pygame, sys, math, time, os
from pygame.locals import *
from math import floor
import random

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
player = [pygame.image.load('images/santa.png'),
          pygame.image.load('images/astro2.png'),
          pygame.image.load('images/astro3.png'),
          pygame.image.load('images/astro4.png'),
          pygame.image.load('images/astro5.png'),
          pygame.image.load('images/astro6.png'), ]
display = (TILE_COLUMNS * MAP_WIDTH, TILE_ROWS * MAP_HEIGHT)
fog_of_war = pygame.Surface(display)

TILEMAP = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 4, 4, 4, 4, 4, 4, 4, 4, 0,
    0, 1, 2, 1, 2, 1, 2, 1, 2, 0,
    0, 2, 1, 2, 1, 3, 3, 2, 1, 0,
    0, 1, 2, 1, 2, 3, 3, 1, 2, 0,
    0, 2, 1, 2, 1, 2, 1, 2, 1, 0,
    0, 1, 2, 1, 2, 1, 2, 1, 2, 0,
    0, 2, 1, 2, 1, 2, 1, 2, 1, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    4, 4, 4, 4, 4, 4, 4, 4, 4, 4

]

PRESENTS = [pygame.image.load('images/presentg.png'),
            pygame.image.load('images/present1.png'),
            pygame.image.load('images/present2.png'),
            pygame.image.load('images/present3.png')
            ]

PRESPOS = []


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
        idx = int((index % 10) * 45)
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
            screen.blit(BLACK, (idx, idy))
        else:
            print "No known tiles found"


def check_block(x, y):
    print x, y
    px = x / 45
    py = y / 45
    check_index = TILEMAP[py * 10 + px]

    for i in range(0, len(PRESPOS)):
        if x == PRESPOS[i][0] and y == PRESPOS[i][1]:  # TODO - Change pos to match player's feet rather than head
            return i  # PRESENT
            print "PRESENT: " + str(i)
    if check_index != 0:
        return -1  # True
    else:
        print ("Move invalid")
        return -2  # False


def move(start_x, start_y, x, y):  # 25, 25
    end_x = start_x + x
    end_y = start_y + y
    if check_block(end_x, end_y) == -1:
        return (end_x, end_y)
    elif check_block(end_x, end_y) >= 0:
        print "YAY"
        present(check_block(end_x, end_y))
        return (end_x, end_y)
    else:
        return (start_x, start_y)
        # DISPLAYSURF.blit(player, (playerx, playery))
        # pygame.display.update()


def present(index):
    PRESPOS.pop(index)
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
    clock = pygame.time.Clock()

    for index, item in enumerate(PRESENTS):
        ax = random.randint(1, 10) # TODO - Change ax range so it doesn't blit into a wall
        ay = random.randint(1, 10) # TODO - Change ay range so it doesn't blit into a wall
        bx = ax * 45
        by = ay * 45
        PRESPOS.append([bx, by])
    print PRESPOS
    while True:
        clock.tick(30)
        draw_map(screen)
        for index, item in enumerate(PRESPOS):
            screen.blit(PRESENTS[index], (PRESPOS[index][0], PRESPOS[index][1]))
        # pygame.draw.rect(fog_of_war, (60, 60, 60), (playerx,playery+45,50,50))
        # fog_of_war.set_colorkey((60, 60, 60))

        inventory = []
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
                    current_x, current_y = move(current_x, current_y, -45,
                                                0)  # LEFT = (-45,0)  RIGHT = (45, 0)  UP = (0,-45)  DOWN=(0, 45)

                    update(player[0], current_x, current_y, screen)
                    player_positions[0] = [current_x, current_y]
                elif event.key == K_RIGHT:
                    current_x, current_y = move(current_x, current_y, 45, 0)
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

                    #          update(player[current_index], current_x, current_y, screen)
                    #               current_x, current_y = player_positions[0]
                    #               update(player[0], current_x, current_y, screen)


if __name__ == '__main__':
    main()
