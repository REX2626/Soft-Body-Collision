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

    def dot(self, other: Vector) -> float:
        """Returns the dot product of `self` and `other`"""
        return self.x*other.x + self.y * other.y

    def distance_to(self, other: Vector) -> float:
        """Returns the Euclidean distance between this Vector and other"""
        return (self - other).magnitude()

    def copy(self) -> Vector:
        return Vector(self.x, self.y)

    def in_range(self, x: float, y: float, width: float, height: float) -> bool:
        return self.x >= x and self.x <= x + width and self.y >= y and self.y <= y + height

    def to_tuple(self) -> tuple:
        return self.x, self.y



class Object():
    def __init__(self, pos: Vector, colour: Colour = game.WHITE) -> None:
        self.pos = pos
        self.colour = colour



class Particle(Object):
    """
    `size` is the radius, NOTE: this is purely visual, the particle is a single point
    """
    def __init__(self, pos: Vector, size: int = 8, colour: Colour = game.RED) -> None:
        super().__init__(pos, colour)
        self.size = size
        self.velocity = Vector(0, 0)

    def collide(self) -> None:
        for obj in game.OBJECTS:
            if not isinstance(obj, Rect): continue

            # NOTE: This method for collision should work for quadrilaterals in general

            # Use dot product to find closest point on Rect line to particle
            # t is the ratio from start of line to end of line
            # if  0 < t < 1  then there is a valid closest point

            top_line = obj.tr - obj.tl
            t_top = top_line.dot(self.pos - obj.tl) / top_line.dot(top_line)  # t = (a->b).(a->c) / (magnitude of top_line ^2)
            if not 0 < t_top < 1: continue

            right_line = obj.br - obj.tr
            t_right = right_line.dot(self.pos - obj.tr) / right_line.dot(right_line)
            if not 0 < t_right < 1: continue

            bottom_line = obj.bl - obj.br
            t_bottom = bottom_line.dot(self.pos - obj.br) / bottom_line.dot(bottom_line)
            if not 0 < t_bottom < 1: continue

            left_line = obj.tl - obj.bl
            t_left = left_line.dot(self.pos - obj.bl) / left_line.dot(left_line)
            if not 0 < t_left < 1: continue

            # The particle now must be inside the rect
            # Move the particle's to the closest point from top, right, bottom and left

            top  = obj.tl + t_top * top_line
            right = obj.tr + t_right * right_line
            bottom = obj.br + t_bottom * bottom_line
            left = obj.bl + t_left * left_line

            closest = min([top, top_line], [right, right_line], [bottom, bottom_line], [left, left_line],
                          key=lambda pair: self.pos.distance_to(pair[0]))

            self.pos = closest[0]

            # Reflect this particle's velocity across the normal to the line our pos is at
            line = closest[1]
            line_angle = line.get_angle()
            vel_angle = self.velocity.get_angle()
            angle_diff = vel_angle - line_angle
            self.velocity.rotate(2*angle_diff)  # 1 diff is parallel to line, 2 diff goes away from line

    def update(self, delta_time: float) -> None:
        # Gravity
        self.velocity.y += game.GRAVITY * delta_time

        # Move
        self.pos += self.velocity * delta_time

        # Handle collision
        self.collide()

    def draw(self) -> None:
        pygame.draw.circle(game.WIN, self.colour, self.pos.to_tuple(), self.size)



class Rect(Object):
    """
    `pos` is centre of rectangle

    `rotation` is in degrees

    `outline` is the width of the outline, 0 is filled rectangle
    """
    def __init__(self, pos: Vector, width: int, height: int, rotation: float = 0, colour: Colour = game.WHITE, outline: int = 0) -> None:
        super().__init__(pos, colour)
        self.width = width
        self.height = height
        self.rotation = rotation
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

    def draw(self) -> None:
        surf = pygame.Surface((self.width, self.height), flags=pygame.SRCALPHA)
        pygame.draw.rect(surf, self.colour, (0, 0, self.width, self.height), width=self.outline)
        surf = pygame.transform.rotate(surf, self.rotation)
        pos = self.pos - Vector(surf.get_width()/2, surf.get_height()/2)
        game.WIN.blit(surf, pos.to_tuple())
