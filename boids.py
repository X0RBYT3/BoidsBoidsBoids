import pygame as pg
import sys
import random
import math
from pygame.locals import * 

## BOIDS 1.0 
## TODO: FIX MOUSE INPUT


pg.init()
# Consts 
WIDTH, HEIGHT = 1000, 1000 # Change as necessary
FPS = 60
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

NUM_BOIDS = 100 # Higher numbers cause more lag, who knew?
BOID_RADIUS = 5 # This is the radius of the circle, it should be a tri but idc enough rn
SPEED = 5 

# Helpful function
def angle_difference(target, current):
    return (target - current + math.pi) % (2 * math.pi) - math.pi

class Boid:
    # Takes a spawn X, Y coord
    # Each boid spawns with a random turn angle
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = random.uniform(0,2 * math.pi)

        # Exponents 
        self.A = 1.2 # Cohesion
        self.B = 1.1 # Seperation
        self.C = 0.75 # Alignment
        self.D = 1 # Align with Mouse // Not Working 
        
    def update(self, boids): # Called every frame, takes ALL other boids as input
        cohesion = self.cohesion(boids) 
        seperation = self.separation(boids)
        alignment = self.alignment(boids)
        align_with_mouse = self.align_with_mouse(boids)

        self.angle += 0.1 * (cohesion * self.A + seperation * self.B + alignment * self.C + align_with_mouse * self.D)
        self.x += SPEED * math.cos(self.angle)
        self.y += SPEED * math.sin(self.angle)

        # Wrap around screen
        self.x %= WIDTH
        self.y %= HEIGHT

    def cohesion(self, boids): 
        """
        Move towards the center of all other boids 
        """
        # Find center of other boids
        center_x = sum(b.x for b in boids) / len(boids)
        center_y = sum(b.y for b in boids) / len(boids)
        # Find angle to center
        angle_to_center = math.atan2(center_y - self.y, center_x - self.x)
        return angle_difference(angle_to_center, self.angle) # return the difference

    def separation(self, boids):
        """
        Move away from nearby boids to avoid collisions
        """
        min_distance = 20
        move_x = 0
        move_y = 0

        for b in boids:
            if b != self:
                distance = math.hypot(self.x - b.x, self.y - b.y)
                if 0 < distance < min_distance:
                    move_x += (self.x - b.x) / distance
                    move_y += (self.y - b.y) / distance

        move_angle = math.atan2(move_y, move_x) if move_x != 0 or move_y != 0 else 0
        return angle_difference(move_angle, self.angle)
    
    def alignment(self, boids):
        """
        Align with average direction of all other boids 
        """
        avg_angle = sum(b.angle for b in boids) / len(boids)
        return angle_difference(avg_angle, self.angle)

    def align_with_mouse(self, boids):
        """
        Move somewhat towards the mouse, May change to a LMB / RMB situation?
        """
        mouse_x, mouse_y = pg.mouse.get_pos()
        # find angle
        angle_to_mouse = math.atan2(mouse_x - self.x, mouse_y - self.y)
        return angle_difference(angle_to_mouse, self.angle)


# Create boids
boids = [Boid(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(NUM_BOIDS)]

# Set up the Pygame screen
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Boids Simulation")
clock = pg.time.Clock()

# Main game loop
while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()

    # Update boids
    for boid in boids:
        boid.update(boids)

    # Draw boids
    screen.fill(BLACK)
    for boid in boids:
        pg.draw.circle(screen, RED, (int(boid.x), int(boid.y)), BOID_RADIUS)
    # Update and keep to FPS
    pg.display.flip()
    clock.tick(FPS)
