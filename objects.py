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
    __slots__ = ("pos", "colour")
    def __init__(self, pos: Vector, colour: Colour = game.WHITE) -> None:
        self.pos = pos
        self.colour = colour



class Particle(Object):
    """
    `size` is the radius, NOTE: this is purely visual, the particle is a single point
    """
    __slots__ = ("size", "velocity")
    def __init__(self, pos: Vector, size: int = 10, colour: Colour = game.BLUE) -> None:
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
        # Air resistance
        if self.velocity:
            # Reduce velocity proportional to velocity
            self.velocity.set_magnitude(self.velocity.magnitude() * (1 - delta_time * game.AIR_RESISTANCE))
            # Reduce velocity by a small amount so particle will completely stop if near 0 speed
            self.velocity.set_magnitude(max(0, self.velocity.magnitude() - 0.1*delta_time))

        # Gravity
        self.velocity.y += game.GRAVITY * delta_time

        # Move
        self.pos += self.velocity * delta_time

        # Handle collision
        self.collide()

    def draw(self) -> None:
        pygame.draw.circle(game.WIN, self.colour, self.pos.to_tuple(), self.size)



class SoftBodyParticle(Particle):
    __slots__ = ("neighbours")
    def __init__(self, pos: Vector, size: int = 10, colour: Colour = game.CYAN) -> None:
        super().__init__(pos, size, colour)
        self.neighbours: list[list[SoftBodyParticle, float]] = []

    def internal_collide_velocity(self) -> float:
        for obj in game.OBJECTS:
            if not isinstance(obj, SoftBody): continue

            for particle in obj.particles:
                if particle == self: continue
                if self.pos.distance_to(particle.pos) < 2*self.size:
                    normal = self.pos - particle.pos

                    """# Reflect velocity through normal
                    tangent = normal.rotated(math.pi/2)
                    line_angle = tangent.get_angle()
                    vel_angle = self.velocity.get_angle()
                    angle_diff = vel_angle - line_angle
                    self.velocity.rotate(2*angle_diff)  # 1 diff is parallel to line, 2 diff goes away from line
                    self.velocity *= 1  # Dampen by 50%"""
                    self.velocity += normal

    def internal_collide_position(self) -> float:
        for obj in game.OBJECTS:
            if not isinstance(obj, SoftBody): continue

            for particle in obj.particles:
                if particle == self: continue
                if self.pos.distance_to(particle.pos) < 2*self.size:
                    normal = self.pos - particle.pos

                    # Move position outside of particle radius
                    normal.set_magnitude(2*self.size - self.pos.distance_to(particle.pos) + 0)
                    self.pos += normal

    def dampen(self, neighbour: SoftBodyParticle, force: float) -> float:
        speed = neighbour.velocity.magnitude() - self.velocity.magnitude()
        if force > 0:
            return max(0, force + speed * game.SPRING_DAMPENING)

        else:
            return min(0, force - speed * game.SPRING_DAMPENING)

    def update_springs(self, delta_time: float) -> None:
        """Accelerate this Particle with the Force from the springs connected to it's neighbours"""
        for neighbour, length in self.neighbours:
            distance = self.pos.distance_to(neighbour.pos)
            extension = distance - length
            force = game.SPRING_COEFFICIENT * extension / length
            force = self.dampen(neighbour, force)
            acceleration = neighbour.pos - self.pos
            acceleration.set_magnitude(force)  # Acceleration = Force, as mass == 1
            self.velocity += acceleration * delta_time

    def draw_springs(self) -> None:
        for neighbour, _ in self.neighbours:
            pygame.draw.line(game.WIN, game.CYAN, self.pos.to_tuple(), neighbour.pos.to_tuple(), width=3)



class ImmovableSoftBodyParticle(SoftBodyParticle):
    def update(self, delta_time: float) -> None:
        pass

    def update_springs(self, delta_time: float) -> None:
        pass



class SoftBody(Object):
    """
    Creates a lattice structure of SoftBodyParticles, in a square shape e.g. 8 neighbours per particle

    The SoftBodyParticles are spawned in a distance of `game.SPRING_LENGTH` from each other

    `pos` is the position of the top left particle

    `width` and `height` are the number of particles of the dimensions of the SoftBody
    """
    __slots__ = ("width", "height", "particles")
    def __init__(self, pos: Vector, width: int, height: int, colour: tuple[int, int, int] = game.RED) -> None:
        super().__init__(pos, colour)
        self.width = width
        self.height = height
        self.particles: list[SoftBodyParticle] = []
        self.spawn_particles()

    def spawn_particles(self) -> None:
        # Create a list of particles at the correct positions
        particles: list[list[SoftBodyParticle]] = []
        for x in range(self.width):
            particles.append([])
            for y in range(self.height):
                pos = Vector(self.pos.x + x*game.SPRING_LENGTH, self.pos.y + y* game.SPRING_LENGTH)
                particles[x].append(SoftBodyParticle(pos, colour=self.colour))

        # Set the neighbours of each particle and add the particle to self.particles
        for x in range(self.width):
            for y in range(self.height):
                particle = particles[x][y]

                # Top, right, bottom and left springs
                if x > 0: particle.neighbours.append([particles[x-1][y], game.SPRING_LENGTH])
                if y > 0: particle.neighbours.append([particles[x][y-1], game.SPRING_LENGTH])
                if x < self.width-1: particle.neighbours.append([particles[x+1][y], game.SPRING_LENGTH])
                if y < self.height-1: particle.neighbours.append([particles[x][y+1], game.SPRING_LENGTH])

                # Diagonal springs, length of spring is longer
                if x > 0 and y > 0: particle.neighbours.append([particles[x-1][y-1], 2**0.5*game.SPRING_LENGTH])
                if x < self.width-1 and y > 0: particle.neighbours.append([particles[x+1][y-1], 2**0.5*game.SPRING_LENGTH])
                if x > 0 and y < self.height-1: particle.neighbours.append([particles[x-1][y+1], 2**0.5*game.SPRING_LENGTH])
                if x < self.width-1 and y < self.height-1: particle.neighbours.append([particles[x+1][y+1], 2**0.5*game.SPRING_LENGTH])

                self.particles.append(particle)

    def update(self, delta_time: float) -> None:
        # The spring acceleration for all particles must be calculated before moving any particles
        for particle in self.particles:
            particle.update_springs(delta_time)

        """for particle in self.particles:
            particle.internal_collide_velocity()

        for particle in self.particles:
            particle.internal_collide_position()"""

        for particle in self.particles:
            particle.update(delta_time)

    def draw_outline(self) -> None:
        particles: list[SoftBodyParticle] = []
        for particle in self.particles:
            if len(particle.neighbours) < 8:
                particles.append(particle)

        particles = [particle.pos.to_tuple() for particle in particles]
        pygame.draw.lines(game.WIN, game.CYAN, False, particles[:self.height], width=6)
        pygame.draw.lines(game.WIN, game.CYAN, False, particles[-self.height:], width=6)
        a, b = [particles[0]], [particles[self.height-1]]
        x = False
        for particle in particles[self.height:-self.height]:
            x = not x
            if x: a.append(particle)
            else: b.append(particle)
        a.append(particles[-self.height])
        b.append(particles[-1])
        pygame.draw.lines(game.WIN, game.CYAN, False, a, width=6)
        pygame.draw.lines(game.WIN, game.CYAN, False, b, width=6)

    def draw(self) -> None:
        if game.OUTLINE:
            self.draw_outline()

        else:
            for particle in self.particles:
                particle.draw_springs()

            for particle in self.particles:
                particle.draw()



class CircularSoftBody(SoftBody):
    """
    `width` is number of layers

    `height` is number of particles per layer
    """
    def spawn_particles(self) -> None:
        particles: list[list[SoftBodyParticle]] = []
        angle = math.tau / self.height
        for layer in range(self.width):
            particles.append([])
            length = game.SPRING_LENGTH * (layer+1)
            for i in range(self.height):
                pos = self.pos + Vector(length*math.sin(i*angle), length*math.cos(i*angle))
                particles[layer].append(SoftBodyParticle(pos, colour=self.colour))

        #middle_particle = ImmovableSoftBodyParticle(self.pos, colour=game.GREEN)
        middle_particle = SoftBodyParticle(self.pos, colour=self.colour)

        for idx, layer in enumerate(particles):
            adjacent_length = layer[0].pos.distance_to(layer[1].pos)
            if idx != 0: inner_diagonal_length = layer[0].pos.distance_to(particles[idx-1][1].pos)
            if idx != self.width-1: outer_diagonal_length = layer[0].pos.distance_to(particles[idx+1][1].pos)
            for i, particle in enumerate(layer):
                # Left particle
                if i == 0: particle.neighbours.append([layer[-1], adjacent_length])
                else: particle.neighbours.append([layer[i-1], adjacent_length])

                # Right particle
                if i == self.height-1: particle.neighbours.append([layer[0], adjacent_length])
                else: particle.neighbours.append([layer[i+1], adjacent_length])

                # Inner particles
                if idx == 0: particle.neighbours.append([middle_particle, game.SPRING_LENGTH])
                else:
                    # Middle
                    particle.neighbours.append([particles[idx-1][i], game.SPRING_LENGTH])
                    # Left
                    if i == 0: particle.neighbours.append([particles[idx-1][-1], inner_diagonal_length])
                    else: particle.neighbours.append([particles[idx-1][i-1], inner_diagonal_length])
                    # Right
                    if i == self.height-1: particle.neighbours.append([particles[idx-1][0], inner_diagonal_length])
                    else: particle.neighbours.append([particles[idx-1][i+1], inner_diagonal_length])

                # Outer particle
                if idx != self.width-1:
                    # Middle
                    particle.neighbours.append([particles[idx+1][i], game.SPRING_LENGTH])
                    # Left
                    if i == 0: particle.neighbours.append([particles[idx+1][-1], outer_diagonal_length])
                    else: particle.neighbours.append([particles[idx+1][i-1], outer_diagonal_length])
                    # Right
                    if i == self.height-1: particle.neighbours.append([particles[idx+1][0], outer_diagonal_length])
                    else: particle.neighbours.append([particles[idx+1][i+1], outer_diagonal_length])

        for particle in particles[0]:
            middle_particle.neighbours.append([particle, game.SPRING_LENGTH])
        self.particles.append(middle_particle)

        for layer in particles:
            for particle in layer:
                self.particles.append(particle)

    def draw_outline(self) -> None:
        pygame.draw.lines(game.WIN, game.CYAN, True, [particle.pos.to_tuple() for particle in self.particles[-self.height:]], width=6)



class Rect(Object):
    """
    `pos` is centre of rectangle

    `rotation` is in degrees

    `outline` is the width of the outline, 0 is filled rectangle
    """
    __slots__ = ("width", "height", "_rotation", "outline", "surf", "tl", "tr", "br", "bl")
    def __init__(self, pos: Vector, width: int, height: int, rotation: float = 0, colour: Colour = game.WHITE, outline: int = 5) -> None:
        super().__init__(pos, colour)
        self.width = width
        self.height = height
        self.rotation = rotation
        self.outline = outline
        self.surf = self.create_surface()
        self.update_corners()

    def __repr__(self) -> str:
        return f"Rect({self.pos}, {self.width}, {self.height})"

    def update_corners(self) -> None:
        self.tl = self.pos + Vector(-self.width/2, -self.height/2).rotated(self._rotation)
        self.tr = self.pos + Vector(self.width/2, -self.height/2).rotated(self._rotation)
        self.br = self.pos + Vector(self.width/2, self.height/2).rotated(self._rotation)
        self.bl = self.pos + Vector(-self.width/2, self.height/2).rotated(self._rotation)

    @property
    def rotation(self) -> float:
        """Rect.rotation is degrees, Rect._rotation is radians"""
        return math.degrees(self._rotation)

    @rotation.setter
    def rotation(self, new_rotation) -> None:
        self._rotation = math.radians(new_rotation)

    @property
    def corners(self) -> tuple[Vector]:
        return self.tl, self.tr, self.bl, self.br

    def create_surface(self) -> pygame.Surface:
        surf = pygame.Surface((self.width, self.height), flags=pygame.SRCALPHA)
        pygame.draw.rect(surf, self.colour, (0, 0, self.width, self.height), width=self.outline)
        surf = pygame.transform.rotozoom(surf, self.rotation, 1)
        return surf

    def draw(self) -> None:
        pos = self.pos - Vector(self.surf.get_width()/2, self.surf.get_height()/2)
        game.WIN.blit(self.surf, pos.to_tuple())



class Player_Spring(Object):
    __slots__ = ("particle")
    def __init__(self, pos: Vector, particle: SoftBodyParticle, colour: Colour = game.YELLOW) -> None:
        super().__init__(pos, colour)
        self.particle = particle

    def update(self, delta_time: float) -> None:
        if game.FOLLOW_MOUSE:
            x, y = pygame.mouse.get_pos()
            vec = Vector(x, y) - self.particle.pos
            self.particle.velocity += vec * game.PLAYER_SPRING_COEFFICIENT * delta_time

    def draw(self) -> None:
        if game.FOLLOW_MOUSE:
            x, y = pygame.mouse.get_pos()
            pygame.draw.line(game.WIN, self.colour, (x, y), self.particle.pos.to_tuple(), width=3)



class Player_Pusher(Object):
    def update(self, delta_time: float) -> None:
        if game.PUSH_PARTICLES:
            x, y = pygame.mouse.get_pos()
            pos = Vector(x, y)
            for obj in game.OBJECTS:
                if not isinstance(obj, SoftBody): continue
                for particle in obj.particles:
                    if pos.distance_to(particle.pos) < game.PUSH_RANGE:
                        vec = particle.pos - pos
                        vec.set_magnitude(delta_time * game.PUSH_POWER)
                        particle.velocity += vec

    def draw(self) -> None:
        if game.PUSH_PARTICLES:
            x, y = pygame.mouse.get_pos()
            surf = pygame.Surface((2*game.PUSH_RANGE, 2*game.PUSH_RANGE), flags=pygame.SRCALPHA)
            pygame.draw.circle(surf, (*game.LIGHT_GREY, 100), (game.PUSH_RANGE, game.PUSH_RANGE), game.PUSH_RANGE)
            game.WIN.blit(surf, (x - game.PUSH_RANGE, y - game.PUSH_RANGE))
