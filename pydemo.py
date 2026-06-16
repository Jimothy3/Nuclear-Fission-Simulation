# Name: James Holland
# Programming Assignment: Nuclear Fission Simulator
# Date: June 15, 2026
import pygame as pg
import random

if not pg.font:
    print("Warning: fonts disabled")

pg.init()
SCREEN_WIDTH, SCREEN_HEIGHT = (1280, 720)
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()
running = True

###############
# Def: Particle is what eminates from a starting uranium particle (protons/neutrons)
# 
# Method(s):
#   __init__: 5-arg ctor - defines radius, proton/neutron, vector speed, location
###############
class Particle:

    # 6-arg ctor
    def __init__(self, radius, x_speed, y_speed, x, y):
        self.radius = radius
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.x = x
        self.y = y
        
        # type
        start_val = 0
        stop_val = 20 # must not be zero

        picker = random.randrange(start_val, stop_val, 1)
        self.picker = picker
        if picker < 10:
            self.type = 'Proton'
        else:
            self.type = 'Neutron'

        # color
        if self.type == 'Proton':
            self.color = 'IndianRed'
        else:
            self.color = 'SlateGray'

###############
# Def: Uranium is the objects being statically held in a grid-style format
# 
# Method(s):
#   __init__: 4-arg ctor - defines uranium particle. location and radius
###############
class Uranium:
    def __init__(self, rad, color, x, y):
        self.radius = rad
        self.color = color
        self.x = x + 200
        self.y = y + 50

###############
# Def: Grid is the uranium grid
# 
# Method(s):
#   __init__: 2-arg ctor consisting of row/col format to create a simple rectangular grid of particles.
###############
class Grid:
    def __init__(self, rows, cols):
        RADIUS = 10
        COLOR = 'SkyBlue'
        MAX_INTEGER = 50

        if rows > MAX_INTEGER or cols > MAX_INTEGER or rows < 0 or cols < 0:
            raise Exception("ERROR: overflow/underflow, too many particles or negative amount of them.")
        
        self.radius = RADIUS
        self.color = COLOR
        self.rows = rows
        self.columns = cols
        self.particles = [[]for _ in range(rows)]

        PADDING = 50
        AVAILABLE_WIDTH = SCREEN_WIDTH - (PADDING * 2)
        AVAILABLE_HEIGHT = SCREEN_HEIGHT - (PADDING * 2)
        X_Step = AVAILABLE_WIDTH / cols
        Y_Step = AVAILABLE_HEIGHT / rows

        for r in range(rows):
            for c in range(cols):
                self.particles[r].append(Uranium(RADIUS, COLOR, PADDING - RADIUS + (c * X_Step), PADDING - RADIUS + (r * Y_Step)))


######################################################################################################################################
#                                              SIMULATION INSTANTIATION                                                              #
######################################################################################################################################
grid = Grid(15, 3)

######################################################################################################################################
#                                                     GAMEPLAY                                                                       #
######################################################################################################################################
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill("white")

    # RENDER GAME HERE

    for row in range(grid.rows):
        for col in range(grid.columns):
            pg.draw.circle(screen, grid.color, (grid.particles[row][col].x, grid.particles[row][col].y), grid.radius)

    if pg.font:
        font = pg.font.Font(None, 64)
        text = font.render("", True, (10, 10, 10))
        textpos = text.get_rect(centerx=350, y=10)
        screen.blit(text, textpos)
    pg.display.flip()

    clock.tick(60)

pg.quit()