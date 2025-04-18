class Particle():

    def __init__(self, grid, x=0, y=0):
        self.grid = grid
        self.x = x
        self.y = y

    def __str__(self):
        return f"{type(self).__name__}({self.x},{self.y})"

    def move(self):
        desired_position = self.physics()
        if not desired_position:
            return
        else:
            desired_x, desired_y = desired_position
            self.grid.set(self.x, self.y, None)
            self.x = desired_x
            self.y = desired_y
            self.grid.set(self.x, self.y, self)