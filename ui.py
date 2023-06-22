import game
import pygame



Colour = tuple[int, int, int]

class Text():
    """`text` is a function"""
    def __init__(self, text, colour: Colour = game.WHITE, size: int = 20) -> None:
        self._text = text
        self.colour = colour
        self.size = size

        self.previous_text = self.text
        self.font = pygame.font.SysFont("bahnschrift", size)
        self._label = self.font.render(self.text, True, self.colour)

    @property
    def text(self) -> str:
        return self._text()

    @property
    def label(self) -> pygame.Surface:
        if self.text != self.previous_text:
            self.previous_text = self.text
            self._label = self.font.render(self.text, True, self.colour)

        return self._label



class Canvas():
    texts = [
        Text(lambda: f"Gravity: {game.GRAVITY}"),
        Text(lambda: f"Spring Length: {game.SPRING_LENGTH}"),
        Text(lambda: f"Spring Coefficient: {game.SPRING_COEFFICIENT}"),
        Text(lambda: f"Spring Dampening: {game.SPRING_DAMPENING}"),
        Text(lambda: f"Player Spring Coefficient: {game.PLAYER_SPRING_COEFFICIENT}"),
        Text(lambda: f"Air Resistance: {game.AIR_RESISTANCE}")
    ]
    x = 8
    y = 200
    gap = 30

    def draw() -> None:
        for idx, text in enumerate(Canvas.texts):
            game.WIN.blit(text.label, (Canvas.x, Canvas.y + idx*Canvas.gap))
