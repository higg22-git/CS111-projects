from Particle import Particle

class Sand(Particle):

    def is_move_ok(self, x, y):
        if not self.grid.in_bounds(x, y):
            return False
        elif self.grid.get(x, y) is not None:
            return False
        elif self.x != x:
            if self.grid.get(x, y - 1) is not None:
                return False
        return True
        
    def physics(self):
        if self.is_move_ok(self.x, self.y + 1):
            return self.x, self.y + 1
        elif self.is_move_ok(self.x - 1, self.y + 1):
            return self.x - 1, self.y + 1
        elif self.is_move_ok(self.x + 1, self.y + 1):
            return self.x + 1, self.y + 1
        return None

class Rock(Particle):
    
    def physics(self):
        return None
    
class Bubble(Particle):

    def is_move_ok(self, x, y):
        if not self.grid.in_bounds(x, y):
            return False
        elif self.grid.get(x, y) is not None:
            return False
        elif self.x != x:
            if self.grid.get(x, y + 1) is not None:
                return False
        return True
    
    def physics(self):
        if self.is_move_ok(self.x, self.y - 1):
            return self.x, self.y - 1
        elif self.is_move_ok(self.x + 1, self.y - 1):
            return self.x + 1, self.y - 1
        elif self.is_move_ok(self.x - 1, self.y - 1):
            return self.x - 1, self.y - 1
        return None
