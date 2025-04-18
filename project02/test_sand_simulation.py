from byu_pytest_utils import max_score, with_import
from functools import cache


@cache
def make_wrapper_class(Object):
    class ObjectWrapper(Object):
        def __eq__(self, other):
            if isinstance(other, (ObjectWrapper)):
                return str(self) == str(other)
            else:
                return False

    return ObjectWrapper


def build_grid(Grid, Sand, Rock, Bubble, lst):
    SandWrapper = make_wrapper_class(Sand)
    RockWrapper = make_wrapper_class(Rock)
    BubbleWrapper = make_wrapper_class(Bubble)

    grid = Grid.build(lst)
    for y in range(grid.height):
        for x in range(grid.width):
            if grid.get(x, y) == "s":
                grid.set(x, y, SandWrapper(grid, x, y))
            elif grid.get(x, y) == "r":
                grid.set(x, y, RockWrapper(grid, x, y))
            elif grid.get(x, y) == "b":
                grid.set(x, y, BubbleWrapper(grid, x, y))

    def fancy_grid_toString(self):
 
        def get_particle_string(obj):
            if isinstance(obj, (Sand, SandWrapper)):
                return "s"
            elif isinstance(obj, (Rock, RockWrapper)):
                return "r"
            elif isinstance(obj, (Bubble, BubbleWrapper)):
                return "b"
            elif obj is None:
                return " "
            else:
                return "?"

        assert isinstance(self, Grid), "Either you did this on purpose, or something went horribly wrong"
        s = "\n"  # We lead with a newline to get off a possibly indented line
        for y in range(self.height):
            for x in range(self.width):
                s += "|" + get_particle_string(self.get(x, y))
            s += "|\n"
        return s

    Grid.__str__ = fancy_grid_toString

    return grid


def construct_all_objects_list(Sand, Rock, Bubble, grid):
    all_grid_objects = []
    for y in range(grid.height):
        for x in range(grid.width):
            space = grid.get(x, y)
            if isinstance(space, (Sand, Rock, Bubble)):
                all_grid_objects.append(space)
    return all_grid_objects


def wrap_all_grid_objects(all_grid_objects, grid, Sand, Rock, Bubble):
    Sandwrapper = make_wrapper_class(Sand)
    Rockwrapper = make_wrapper_class(Rock)
    Bubblewrapper = make_wrapper_class(Bubble)
    new_all_grid_objects = []
    for object in all_grid_objects:
        if isinstance(object, Sand):
            grid.set(object.x, object.y, Sandwrapper(object.grid, object.x, object.y))
            new_all_grid_objects.append(Sandwrapper(object.grid, object.x, object.y))
        elif isinstance(object, Rock):
            grid.set(object.x, object.y, Rockwrapper(object.grid, object.x, object.y))
            new_all_grid_objects.append(Rockwrapper(object.grid, object.x, object.y))
        elif isinstance(object, Bubble):
            grid.set(object.x, object.y, Bubblewrapper(object.grid, object.x, object.y))
            new_all_grid_objects.append(Bubblewrapper(object.grid, object.x, object.y))
    return new_all_grid_objects


@max_score(1)
@with_import('Grid_Objects', 'Sand')
@with_import('Grid', 'Grid')
def test_sand_str(Grid, Sand):
    grid = Grid(6, 6)
    assert str(Sand(grid, 1, 2)) == 'Sand(1,2)'
    assert str(Sand(grid, 5, 3)) == 'Sand(5,3)'

@max_score(1)
@with_import('Grid_Objects', 'Rock')
@with_import('Grid', 'Grid')
def test_rock_str(Grid, Rock):
    grid = Grid(6, 6)
    assert str(Rock(grid, 1, 2)) == 'Rock(1,2)'
    assert str(Rock(grid, 5, 3)) == 'Rock(5,3)'

@max_score(1)
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_bubble_str(Grid, Bubble):
    grid = Grid(6, 6)
    assert str(Bubble(grid, 1, 2)) == 'Bubble(1,2)'
    assert str(Bubble(grid, 5, 3)) == 'Bubble(5,3)'


@max_score(1)
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_rock_physics(Grid, Bubble, Rock, Sand):
    grid = build_grid(Grid, Sand, Rock, Bubble, 
                      [[None, None, None],
                       [None, 'r', None],
                       [None, None, None]])
    assert (actual := grid.get(1, 1).physics()) == (expected := None), \
        f"got {actual} instead of {expected} with grid: {grid}"


@max_score(1.5)
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_sand_physics_out_of_bounds(Grid, Bubble, Rock, Sand):
    grid = build_grid(Grid, Sand, Rock, Bubble, [['s']])
    assert (actual := grid.get(0, 0).physics()) == (expected := None), \
        f"got {actual} instead of {expected} with grid: {grid}"
    
@max_score(1.5)
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_bubble_physics_out_of_bounds(Grid, Bubble, Rock, Sand):
    grid = build_grid(Grid, Sand, Rock, Bubble, [['b']])
    assert (actual := grid.get(0, 0).physics()) == (expected := None), \
        f"got {actual} instead of {expected} with grid: {grid}"


@max_score(1.5)
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_sand_physics_cant_move(Grid, Bubble, Rock, Sand):
    grid = build_grid(
        Grid, Sand, Rock, Bubble,
        [[None, 's', None],
         ['s', 's', 's']]
    )
    assert (actual := grid.get(1, 0).physics()) == (expected := None), \
        f"got {actual} instead of {expected} with grid: {grid}"
    
@max_score(1.5)
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_bubble_physics_cant_move(Grid, Bubble, Rock, Sand):
    grid = build_grid(
        Grid, Sand, Rock, Bubble,
        [['b', 'b', 'b'],
         [None, 'b', None]]
    )
    assert (actual := grid.get(1, 1).physics()) == (expected := None), \
        f"got {actual} instead of {expected} with grid: {grid}"

    
@max_score(1.5)
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_sand_physics_straight_down(Grid, Bubble, Rock, Sand):
    grid = build_grid(
        Grid, Sand, Rock, Bubble,
        [[None, 's', None], 
         [None, None, None]]
    )
    assert (actual := grid.get(1, 0).physics()) == (expected := (1, 1)), \
        f"got {actual} instead of {expected} with grid: {grid}"
    
@max_score(1.5)
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_bubble_physics_straight_up(Grid, Bubble, Rock, Sand):
    grid = build_grid(
        Grid, Sand, Rock, Bubble,
        [[None, None, None], 
         [None, 'b', None]]
    )
    assert (actual := grid.get(1, 1).physics()) == (expected := (1, 0)), \
        f"got {actual} instead of {expected} with grid: {grid}"

    
@max_score(1.5)
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_sand_physics_down_left(Grid, Bubble, Rock, Sand):
    grid = build_grid(
        Grid, Sand, Rock, Bubble,
        [[None, 's', None], 
         [None, 'r', None]]
    )
    assert (actual := grid.get(1, 0).physics()) == (expected := (0, 1)), \
        f"got {actual} instead of {expected} with grid: {grid}"
    
@max_score(1.5)
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_bubble_physics_up_right(Grid, Bubble, Rock, Sand):
    grid = build_grid(
        Grid, Sand, Rock, Bubble,
        [[None, 'r', None], 
         [None, 'b', None]]
    )
    assert (actual := grid.get(1, 1).physics()) == (expected := (2, 0)), \
        f"got {actual} instead of {expected} with grid: {grid}"
    
    
@max_score(1.5)
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_sand_physics_down_right(Grid, Bubble, Rock, Sand):
    grid = build_grid(
        Grid, Sand, Rock, Bubble,
        [['r', 's', None], 
         ['r', 's', None]]
    )
    assert (actual := grid.get(1, 0).physics()) == (expected := (2, 1)), \
        f"got {actual} instead of {expected} with grid: {grid}"
    
@max_score(1.5)
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_bubble_physics_up_left(Grid, Bubble, Rock, Sand):
    grid = build_grid(
        Grid, Sand, Rock, Bubble,
        [[None, 'b', 'r'], 
         [None, 'b', 'r']]
    )
    assert (actual := grid.get(1, 1).physics()) == (expected := (0, 0)), \
        f"got {actual} instead of {expected} with grid: {grid}"
    
    
@max_score(1.5)
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_sand_physics_corner_rule(Grid, Bubble, Rock, Sand):
    grid = build_grid(
        Grid, Sand, Rock, Bubble,
        [['r', 's', 'r'], 
        [None, 'r', None]]
    )
    assert (actual := grid.get(1, 0).physics()) == (expected := None), \
        f"got {actual} instead of {expected} with grid: {grid}"
    
@max_score(1.5)
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_bubble_physics_corner_rule(Grid, Bubble, Rock, Sand):
    grid = build_grid(
        Grid, Sand, Rock, Bubble,
        [[None, 'r', None], 
        ['r', 'b', 's']]
    )
    assert (actual := grid.get(1, 1).physics()) == (expected := None), \
        f"got {actual} instead of {expected} with grid: {grid}"


@max_score(1)
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_sand_move_out_of_bounds(Grid, Bubble, Rock, Sand):
    key = build_grid(Grid, Sand, Rock, Bubble, [['s']])
    grid = build_grid(Grid, Sand, Rock, Bubble, [['s']])
    sand = grid.get(0, 0)
    sand.move()
    assert grid == key, f"grid does not match key\ngrid:{grid}\nkey:{key}"

@max_score(1)
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_bubble_move_out_of_bounds(Grid, Bubble, Rock, Sand):
    key = build_grid(Grid, Sand, Rock, Bubble, [['b']])
    grid = build_grid(Grid, Sand, Rock, Bubble, [['b']])
    bubble = grid.get(0, 0)
    bubble.move()
    assert grid == key, f"grid does not match key\ngrid:{grid}\nkey:{key}"


@max_score(1)
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_sand_move_cant_move(Grid, Bubble, Rock, Sand):
    key = build_grid(
        Grid, Sand, Rock, Bubble,
        [[None, 's', None],
         ['s', 's', 's']]
    )
    grid = build_grid(
        Grid, Sand, Rock, Bubble,
        [[None, 's', None],
         ['s', 's', 's']]
    )
    sand = grid.get(1, 0)
    sand.move()
    assert grid == key, f"grid does not match key\ngrid:{grid}\nkey:{key}"

@max_score(1)
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_bubble_move_cant_move(Grid, Bubble, Rock, Sand):
    key = build_grid(
        Grid, Sand, Rock, Bubble,
        [['b', 'b', 'b'],
         [None, 'b', None]]
    )
    grid = build_grid(
        Grid, Sand, Rock, Bubble,
        [['b', 'b', 'b'],
         [None, 'b', None]]
    )
    bubble = grid.get(1, 1)
    bubble.move()
    assert grid == key, f"grid does not match key\ngrid:{grid}\nkey:{key}"


@max_score(1)
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_sand_move_straight_down(Grid, Bubble, Rock, Sand):
    key = build_grid(Grid, Sand, Rock, Bubble,
        [[None, None, None], 
         [None, 's', None]])
    grid = build_grid(Grid, Sand, Rock, Bubble,
        [[None, 's', None], 
         [None, None, None]])
    sand = grid.get(1, 0)
    sand.move()
    assert grid == key, f"grid does not match key\ngrid:{grid}\nkey:{key}"

@max_score(1)
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_bubble_move_straight_up(Grid, Bubble, Rock, Sand):
    key = build_grid(Grid, Sand, Rock, Bubble,
        [[None, 'b', None], 
         [None, None, None]])
    grid = build_grid(Grid, Sand, Rock, Bubble,
        [[None, None, None], 
         [None, 'b', None]])
    bubble = grid.get(1, 1)
    bubble.move()
    assert grid == key, f"grid does not match key\ngrid:{grid}\nkey:{key}"


@max_score(1)
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_sand_move_down_left(Grid, Bubble, Rock, Sand):
    key = build_grid(Grid, Sand, Rock, Bubble,
    [[None, None, None], 
     ['s', 'r', None]])
    grid = build_grid(Grid, Sand, Rock, Bubble,
    [[None, 's', None], 
     [None, 'r', None]])
    sand = grid.get(1, 0)
    sand.move()
    assert grid == key, f"grid does not match key\ngrid:{grid}\nkey:{key}"

@max_score(1)
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_bubble_move_up_right(Grid, Bubble, Rock, Sand):
    key = build_grid(Grid, Sand, Rock, Bubble,
    [[None, 'r', 'b'], 
     [None, None, None]])
    grid = build_grid(Grid, Sand, Rock, Bubble,
    [[None, 'r', None], 
     [None, 'b', None]])
    bubble = grid.get(1, 1)
    bubble.move()
    assert grid == key, f"grid does not match key\ngrid:{grid}\nkey:{key}"


@max_score(1)
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_sand_move_down_right(Grid, Bubble, Rock, Sand):
    key = build_grid(Grid, Sand, Rock, Bubble,
    [['r', None, None],
     [None, None, None], 
     ['r', 's', 's']])
    grid = build_grid(Grid, Sand, Rock, Bubble,
    [['r', None, None],
     [None, 's', None], 
     ['r', 's', None]])
    sand = grid.get(1, 1)
    sand.move()
    assert grid == key, f"grid does not match key\ngrid:{grid}\nkey:{key}"

@max_score(1)
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_bubble_move_up_left(Grid, Bubble, Rock, Sand):
    key = build_grid(Grid, Sand, Rock, Bubble,
    [['b', 'b', 'r'],
     [None, None, None], 
     [None, None, 'r']])
    grid = build_grid(Grid, Sand, Rock, Bubble,
    [[None, 'b', 'r'],
     [None, 'b', None], 
     [None, None, 'r']])
    bubble = grid.get(1, 1)
    bubble.move()
    assert grid == key, f"grid does not match key\ngrid:{grid}\nkey:{key}"


@max_score(1)
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_sand_move_corner_rule(Grid, Bubble, Rock, Sand):
    key = build_grid(Grid, Sand, Rock, Bubble,
    [['r', 's', 'r'], 
     [None, 'r', None]])
    grid = build_grid(Grid, Sand, Rock, Bubble,
    [['r', 's', 'r'], 
     [None, 'r', None]])
    sand = grid.get(1, 0)
    sand.move()
    assert grid == key, f"grid does not match key\ngrid:{grid}\nkey:{key}"

@max_score(1)
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_bubble_move_corner_rule(Grid, Bubble, Rock, Sand):
    key = build_grid(Grid, Sand, Rock, Bubble,
    [[None, 'r', None], 
     ['r', 'b', 's']])
    grid = build_grid(Grid, Sand, Rock, Bubble,
    [[None, 'r', None], 
     ['r', 'b', 's']])
    bubble = grid.get(1, 1)
    bubble.move()
    assert grid == key, f"grid does not match key\ngrid:{grid}\nkey:{key}"


@max_score(6)
@with_import('Grid_Objects', 'Sand')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid', 'Grid')
def test_move_falling_example(Grid, Bubble, Rock, Sand):
    keys = [
        build_grid(
            Grid, Sand, Rock, Bubble,
            [[None, 'r', None, None, 'b', None],
             [None, 's', None, None, 'b', None],
             [None, 's', None, None, 'b', None],
             [None, 's', None, None, 'b', None],
             [None, 's', None, None, 'r', None]]
        ),
        build_grid(
            Grid, Sand, Rock, Bubble,
            [[None, 'r',  None, None, 'b',  'b'],
             [None, None, None, None, 'b',  None],
             [None, 's',  None, None, 'b',  None],
             [None, 's',  None, None, None, None],
             ['s',  's',  None, None, 'r',  None]]
        ),
        build_grid(
            Grid, Sand, Rock, Bubble,
            [[None, 'r',  None, 'b',  'b',  'b'],
             [None, None, None, None, 'b',  None],
             [None, None, None, None, None, None],
             [None, 's',  None, None, None, None],
             ['s',  's',  's',  None, 'r',  None]]
        ),
        build_grid(
            Grid, Sand, Rock, Bubble,
            [[None, 'r',  None, 'b',  'b',  'b'],
             [None, None, None, None, 'b',  None],
             [None, None, None, None, None, None],
             [None, 's',  None, None, None, None],
             ['s',  's',  's',  None, 'r',  None]]
        )
    ]
    grid = build_grid(
        Grid, Sand, Rock, Bubble,
        [[None, 'r', None, None, 'b', None],
         [None, 's', None, None, 'b', None],
         [None, 's', None, None, 'b', None],
         [None, 's', None, None, 'b', None],
         [None, 's', None, None, 'r', None]]
    )
    assert grid == keys[0], f"Test setups do not match. There's probably something wrong with the tests. Let your TAs know."
    for key in keys[1:]:
        for y in (range(grid.height)):
            for x in range(grid.width):
                elem = grid.get(x, y)
                if isinstance(elem, Bubble):
                    elem.move()
        for y in reversed(range(grid.height)):
            for x in range(grid.width):
                elem = grid.get(x, y)
                if isinstance(elem, (Sand, Rock)):
                    elem.move()
        assert grid == key, f"grid does not match key\ngrid:{grid}\nkey:{key}"


@max_score(15)
@with_import('sand_simulation', 'all_grid_objects')
@with_import('sand_simulation', 'add_object')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Sand')
@with_import('Grid', 'Grid')
def test_add_objects(Grid, Sand, Rock, Bubble, add_object, all_grid_objects):
    key_grid = build_grid(
        Grid, Sand, Rock, Bubble,
        [[None, 's', 'b'],
         ['s', 'b', None],
         [None, 'r', 's']]
    )
    key_all_grid_objects = construct_all_objects_list(Sand, Rock, Bubble, key_grid)

    grid = build_grid(
        Grid, Sand, Rock, Bubble,
        [[None, None, None], 
         [None, None, None], 
         [None, None, None]])
    add_object(grid, Sand, 1, 0)
    add_object(grid, Bubble, 2, 0)
    add_object(grid, Sand, 0, 1)
    add_object(grid, Bubble, 1, 1)
    add_object(grid, Rock, 1, 2)
    add_object(grid, Sand, 2, 2)

    all_grid_objects = wrap_all_grid_objects(all_grid_objects, grid, Sand, Rock, Bubble)

    assert grid == key_grid, f"grid does not match key\ngrid:{grid}\nkey:{key_grid}"
    # have to sort lists before comparison in case order of objects is different
    all_grid_objects.sort(key=lambda object:(object.x, object.y))
    key_all_grid_objects.sort(key=lambda object:(object.x, object.y))
    assert all_grid_objects == key_all_grid_objects, "all_grid_objects list does not match key"

    add_object(grid, Rock, 1, 0)
    add_object(grid, Sand, 1, 2)
    add_object(grid, Bubble, 2, 2)
    assert len(all_grid_objects) == 6  # the three adds should have failed


@max_score(15)
@with_import('sand_simulation', 'all_grid_objects')
@with_import('sand_simulation', 'remove_object')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Sand')
@with_import('Grid', 'Grid')
def test_remove_objects(Grid, Sand, Rock, Bubble, remove_object, all_grid_objects):
    key_grid = build_grid(
        Grid, Sand, Rock, Bubble,
        [[None, 'b', None],
         ['s', None, None],
         [None, 'r', 's']]
    )
    key_all_grid_objects = construct_all_objects_list(Sand, Rock, Bubble, key_grid)

    grid = build_grid(
        Grid, Sand, Rock, Bubble,
        [['s', 'b', 'b'],
         ['s', 'b', 's'],
         ['r', 'r', 's']]
    )
    all_grid_objects[:] = construct_all_objects_list(Sand, Rock, Bubble, grid)

    remove_object(grid, 0, 0)
    remove_object(grid, 2, 0)
    remove_object(grid, 1, 1)
    remove_object(grid, 2, 1)
    remove_object(grid, 0, 2)


    assert grid == key_grid, f"grid does not match key\ngrid:{grid}\nkey:{key_grid}. Make sure you are accessing existing sand objects using grid.get()"
    all_grid_objects.sort(key=lambda object:(object.x, object.y))
    key_all_grid_objects.sort(key=lambda object:(object.x, object.y))
    assert all_grid_objects == key_all_grid_objects

    remove_object(grid, 0, 2)
    remove_object(grid, 2, 1)
    remove_object(grid, 1, 1)

    # the three removes should have failed
    assert len(all_grid_objects) == 4
    assert grid.get(0, 2) == None
    assert isinstance(grid.get(1, 2), Rock)


@max_score(10)
@with_import('sand_simulation', 'all_grid_objects')
@with_import('sand_simulation', 'do_whole_grid')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Sand')
@with_import('Grid', 'Grid')
def test_do_whole_grid_all_falling_rules(Grid, Sand, Rock, Bubble, do_whole_grid, all_grid_objects):
    key = build_grid(
        Grid, Sand, Rock, Bubble,
        [[None, 's', None, None, None, None, None, None, None],
         ['r',  's', 'r',  's' , 'r',  None, 's',  'r',  's'],
         [None, 'r', None, None, None, None, 'r',  None, None],
         ['r',  'b', 'r',  None, 'r',  'b' , 'b',  'b', 'r'],
         [None, 'b', None, None, None, None, None, None, None]]
    )
    key_all_grid_objects = construct_all_objects_list(Sand, Rock, Bubble, key)

    grid = build_grid(
        Grid, Sand, Rock, Bubble,
        [[None, 's', None, None, 's',  None, 's',  's',  None],
         ['r',  's', 'r',  None, 'r',  None, None, 'r',  None],
         [None, 'r', None, None, None, None, 'r',  None, None],
         ['r',  'b', 'r',  None, 'r',  None, None, None, 'r'],
         [None, 'b', None, None, 'b',  None, 'b',  None, 'b']]
    )
    all_grid_objects[:] = construct_all_objects_list(Sand, Rock, Bubble, grid)

    do_whole_grid()
    assert grid == key, f"grid does not match key\ngrid:{grid}\nkey:{key}"
    all_grid_objects.sort(key=lambda object:(object.x, object.y))
    key_all_grid_objects.sort(key=lambda object:(object.x, object.y))
    assert all_grid_objects == key_all_grid_objects


@max_score(5)
@with_import('sand_simulation', 'all_grid_objects')
@with_import('sand_simulation', 'do_whole_grid')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Sand')
@with_import('Grid', 'Grid')
def test_sand_falls_together(Grid, Sand, Rock, Bubble, do_whole_grid, all_grid_objects):
    key = build_grid(Grid, Sand, Rock, Bubble, [[None], ['s'], ['s'], ['s'], ['s']])
    key_all_grid_objects = construct_all_objects_list(Sand, Rock, Bubble, key)

    grid = build_grid(Grid, Sand, Rock, Bubble, [['s'], ['s'], ['s'], ['s'], [None]])
    all_grid_objects[:] = construct_all_objects_list(Sand, Rock, Bubble, grid)

    do_whole_grid()
    assert grid == key, f"grid does not match key\ngrid:{grid}\nkey:{key}"
    all_grid_objects.sort(key=lambda object:(object.x, object.y))
    key_all_grid_objects.sort(key=lambda object:(object.x, object.y))
    assert all_grid_objects == key_all_grid_objects

@max_score(5)
@with_import('sand_simulation', 'all_grid_objects')
@with_import('sand_simulation', 'do_whole_grid')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Sand')
@with_import('Grid', 'Grid')
def test_bubbles_rise_together(Grid, Sand, Rock, Bubble, do_whole_grid, all_grid_objects):
    key = build_grid(Grid, Sand, Rock, Bubble, [['b'], ['b'], ['b'], ['b'], [None]])
    key_all_grid_objects = construct_all_objects_list(Sand, Rock, Bubble, key)

    grid = build_grid(Grid, Sand, Rock, Bubble, [[None], ['b'], ['b'], ['b'], ['b']])
    all_grid_objects[:] = construct_all_objects_list(Sand, Rock, Bubble, grid)

    do_whole_grid()
    assert grid == key, f"grid does not match key\ngrid:{grid}\nkey:{key}"
    all_grid_objects.sort(key=lambda object:(object.x, object.y))
    key_all_grid_objects.sort(key=lambda object:(object.x, object.y))
    assert all_grid_objects == key_all_grid_objects


@max_score(5)
@with_import('sand_simulation', 'all_grid_objects')
@with_import('sand_simulation', 'do_whole_grid')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Sand')
@with_import('Grid', 'Grid')
def test_do_whole_grid_until_sand_settles(Grid, Sand, Rock, Bubble, do_whole_grid, all_grid_objects):
    key_grids = [
        build_grid(
            Grid, Sand, Rock, Bubble,
            [[None, None, None],
             [None, 's', None],
             [None, 's', None],
             [None, 's', None],
             [None, 's', None],
             ['s', 's', None]]
        ),
        build_grid(
            Grid, Sand, Rock, Bubble,
            [[None, None, None],
             [None, None, None],
             [None, 's', None],
             [None, 's', None],
             [None, 's', None],
             ['s', 's', 's']]
        ),
        build_grid(
            Grid, Sand, Rock, Bubble,
            [[None, None, None],
             [None, None, None],
             [None, None, None],
             [None, 's', None],
             ['s', 's', None],
             ['s', 's', 's']]
        ),
        build_grid(
            Grid, Sand, Rock, Bubble,
            [[None, None, None],
             [None, None, None],
             [None, None, None],
             [None, None, None],
             ['s', 's', 's'],
             ['s', 's', 's']]
        ),
        build_grid(
            Grid, Sand, Rock, Bubble,
            [[None, None, None],
             [None, None, None],
             [None, None, None],
             [None, None, None],
             ['s', 's', 's'],
             ['s', 's', 's']]
        )
    ]

    grid = build_grid(
        Grid, Sand, Rock, Bubble,
        [[None, 's', None],
         [None, 's', None],
         [None, 's', None],
         [None, 's', None],
         [None, 's', None],
         [None, 's', None]]
    )
    all_grid_objects[:] = construct_all_objects_list(Sand, Rock, Bubble, grid)

    for key in key_grids:
        key_all_grid_objects = construct_all_objects_list(Sand, Rock, Bubble, key)

        do_whole_grid()
        assert grid == key, f"grid does not match key\ngrid:{grid}\nkey:{key}"
        all_grid_objects.sort(key=lambda object:(object.x, object.y))
        key_all_grid_objects.sort(key=lambda object:(object.x, object.y))
        assert all_grid_objects == key_all_grid_objects


@max_score(5)
@with_import('sand_simulation', 'all_grid_objects')
@with_import('sand_simulation', 'do_whole_grid')
@with_import('Grid_Objects', 'Bubble')
@with_import('Grid_Objects', 'Rock')
@with_import('Grid_Objects', 'Sand')
@with_import('Grid', 'Grid')
def test_do_whole_grid_until_bubbles_settle(Grid, Sand, Rock, Bubble, do_whole_grid, all_grid_objects):
    key_grids = [
        build_grid(
            Grid, Sand, Rock, Bubble,
            [[None, 'b',  'b'],
             [None, 'b',  None],
             [None, 'b',  None],
             [None, 'b',  None],
             [None, 'b',  None],
             [None, None, None]]
        ),
        build_grid(
            Grid, Sand, Rock, Bubble,
            [['b',  'b',  'b'],
             [None, 'b',  None],
             [None, 'b',  None],
             [None, 'b', None],
             [None, None, None],
             [None, None, None]]
        ),
        build_grid(
            Grid, Sand, Rock, Bubble,
            [['b',  'b',  'b'],
             [None, 'b',  'b'],
             [None, 'b',  None],
             [None, None, None],
             [None, None, None],
             [None, None, None]]
        ),
        build_grid(
            Grid, Sand, Rock, Bubble,
            [['b',  'b',  'b'],
             ['b',  'b',  'b'],
             [None, None, None],
             [None, None, None],
             [None, None, None],
             [None, None, None]]
        ),
        build_grid(
            Grid, Sand, Rock, Bubble,
            [['b',  'b',  'b'],
             ['b',  'b',  'b'],
             [None, None, None],
             [None, None, None],
             [None, None, None],
             [None, None, None]]
        )
    ]

    grid = build_grid(
        Grid, Sand, Rock, Bubble,
        [[None, 'b', None],
         [None, 'b', None],
         [None, 'b', None],
         [None, 'b', None],
         [None, 'b', None],
         [None, 'b', None]]
    )
    all_grid_objects[:] = construct_all_objects_list(Sand, Rock, Bubble, grid)

    for key in key_grids:
        key_all_grid_objects = construct_all_objects_list(Sand, Rock, Bubble, key)

        do_whole_grid()
        assert grid == key, f"grid does not match key\ngrid:{grid}\nkey:{key}"
        all_grid_objects.sort(key=lambda object:(object.x, object.y))
        key_all_grid_objects.sort(key=lambda object:(object.x, object.y))
        assert all_grid_objects == key_all_grid_objects
        