# Name: James Holland
# Programming Assignment: Nuclear Fission Simulator
# Date: June 15, 2026
import random as rand
import pygame as pg

if not pg.font:
    print("Warning: fonts disabled")

pg.init()
if pg.font:
    font = pg.font.Font(None, 64)
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
#   __init__   : 5-arg ctor   - defines radius, proton/neutron, vector speed, location                                               #
#   __update__ : 0-arg method - updates particle location and speed                                                                  #
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

        if picker < (start_val + stop_val) / 2:
            self.type = 'Proton'
        else:
            self.type = 'Neutron'

        # color
        if self.type == 'Proton':
            self.color = 'IndianRed'
        else:
            self.color = 'SlateGray'
    
    def __update__(self):
        xdirection = rand.randrange(1, 10)
        ydirection = rand.randrange(1, 10)
        if xdirection < 5:
            self.x += self.x_speed
        else:
            self.x -= self.x_speed

        if ydirection < 5:
            self.y += self.y_speed
        else:
            self.y -= self.y_speed            

######################################################################################################################################
#                                                      URANIUM                                                                       #
######################################################################################################################################
# Def: Uranium is the objects being statically held in a grid-style format                                                           #
#                                                                                                                                    #
# Method(s):                                                                                                                         #
#   __init__             : 4-arg ctor   - defines uranium particle. location and radius                                              #
#   __irradiate__        : 0-arg method - creates 1-5 random particles                                                               #
#   __update_particles__ : 0-arg method - function to easily update the location of loose particles                                  #
#   __clear_particles__  : 0-arg method - sets all particle lists to []                                                              #
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
        for _ in range(num_particles):
            RADIUS = 2
            xspeed, yspeed = (rand.randrange(-10, 10), rand.randrange(-10, 10))
            self.particles.append(Particle(RADIUS, xspeed, yspeed, self.x, self.y))

    def __update_particles__(self):
        for i in range(len(self.particles)):
            self.particles[i].__update__()

    def __clear_particles__(self):
        self.particles = []
        
######################################################################################################################################
#                                                         GRID                                                                       #
######################################################################################################################################
# Def: Grid is a 2D-array of uranium                                                                                                 #
#                                                                                                                                    #
# Method(s):                                                                                                                         #
#   __init__             : 2-arg ctor   - consisting of row/col format to create a simple rectangular grid of particles.             #
#   __update_radiation__ : 0-arg method - function to easily update the location of loose particles                                  #
#   __collision__        : 4-arg method - function to detect collisions and automatically cause chain-reaction                       #
#   __clear_fission__    : 0-arg method - function to reset all fission (all particle lists set to [])                               #
######################################################################################################################################
class Grid:
    def __init__(self, rows, cols):
        RADIUS = 10
        COLOR = 'SkyBlue'
        MAX_INTEGER = 10

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

    def __collision__(self, x = 0, y = 0, parentx = 0, parenty = 0):
        for row in range(self.rows):
            for col in range(self.columns):
                x_touching = False
                y_touching = False

                if x >= parentx - self.particles[row][col].radius and x <= parentx + self.particles[row][col].radius:
                    if y >= parenty - self.particles[row][col].radius and y <= parenty + self.particles[row][col].radius:
                        continue

                if x >= self.particles[row][col].x - self.particles[row][col].radius and x <= self.particles[row][col].x + self.particles[row][col].radius:
                    x_touching = True
                if y >= self.particles[row][col].y - self.particles[row][col].radius and y <= self.particles[row][col].y + self.particles[row][col].radius:
                    y_touching = True
                if x_touching and y_touching:
                    self.particles[row][col].__irradiate__()
                    return True
        return False
    
    def __clear_fission__(self):
        for row in range(self.rows):
            for col in range(self.columns):
                self.particles[row][col].__clear_particles__()

######################################################################################################################################
#                                                     GAMEPLAY                                                                       #
######################################################################################################################################
ROWS = 7
COLS = 7
BUTTON_WIDTH, BUTTON_HEIGHT = (170, 64)
BUTTON_RADIATE_X, BUTTON_RADIATE_Y = (SCREEN_WIDTH - BUTTON_WIDTH - 50, 10)
BUTTON_CLEAR_X, BUTTON_CLEAR_Y = (SCREEN_WIDTH - BUTTON_WIDTH - 50, 84)
grid = Grid(ROWS, COLS)

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if pg.Rect(BUTTON_RADIATE_X, BUTTON_RADIATE_Y, BUTTON_WIDTH, BUTTON_HEIGHT).collidepoint(mouse_x, mouse_y):
                grid.particles[0][0].__irradiate__()
            elif pg.Rect(BUTTON_CLEAR_X, BUTTON_CLEAR_Y, BUTTON_WIDTH, BUTTON_HEIGHT).collidepoint(mouse_x, mouse_y):
                grid.__clear_fission__()

    screen.fill("white")

    # render uranium and particles
    for row in range(grid.rows):
        for col in range(grid.columns):
            pg.draw.circle(screen, grid.color, (grid.particles[row][col].x, grid.particles[row][col].y), grid.radius)

            for p in range(len(grid.particles[row][col].particles)):
                pg.draw.circle(screen, grid.particles[row][col].particles[p].color, 
                                (grid.particles[row][col].particles[p].x, grid.particles[row][col].particles[p].y), grid.radius - 5)
    
    # update particles so they move
    for row in range(grid.rows):
        for col in range(grid.columns):
            for p in range(len(grid.particles[row][col].particles)):
                pg.draw.circle(screen, grid.particles[row][col].particles[p].color, 
                               (grid.particles[row][col].particles[p].x, grid.particles[row][col].particles[p].y),
                               grid.radius - 5)

                # fission chain-reaction method
                grid.__collision__(grid.particles[row][col].particles[p].x, 
                                   grid.particles[row][col].particles[p].y, 
                                   grid.particles[row][col].x, grid.particles[row][col].y)

    grid.__update_radiation__()

    # Button to Radiate
    pg.draw.rect(screen, 'IndianRed', (BUTTON_RADIATE_X, BUTTON_RADIATE_Y, BUTTON_WIDTH, BUTTON_HEIGHT))
    if pg.font:
        text = font.render("Radiate", True, (10, 10, 10))
        textpos = text.get_rect(x=BUTTON_RADIATE_X + 2, y=BUTTON_RADIATE_Y + 10)
        screen.blit(text, textpos)

    # Button to Reset
    pg.draw.rect(screen, 'Orange', (BUTTON_CLEAR_X, BUTTON_CLEAR_Y, BUTTON_WIDTH, BUTTON_HEIGHT))
    if pg.font:
        text = font.render("Clear", True, (10, 10, 10))
        textpos = text.get_rect(x=BUTTON_CLEAR_X + 2, y=BUTTON_CLEAR_Y + 10)
        screen.blit(text, textpos)

    pg.display.flip()
    clock.tick(60)

pg.quit()