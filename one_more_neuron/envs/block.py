"""Block File
"""


class Block:
    """ This is the Block class """
    def __init__(self, x, y, w, h, t, e,c):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.gap = t
        self.health = e
        self.orig_health = e
        self.colour = c

    def get_position(self):
        """ Return the coordinates of the block """
        return (self.x, self.y)

    def get_size(self):
        """ Return the size of the block """
        return (self.width, self.height)

    def get_colour(self):
        """ Return the colour of the block """
        return self.colour

    def get_health(self):
        """ Return the health of the block """
        return self.health

    def get_original_health(self):
        """ Return the original health of the block """
        return self.orig_health

    def get_gap(self):
        """ Return the gap between blocks """
        return self.gap

    def get_center_position(self):
        """ Return the center of the block """
        x, y = self.get_coords()
        return (x + (self.width / 2), y + self.height / 2)

    def get_coords(self):
        """ Return the coords of the block """
        return (
            self.gap + (self.width + self.gap) * self.x,
            self.gap + (self.height + self.gap) * self.y
        )

    def hit_ball(self):
        """ Reduce health of the block """
        self.health -= 1

    def move_down(self):
        """ Increase the y coordinate of the block """
        self.y += 1
