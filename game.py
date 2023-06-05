import pygame

WIDTH = 1000
HEIGHT = 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Soft Body Collision")
pygame.init()

# Colours
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
WHITE = (255, 255, 255)
LIGHT_GREY = (150, 150, 150)
GREY = (70, 70, 70)
DARK_GREY = (30, 30, 30)
BLUE_GREY = (20, 23, 26)
BLACK = (0, 0, 0)

from objects import Object
OBJECTS: set[Object] = set()

FOLLOW_MOUSE = False
SOFT_MODE = False



### SIMULATION PARAMETERS ###
GRAVITY = 100  # Gravitational acceleration
SPRING_LENGTH = 30  # In pixels
SPRING_COEFFICIENT = 2  # Newtons / pixel
SPRING_DAMPENING = 1  # 0 is no dampening, greater than 0 is more dampening
AIR_RESISTANCE = 0.7  # 0 to 1, 0 is no resistance, 1 is max resistance
RESTITUTION = 1
