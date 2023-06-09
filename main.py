import game
from objects import Vector, Particle, SoftBody, Rect, Player_Spring, Player_Pusher
from ui import Canvas
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
            if game.SOFT_MODE:
                game.OBJECTS.add(SoftBody(Vector(x, y), width=6, height=4))
            else:
                game.OBJECTS.add(Particle(Vector(x, y)))

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game.FOLLOW_MOUSE = not game.FOLLOW_MOUSE

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
            game.SOFT_MODE = not game.SOFT_MODE

    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_LCTRL]:
        game.PUSH_PARTICLES = True
    else:
        game.PUSH_PARTICLES = False

font = pygame.font.SysFont("bahnschrift", 20)
def draw(delta_time: float) -> None:
    game.WIN.fill(game.BLUE_GREY)

    for obj in game.OBJECTS:
        obj.draw()

    label = font.render(f"FPS: {round(get_average_fps(delta_time))}", True, game.WHITE)
    game.WIN.blit(label, (8, 8))

    Canvas.draw()

    pygame.display.update()

average_fps_elapsed_time = 0
average_fps = 0
n_fps = 1
showing_average_fps = 0
def get_average_fps(delta_time):
    global average_fps_elapsed_time, average_fps, n_fps, showing_average_fps
    if not delta_time: return average_fps

    average_fps_elapsed_time += delta_time
    if average_fps_elapsed_time > 1:

        average_fps_elapsed_time = 0
        showing_average_fps = average_fps
        average_fps = 1 / delta_time
        n_fps = 1

    else:
        average_fps = (1 / delta_time + n_fps * average_fps) / (n_fps + 1)
        n_fps += 1

    return showing_average_fps

def create_border():
    # Rect have a thickness of 100
    game.OBJECTS.add(Rect(Vector(game.WIDTH/2, -50), game.WIDTH + 100, 100))  # TOP
    game.OBJECTS.add(Rect(Vector(game.WIDTH + 50, game.HEIGHT/2), 100, game.HEIGHT + 100))  # RIGHT
    game.OBJECTS.add(Rect(Vector(game.WIDTH/2, game.HEIGHT + 50), game.WIDTH + 100, 100))  # BOTTOM
    game.OBJECTS.add(Rect(Vector(-50, game.HEIGHT/2), 100, game.HEIGHT + 100))  # LEFT

def create_map():
    # Soft body
    global soft_body
    soft_body = SoftBody(Vector(200, 0), width=4, height=4)
    game.OBJECTS.add(soft_body)

    # Player stuff
    game.OBJECTS.add(Player_Spring(Vector(0, 0), soft_body.particles[0]))
    game.OBJECTS.add(Player_Pusher(Vector(0, 0)))

    # Rectangles
    game.OBJECTS.add(Rect(Vector(250, 180), 350, 75, rotation=-18))
    game.OBJECTS.add(Rect(Vector(640, 320), 350, 75, rotation=30))
    game.OBJECTS.add(Rect(Vector(260, 490), 300, 75, rotation=-25))
    game.OBJECTS.add(Rect(Vector(640, 640), 400, 75, rotation=30))

def main():
    delta_time = 0
    create_border()
    create_map()
    draw(1)
    time.sleep(1)
    while True:
        time1 = time.perf_counter()

        draw(delta_time)

        update(delta_time)

        handle_events()

        time2 = time.perf_counter()
        delta_time = time2 - time1


if __name__ == "__main__":
    main()
