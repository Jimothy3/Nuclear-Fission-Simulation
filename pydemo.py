# Name: James Holland
# Programming Assignment: Nuclear Fission Simulator
# Date: June 15, 2026
import random as rand
import pygame as pg

if not pg.font:
    print("Warning: fonts disabled")

pg.init()
pg.display.set_caption('Nuclear Fission Simulator')
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
#   __init__ : 5-arg ctor   - defines radius, proton/neutron, vector speed, location                                                 #
#   update   : 0-arg method - updates particle location and speed                                                                    #
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

        if picker < ((start_val + stop_val) / 2) * 0.95:
            self.type = 'Proton'
        else:
            self.type = 'Neutron'

        # color
        if self.type == 'Proton':
            self.color = 'IndianRed'
        else:
            self.color = 'SlateGray'
    
    def update(self):
        self.x += self.x_speed
        self.y += self.y_speed                  

######################################################################################################################################
#                                                      URANIUM                                                                       #
######################################################################################################################################
# Def: Uranium is the objects being statically held in a grid-style format                                                           #
#                                                                                                                                    #
# Method(s):                                                                                                                         #
#   __init__         : 4-arg ctor   - defines uranium particle. location and radius                                                  #
#   irradiate        : 0-arg method - creates 1-5 random particles                                                                   #
#   update_particles : 0-arg method - function to easily update the location of loose particles                                      #
#   clear_particles  : 0-arg method - sets all particle lists to []                                                                  #
######################################################################################################################################
class Uranium:
    def __init__(self, rad, color, x, y):
        self.radius = rad
        self.color = color
        self.x = x
        self.y = y
        self.particles = []

    def irradiate(self):
        MAX_PARTICLES = 3
        MIN_PARTICLES = 2
        FISSION_MINIMUM_FLOAT = .1
        num_particles = rand.randrange(MIN_PARTICLES, MAX_PARTICLES + 1)
        successful_fission = rand.random()
        if successful_fission > FISSION_MINIMUM_FLOAT:
            for _ in range(num_particles):
                RADIUS = 2
                xspeed, yspeed = (rand.randrange(-10, 10), rand.randrange(-10, 10))
                self.particles.append(Particle(RADIUS, xspeed, yspeed, self.x, self.y))

    def update_particles(self):
        PARTICLE_INDEX = 0
        while PARTICLE_INDEX < len(self.particles):
            X = self.particles[PARTICLE_INDEX].x
            Y = self.particles[PARTICLE_INDEX].y
            self.particles[PARTICLE_INDEX].update()

            if X < 0 or X > SCREEN_WIDTH:
                del self.particles[PARTICLE_INDEX]
            elif Y < 0 or Y > SCREEN_HEIGHT:
                del self.particles[PARTICLE_INDEX]
            else:
                PARTICLE_INDEX += 1
            
    def remove_particle(self, index = 0):
        del self.particles[index]

    def clear_particles(self):
        self.particles = []
        
######################################################################################################################################
#                                                         GRID                                                                       #
######################################################################################################################################
# Def: Grid is a 2D-array of uranium                                                                                                 #
#                                                                                                                                    #
# Method(s):                                                                                                                         #
#   __init__         : 2-arg ctor   - consisting of row/col format to create a simple rectangular grid of particles.                 #
#   update_radiation : 0-arg method - function to easily update the location of loose particles                                      #
#   collision        : 4-arg method - function to detect collisions and automatically cause chain-reaction                           #
#   irradiate_cell   : 1-arg method - function to tell a uranium atom to shoot out some particles                                    #
#   clear_fission    : 0-arg method - function to reset all fission (all particle lists set to [])                                   #
######################################################################################################################################
class Grid:
    def __init__(self, rows, cols):
        RADIUS = 10
        COLOR = 'SkyBlue'
        MAX_INTEGER = 50

        if rows < 0 or cols < 0:
            raise Exception("ERROR: underflow, negative particles")
        if rows >= MAX_INTEGER or cols >= MAX_INTEGER:
            raise Exception("ERROR: overflow, too many particles")
        
        self.radius = RADIUS
        self.color = COLOR
        self.rows = rows
        self.columns = cols
        self.atoms = [[]for _ in range(rows)]

        PADDING = 50
        AVAILABLE_WIDTH = SCREEN_WIDTH - (PADDING * 2)
        AVAILABLE_HEIGHT = SCREEN_HEIGHT - (PADDING * 2)
        X_Step = AVAILABLE_WIDTH / cols
        Y_Step = AVAILABLE_HEIGHT / rows

        for r in range(rows):
            for c in range(cols):
                self.atoms[r].append(Uranium(RADIUS, COLOR, PADDING - RADIUS + (c * X_Step), PADDING - RADIUS + (r * Y_Step)))
    
    def update_radiation(self):
        for row in range(self.rows):
            for col in range(self.columns):
                self.atoms[row][col].update_particles()

    def collision(self, x = 0, y = 0, parentx = 0, parenty = 0):
        for row in range(self.rows):
            for col in range(self.columns):
                x_touching = False
                y_touching = False
                radius = self.atoms[row][col].radius
                cur_x = self.atoms[row][col].x
                cur_y = self.atoms[row][col].y
                if x >= parentx - radius and x <= parentx + radius:
                    if y >= parenty - radius and y <= parenty + radius:
                        continue

                if x >= cur_x - radius and x <= cur_x + radius:
                    x_touching = True
                if y >= cur_y - radius and y <= cur_y + radius:
                    y_touching = True
                if x_touching and y_touching:
                    return (True, row, col) # returns atom coordinates that needs to be irradiated
                
        return (False, row, col)
    
    def irradiate_cell(self, atom = Uranium(0,'SlateGray',0,0)):
        atom.irradiate()
        
    def clear_fission(self):
        for row in range(self.rows):
            for col in range(self.columns):
                self.atoms[row][col].clear_particles()

######################################################################################################################################
#                                                     GAMEPLAY                                                                       #
######################################################################################################################################
ROWS = 30
COLS = 30
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
                for _ in range(15):
                    grid.atoms[int(ROWS / 2)][int(COLS / 2)].irradiate()
            elif pg.Rect(BUTTON_CLEAR_X, BUTTON_CLEAR_Y, BUTTON_WIDTH, BUTTON_HEIGHT).collidepoint(mouse_x, mouse_y):
                grid.clear_fission()

    screen.fill("white")

    # render uranium and particles
    for row in range(grid.rows):
        for col in range(grid.columns):
            pg.draw.circle(screen, grid.color, (grid.atoms[row][col].x, grid.atoms[row][col].y), grid.radius)

            for p in range(len(grid.atoms[row][col].particles)):
                pg.draw.circle(screen, grid.atoms[row][col].particles[p].color, 
                                (grid.atoms[row][col].particles[p].x, grid.atoms[row][col].particles[p].y), grid.radius - 5)
                
            # update particles so they move
            particle_index = 0
            while particle_index < len(grid.atoms[row][col].particles):
                PARTICLE_TYPE = grid.atoms[row][col].particles[particle_index].type
                PARTICLE_X = grid.atoms[row][col].particles[particle_index].x
                PARTICLE_Y = grid.atoms[row][col].particles[particle_index].y
                ATOM_X = grid.atoms[row][col].x
                ATOM_Y = grid.atoms[row][col].y

                if PARTICLE_TYPE == 'Neutron':
                    success, row_of_target, col_of_target = grid.collision(PARTICLE_X, PARTICLE_Y, ATOM_X, ATOM_Y)
                    if success:
                        grid.irradiate_cell(grid.atoms[row_of_target][col_of_target])
                        del grid.atoms[row][col].particles[particle_index] # removes neutron from the playing field
                    else:
                        particle_index += 1
                else:
                    particle_index += 1

    grid.update_radiation()

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