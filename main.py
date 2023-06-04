import game
from objects import Vector, Rect
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

def draw():
    game.WIN.fill(game.BLACK)

    for obj in game.OBJECTS:
        obj.draw()

    pygame.display.update()

def main():
    delta_time = 1
    game.OBJECTS.add(Rect(Vector(300, 300), 400, 200))
    while True:
        time1 = time.perf_counter()

        update(delta_time)

        handle_events()

        draw()

        time2 = time.perf_counter()
        delta_time = time2 - time1


if __name__ == "__main__":
    main()
