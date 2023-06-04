from __future__ import annotations
import math
import game
import pygame



Colour = tuple[int, int, int]

class Vector():
    __slots__ = ("x", "y")
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __add__(self, arg: Vector | float) -> Vector:

        # Adding Vectors
        if isinstance(arg, Vector):
            return Vector(self.x + arg.x, self.y + arg.y)

        # Adding Vector to Scalar
        else:
            return Vector(self.x + arg, self.y + arg)

    def __truediv__(self, arg: Vector | float) -> Vector:

        # Dividing Vectors
        if isinstance(arg, Vector):
            return Vector(self.x / arg.x, self.y / arg.y)

        # Dividing Vector by Scalar
        else:
            return Vector(self.x / arg, self.y / arg)

    def __rtruediv__(self, arg: float) -> Vector:

        # arg can't be a Vector
        return Vector(self.x / arg, self.y / arg)

    def __floordiv__(self, arg: float) -> Vector:

        # Dividing Vector by Scalar
        return Vector(int(self.x // arg), int(self.y // arg))

    def __sub__(self, arg: Vector | float) -> Vector:

        # Subtracting Vectors
        if isinstance(arg, Vector):
            return Vector(self.x - arg.x, self.y - arg.y)

        # Subtracting Scalar from Vector
        else:
            return Vector(self.x - arg, self.y - arg)

    def __mul__(self, arg: Vector | float) -> Vector:

        # Multiplying Vectors
        if isinstance(arg, Vector):
            return Vector(self.x * arg.x, self.y * arg.y)

        # Multiplying Vector with Scalar
        else:
            return Vector(self.x * arg, self.y * arg)

    def __rmul__(self, arg: float) -> Vector:

        # arg can't be a Vector
        return Vector(self.x * arg, self.y * arg)

    def __mod__(self, arg: Vector) -> Vector:
        return Vector(int(self.x) % arg, int(self.y) % arg)

    def __neg__(self) -> Vector:
        return Vector(-self.x, -self.y)

    def __bool__(self) -> Vector:
        return bool(self.x) or bool(self.y)

    def __repr__(self) -> str:
        return str((self.x, self.y))

    def __round__(self) -> Vector:
        return Vector(round(self.x), round(self.y))

    def clamp(self, maximum: float) -> None:
        if self.magnitude() > maximum:
            self.set_magnitude(maximum)

    def get_clamp(self, maximum: float) -> Vector:
        if self.magnitude() > maximum:
            # Set magnitude to maximum
            return self * maximum / self.magnitude()
        return self

    def magnitude(self) -> float:
        return (self.x**2 + self.y**2) ** 0.5

    def set_magnitude(self, magnitude: float) -> None:
        # cringe way of updating self
        # can't do "self = new_vector" as self is just a variable
        new_vector = self * magnitude / self.magnitude()
        self.x = new_vector.x
        self.y = new_vector.y

    def get_angle_to(self, position: Vector) -> float:
        angle = math.atan((-position.y + self.y) / (position.x - self.x))
        return angle - math.pi/2 if self.x < position.x else angle + math.pi/2

    def get_angle(self) -> float:
        """Get's the Vector's angle from the origin"""
        return math.atan2(self.y, self.x)

    def rotate(self, angle: float) -> None:
        """Rotates the Vector"""
        x1, y1 = self.x, self.y
        # The positive and negative signs are different
        # Because y increases downwards (for our coord system)
        self.x = y1*math.sin(angle) + x1*math.cos(angle)
        self.y = y1*math.cos(angle) - x1*math.sin(angle)

    def rotated(self, angle: float) -> Vector:
        """Returns a rotated Vector"""
        x1, y1 = self.x, self.y
        # The positive and negative signs are different
        # Because y increases downwards (for our coord system)
        x = y1*math.sin(angle) + x1*math.cos(angle)
        y = y1*math.cos(angle) - x1*math.sin(angle)
        return Vector(x, y)

    def rotate_about(self, angle: float, position: Vector) -> None:
        self.x -= position.x
        self.y -= position.y
        self.rotate(angle)
        self.x += position.x
        self.y += position.y

    def copy(self) -> Vector:
        return Vector(self.x, self.y)

    def in_range(self, x: float, y: float, width: float, height: float) -> bool:
        return self.x >= x and self.x <= x + width and self.y >= y and self.y <= y + height

    def to_tuple(self) -> tuple:
        return self.x, self.y



class Rect():
    """
    `pos` is centre of rectangle

    `rotation` is in degrees

    `outline` is the width of the outline, 0 is filled rectangle
    """
    def __init__(self, pos: Vector, width: int, height: int, rotation: float = 0, colour: Colour = game.WHITE, outline: int = 0) -> None:
        self.pos = pos
        self.width = width
        self.height = height
        self.rotation = rotation
        self.colour = colour
        self.outline = outline

    def __repr__(self) -> str:
        return f"Rect({self.pos}, {self.width}, {self.height})"

    @property
    def rotation(self) -> float:
        """Rect.rotation is degrees, Rect._rotation is radians"""
        return math.degrees(self._rotation)

    @rotation.setter
    def rotation(self, new_rotation) -> None:
        self._rotation = math.radians(new_rotation)

    @property
    def tl(self) -> Vector:
        return self.pos + Vector(-self.width/2, -self.height/2).rotated(self._rotation)

    @property
    def tr(self) -> Vector:
        return self.pos + Vector(self.width/2, -self.height/2).rotated(self._rotation)

    @property
    def bl(self) -> Vector:
        return self.pos + Vector(-self.width/2, self.height/2).rotated(self._rotation)

    @property
    def br(self) -> Vector:
        return self.pos + Vector(self.width/2, self.height/2).rotated(self._rotation)

    @property
    def corners(self) -> tuple[Vector]:
        return self.tl, self.tr, self.bl, self.br

    def update(self, delta_time):
        self.rotation += delta_time * 30

    def draw(self) -> None:
        """surf = pygame.Surface((self.width, self.height), flags=pygame.SRCALPHA)
        pygame.draw.rect(surf, self.colour, (0, 0, self.width, self.height), self.outline)
        #og_width, og_height = surf.get_size()
        surf = pygame.transform.rotate(surf, self.rotation)
        centre = Vector(surf.get_width()/2, surf.get_height()/2)
        pos = self.pos + (centre - Vector(self.width/2, self.height/2).rotated(self._rotation))
        #pos = self.pos.x + (surf.get_width() - og_width)/2, self.pos.y + (surf.get_height() - og_height)/2
        game.WIN.blit(surf, pos.to_tuple())
        x, y, width, height = surf.get_rect()
        x += pos.x
        y += pos.y
        pygame.draw.rect(game.WIN, game.RED, (x, y, width, height), width=2)"""
        surf = pygame.Surface((self.width, self.height), flags=pygame.SRCALPHA)
        pygame.draw.rect(surf, self.colour, (0, 0, self.width, self.height), width=self.outline)
        surf = pygame.transform.rotate(surf, self.rotation)
        pos = self.pos - Vector(surf.get_width()/2, surf.get_height()/2)
        game.WIN.blit(surf, pos.to_tuple())
