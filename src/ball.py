"""Ball File
"""


class Ball:
    """ This is the Ball class """
    def __init__(self, x, y, d, i, c):
        self.x = x
        self.y = y
        self.origin_x = x
        self.origin_y = y
        self.radius = d
        self.index = i
        self.colour = c

        self.health = 1
        self.magnitude = -10
        self.velocity = (1, 1)
        self.spawned = False
        self.delay = 0

    def get_position(self):
        """ Return the coordinates of the ball """
        return (self.x, self.y)

    def get_new_position(self):
        """ Return the coordinates after movement """
        return (
            self.x + self.velocity[0],
            self.y + self.velocity[1]
        )

    def get_radius(self):
        """ Return the radius of the ball """
        return self.radius

    def get_colour(self):
        """ Return the colour of the ball """
        return self.colour

    def get_velocity(self):
        """ Return the velocity of the ball """
        return self.velocity

    def get_health(self):
        """ Return the health of the balll """
        return self.health

    def get_delay(self):
        """ Return the delay of the ball """
        return self.delay

    def is_spawned(self):
        """ Return whether ball has finished spawning """
        return self.spawned

    def invert_x_velocity(self):
        """ Invert the velocity in the x direction """
        self.velocity = (self.velocity[0] * -1, self.velocity[1])

    def invert_y_velocity(self):
        """ Invert the velocity in the x direction """
        self.velocity = (self.velocity[0], self.velocity[1] * -1)

    def set_position(self, position):
        """ Set the position of the ball """
        self.x, self.y = position

    def set_velocity(self, x, y):
        """ Set the velocity of the ball """
        self.velocity = (self.magnitude * x, self.magnitude * y)

    def set_spawned(self):
        """ Set ball span to true """
        self.spawned = True

    def set_delay(self, time):
        """ Set the delay before moving """
        self.delay = time + (100 * self.index)

    def hit_floor(self):
        """ Reduce health of the ball """
        if self.spawned:
            self.health -= 1

    def reset(self):
        """ Reset the ball to the origin """
        self.set_velocity(0, 0)
        self.set_position((self.origin_x, self.origin_y))
