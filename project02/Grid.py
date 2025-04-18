class Grid:

    def __init__(self, width, height, first = None):
        self.width = width
        self.height = height
        self.array = []
        for y in range(height):
            self.array.append([None] * width)

    def in_bounds(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return True
        return False

    def get(self, x, y):
        if self.in_bounds(x, y):
            return self.array[y][x]
        else:
            raise IndexError("The location is out of bounds.")

    def set(self, x, y, val):
        if self.in_bounds(x, y):
            self.array[y][x] = val
        else:
            raise IndexError("The location is out of bounds.")
        

    @staticmethod
    def check_list_malformed(lst):
        if not isinstance(lst, list):
            raise ValueError("Input must be a non-empty list of lists.")
        elif not lst:
            raise ValueError("Input must be a non-empty")
        for item in lst:
            if not isinstance(item, list) or len(item) != len(lst[0]):
                raise ValueError("All items in list must be lists of the same length.")
        return True
    
    @staticmethod
    def build(lst):
        if Grid.check_list_malformed(lst):
            pass
        width = len(lst[0])
        height = len(lst)
        grid = Grid(width, height)
        for y in range(height):
            for x in range(width):
                grid.set(x, y, lst[y][x])
        return grid
    

    def copy(self):
        grid = Grid(self.width, self.height)
        for y in range(self.height):
            for x in range(self.width):
                grid.set(x, y, self.get(x, y))
        return grid
        

    def __str__(self):
        try:
            return f"Grid({self.height}, {self.width}, first = {self.array[0][0]})"
        except IndexError:
            return "The location is out of bounds."

    def __repr__(self):
        try:
            return f"Grid.build({self.array})"
        except IndexError:
            return "The location is out of bounds."

    def __eq__(self, other):
        if isinstance(other, Grid):
            return self.array == other.array
        elif isinstance(other, list):
            return self.array == other
        return False