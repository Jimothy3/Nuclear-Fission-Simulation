# Name: James Holland
# Programming Assignment: Nuclear Fission Simulator
# Date: June 15, 2026
import random as rand
import pygame as pg
import time   as t

if not pg.font:
    print("Warning: fonts disabled")

pg.init()
SCREEN_WIDTH, SCREEN_HEIGHT = (1280, 720)
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()
running = True

######################################################################################################################################
#                                                     PARTICLE                                                                       #
######################################################################################################################################
# Def: Particle is what eminates from an active uranium particle (protons/neutrons)                                                  #
#                                                                                                                                    #
# Method(s):                                                                                                                         #
#   __init__  : 5-arg ctor   - defines radius, proton/neutron, vector speed, location                                                #
#   __update__: 0-arg method - updates particle location and speed                                                                   #
######################################################################################################################################
class Particle:
    def __init__(self, radius, x_speed, y_speed, x, y):
        self.radius = radius
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.x = x
        self.y = y
        
        # type
        start_val = 0
        stop_val = 20 # must not be zero

        picker = rand.randrange(start_val, stop_val, 1)

        if picker < 10:
            self.type = 'Proton'
        else:
            self.type = 'Neutron'

        # color
        if self.type == 'Proton':
            self.color = 'IndianRed'
        else:
            self.color = 'SlateGray'
    
    def __update__(self):
        self.x += self.x_speed
        self.y += self.y_speed
        self.x_speed -= 0.1
        self.y_speed -= 0.1

######################################################################################################################################
#                                                      URANIUM                                                                       #
######################################################################################################################################
# Def: Uranium is the objects being statically held in a grid-style format                                                           #
#                                                                                                                                    #
# Method(s):                                                                                                                         #
#   __init__            : 4-arg ctor                      - defines uranium particle. location and radius                            #
#   __irradiate__       : 0-arg method                    - creates 1-5 random particles                                             #
#   __update_particles__: 0-arg method                    - function to easily update the location of loose particles                #
#   __collision__       : 2-arg method (X-Coord, Y-Coord) - Returns whether a target is touching a uranium particle                  #
######################################################################################################################################
class Uranium:
    def __init__(self, rad, color, x, y):
        self.radius = rad
        self.color = color
        self.x = x
        self.y = y
        self.particles = []

    def __irradiate__(self):
        MAX_PARTICLES = 5
        num_particles = rand.randrange(1, MAX_PARTICLES)
        self.particles = []
        for _ in range(num_particles):
            RADIUS = 2
            xspeed, yspeed = (rand.randrange(1, 10), rand.randrange(1, 10))
            self.particles.append(Particle(RADIUS, xspeed, yspeed, self.x, self.y))

    def __update_particles__(self):
        for i in range(len(self.particles)):
            self.particles[i].__update__()
    
    def __collision__(self, x, y):
        x_touching = False
        y_touching = False

        if x >= self.x - self.radius and x <= self.x + self.radius:
            x_touching = True
        if y >= self.y - self.radius and y <= self.y + self.radius:
            y_touching = True

        return x_touching and y_touching
        
######################################################################################################################################
#                                                         GRID                                                                       #
######################################################################################################################################
# Def: Grid is a 2D-array of uranium                                                                                                 #
#                                                                                                                                    #
# Method(s):                                                                                                                         #
#   __init__            : 2-arg ctor   - consisting of row/col format to create a simple rectangular grid of particles.              #
#   __update_radiation__: 0-arg method - function to easily update the location of loose particles                                   #
######################################################################################################################################
class Grid:
    def __init__(self, rows, cols):
        RADIUS = 10
        COLOR = 'SkyBlue'
        MAX_INTEGER = 25

        if rows < 0 or cols < 0:
            raise Exception("ERROR: underflow, negative particles")
        if rows >= MAX_INTEGER or cols >= MAX_INTEGER:
            raise Exception("ERROR: overflow, too many particles")
        
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
    
    def __update_radiation__(self):
        for row in range(self.rows):
            for col in range(self.columns):
                self.particles[row][col].__update_particles__()

######################################################################################################################################
#                                                     GAMEPLAY                                                                       #
######################################################################################################################################
grid = Grid(5, 5)

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill("white")

    # RENDER GAME HERE
    for row in range(grid.rows):
        for col in range(grid.columns):
            pg.draw.circle(screen, grid.color, (grid.particles[row][col].x, grid.particles[row][col].y), grid.radius)
            grid.particles[row][col].__irradiate__()

            for p in range(len(grid.particles[row][col].particles)):
                pg.draw.circle(screen, grid.particles[row][col].particles[p].color, 
                                (grid.particles[row][col].particles[p].x, grid.particles[row][col].particles[p].y),
                                grid.radius - 5)
            
    for row in range(grid.rows):
        for col in range(grid.columns):
            grid.__update_radiation__()
            for p in range(len(grid.particles[row][col].particles)):
                pg.draw.circle(screen, grid.particles[row][col].particles[p].color, 
                               (grid.particles[row][col].particles[p].x, grid.particles[row][col].particles[p].y),
                               grid.radius - 5)
                t.sleep(0.0001)
    

    if pg.font:
        font = pg.font.Font(None, 64)
        text = font.render("", True, (10, 10, 10))
        textpos = text.get_rect(centerx=350, y=10)
        screen.blit(text, textpos)
    pg.display.flip()

    clock.tick(60)

pg.quit()