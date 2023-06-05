import pygame

WIDTH = 1000
HEIGHT = 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Soft Body Collision")

# Colours
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
BLACK = (0, 0, 0)

from objects import Object
OBJECTS: set[Object] = set()



### SIMULATION PARAMETERS ###
GRAVITY = 200  # Gravitational acceleration
SPRING_LENGTH = 1
SPRING_COEFFICIENT = 1
SPRING_DAMPENING = 1
AIR_RESISTANCE = 0
RESTITUTION = 1
