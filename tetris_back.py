import numpy as np
import random

from typing import TypeVar, Tuple

Grid = TypeVar('2DArray')
VectorGrid = TypeVar('2DArray[2-Vector]')
Vector = TypeVar('2-Vector')


class Direction:
    left =  np.array([-1, 0])
    right = np.array([1, 0])
    up =    np.array([0, -1])
    down =  np.array([0, 1])

class Rotation:
    direct = 1
    indirect = -1


def random_color():
    return random.randrange(1, 7)


class Block:
    """Implements Tetris blocks

    Interface
    ----------------------------------------------------------------------------
    attributes:
        color: int

    methods:
        get_squares
        inside_limits
        colides
        shift
        rotate
        lock
    """
    models: VectorGrid
    radius: int

    def __init__(self, x, y, color):
        self.shapes = self.models.copy()
        self.shapes[:, :, 0] += x
        self.shapes[:, :, 1] += y

        self.orientation = 0
        self.color = color

    def get_squares(self):
        return self.shapes[self.orientation]

    def grid_repr(self, grid):
        result = []
        for y in range(grid.shape[1]):
            row = [f'{y:2}']
            for x in range(grid.shape[0]):
                if (grid[x, y] or
                        any((x,y) == (u,v) for u,v in self.get_squares())):
                    row.append('*')
                else:
                    row.append('.')
            result.append(''.join(row))
        return '\n'.join(result)

    def inside_limits(self, width, height):
        sqrs = self.get_squares()
        return np.all((0, 0) <= sqrs) and np.all(sqrs < (width, height))

    def colides(self, grid):
        return any(grid[x, y] for x, y in self.get_squares())

    def shift(self, vector):
        self.shapes += vector

    def rotate(self, rotation):
        self.orientation = (self.orientation + rotation) % len(self.models)

    def lock(self, grid):
        for x, y in self.get_squares():
            grid[x, y] = self.color


class BlockO(Block):
    models = np.array(( ((0,0), (1,0), (0,1), (1,1)), ), dtype=np.int64)
    y_start = -2
    x_min = 0
    x_max = -1

class BlockI(Block):
    models = np.array((
        ((0,-1), (0,0), (0,1), (0,2)),
        ((-1,1), (0,1), (1,1), (2,1)),
        ((1,-1), (1,0), (1,1), (1,2)),
        ((-1,0), (0,0), (1,0), (2,0)),
        ), dtype=np.int64)
    y_start = -2
    x_min = 1
    x_max = -2

class BlockS(Block):
    models = np.array((
        ((-1,0), (0,0), (0,-1), (1,-1)),
        ((-1,-1), (-1,0), (0,0), (0,1)),
        ((-1,1), (0,1), (0,0), (1,0)),
        ((0,-1), (0,0), (1,0), (1,1)),
        ), dtype=np.int64)
    y_start = -2
    x_min = 1
    x_max = -1

class BlockZ(Block):
    models = np.array((
        ((0,-1), (0,0), (-1,0), (-1,1)),
        ((1,1), (0,1), (0,0), (-1,0)),
        ((1,-1), (1,0), (0,0), (0,1)),
        ((1,0), (0,0), (0,-1), (-1,-1)),
        ), dtype=np.int64)
    y_start = -2
    x_min = 1
    x_max = -1

class BlockJ(Block):
    models = np.array((
        ((0,1), (0,0), (0,-1), (-1,1)),
        ((-1,0), (0,0), (1,0), (1,1)),
        ((0,1), (0,0), (0,-1), (1,-1)),
        ((-1,0), (0,0), (1,0), (-1,-1)),
        ), dtype=np.int64)
    y_start = -2
    x_min = 1
    x_max = -1

class BlockL(Block):
    models = np.array((
        ((0,1), (0,0), (0,-1), (-1,-1)),
        ((-1,0), (0,0), (1,0), (-1,1)),
        ((0,1), (0,0), (0,-1), (1,1)),
        ((-1,0), (0,0), (1,0), (1,-1)),
        ), dtype=np.int64)
    y_start = -2
    x_min = 1
    x_max = -1

class BlockT(Block):
    models = np.array((
        ((0,1), (0,0), (0,-1), (1,0)),
        ((-1,0), (0,0), (1,0), (0,-1)),
        ((0,1), (0,0), (0,-1), (-1,0)),
        ((-1,0), (0,0), (1,0), (0,1)),
        ), dtype=np.int64)
    y_start = -2
    x_min = 1
    x_max = -1

SHAPES = (BlockO, BlockI, BlockS, BlockZ, BlockL ,BlockJ, BlockT)


class Tetris:
    """Implements a tetris game backend.

    Interface
    ----------------------------------------------------------------------------
    attributes:
        width: int
        height: int
        starting_row: int
        current_block: Block
        next_block: Block

    methods:
        colored_squares
        game_step
        shift_left
        shift_right
        rotate_left
        rotate_right
    """
    def __init__(self, width, height, starting_row):
        assert height > 5 and width > 5
        self.grid = np.ones((width, height+1), dtype=np.int32)

        # interface
        self.width = width
        self.height = height
        self.starting_row = starting_row
        self.current_block = None
        self.next_block = None

        self.reset()

    def colored_squares(self):
        # locked blocks
        for x in range(self.width):
            for y in range(self.height):
                color = self.grid[x, y]
                if color:
                    yield x, y, color

        # moving block
        color = self.current_block.color
        for x, y in self.current_block.get_squares():
            yield x, y, color

    def reset(self):
        self.grid[:, :-1] = 0
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()

    def __repr__(self):
        return self.current_block.grid_repr(self.grid)

    def get_random_block(self):
        block_type = random.choice(SHAPES)
        block = block_type(
            random.randrange(
                block_type.x_min,
                self.width + block_type.x_max
            ),
            self.starting_row + block_type.y_start,
            random_color()
        )
        print(f'created {type(block).__name__}')
        print(f'{block.get_squares()=}')
        print(f'{block.color=}\n')
        for _ in range(random.randrange(0, 4)):
            block.rotate(Rotation.direct)
        return block


    def erase_row(self, y):
        self.grid[:, y] = 0

    def fall(self, y):
        for y2 in range(y, 0, -1):
            self.grid[:, y2] = self.grid[:, y2-1]

    def lock_current_block(self):
        self.current_block.lock(self.grid)
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        for y in range(self.height):
            if np.all(self.grid[:, y]):
                self.erase_row(y)
                self.fall(y)

    def is_over(self):
        return np.any(self.grid[:, :self.starting_row])

    def game_step(self):
        self.current_block.shift(Direction.down)
        if self.current_block.colides(self.grid):
            self.current_block.shift(Direction.up)
            self.lock_current_block()
        return self.is_over()

    def accelerate(self):
        while not self.current_block.colides(self.grid):
            self.current_block.shift(Direction.down)
        self.current_block.shift(Direction.up)
        self.lock_current_block()
        return self.is_over()

    def _move_methods_fallback(do, undo):
        def move_current_block(self):
            do(self.current_block)
            if (not self.current_block.inside_limits(self.width, self.height)
                    or self.current_block.colides(self.grid)):
                undo(self.current_block)
        return move_current_block

    shift_left = _move_methods_fallback(
        lambda block: block.shift(Direction.left),
        lambda block: block.shift(Direction.right)
    )

    shift_right = _move_methods_fallback(
        lambda block: block.shift(Direction.right),
        lambda block: block.shift(Direction.left)
    )

    rotate_left = _move_methods_fallback(
        lambda block: block.rotate(Rotation.direct),
        lambda block: block.rotate(Rotation.indirect)
    )

    rotate_right = _move_methods_fallback(
        lambda block: block.rotate(Rotation.indirect),
        lambda block: block.rotate(Rotation.direct)
    )
