import game
from objects import Vector, Particle, Rect
import time
import pygame



def update(delta_time):
    for obj in game.OBJECTS:
        if hasattr(obj, "update"):
            obj.update(delta_time)

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 1 is left click
            x, y = pygame.mouse.get_pos()
            game.OBJECTS.add(Particle(Vector(x, y)))

def draw():
    game.WIN.fill(game.BLACK)

    for obj in game.OBJECTS:
        obj.draw()

    pygame.display.update()

def create_border():
    # Rect have a thickness of 100
    game.OBJECTS.add(Rect(Vector(game.WIDTH/2, -50), game.WIDTH + 100, 100))  # TOP
    game.OBJECTS.add(Rect(Vector(game.WIDTH + 50, game.HEIGHT/2), 100, game.HEIGHT + 100))  # RIGHT
    game.OBJECTS.add(Rect(Vector(game.WIDTH/2, game.HEIGHT + 50), game.WIDTH + 100, 100))  # BOTTOM
    game.OBJECTS.add(Rect(Vector(-50, game.HEIGHT/2), 100, game.HEIGHT + 100))  # LEFT

def create_map():
    game.OBJECTS.add(Rect(Vector(250, 400), 300, 150, rotation=160))
    game.OBJECTS.add(Rect(Vector(800, 450), 350, 100, rotation=60))

def main():
    delta_time = 1
    create_border()
    create_map()
    while True:
        time1 = time.perf_counter()

        update(delta_time)

        handle_events()

        draw()

        time2 = time.perf_counter()
        delta_time = time2 - time1


if __name__ == "__main__":
    main()
