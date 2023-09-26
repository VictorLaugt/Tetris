import numpy as np
import random

from typing import TypeVar, Tuple

Grid = TypeVar('2DArray')
VectorArray = TypeVar('1DArray[2-Vector]')
Vector = TypeVar('2-Vector')


def rotate_direct(vector):
    """Rotates in place `vector` from pi/2"""
    vector[0], vector[1] = vector[1], -vector[0]

def rotate_indirect(vector):
    """Rotates in place `vector` from -pi/2"""
    vector[0], vector[1] = -vector[1], vector[0]


class Direction:
    left =  np.array([-1, 0])
    right = np.array([1, 0])
    up =    np.array([0, -1])
    down =  np.array([0, 1])
    
    
def random_color():
    return random.randrange(1, 7)


class Block:
    model: VectorArray
    center: Vector
    radius: int
    
    def __init__(self, x, y, color):
        self.position = np.zeros((2,), dtype=np.int64)
        self.position[0] = x
        self.position[1] = y
        
        self.squares = self.model.copy()
        self.squares += self.position
        
        self.color = color
    
    def grid_repr(self, grid):
        result = []
        for y in range(grid.shape[1]):
            row = [f'{y:2}']
            for x in range(grid.shape[0]):
                if (grid[x, y] or
                        any((x,y) == (u,v) for u,v in self.squares)):
                    row.append('*')
                else:
                    row.append('.')
            result.append(''.join(row))
        return '\n'.join(result)
    
    def inside_limits(self, width, height):
        return (np.all((0,0) <= self.squares) and
            np.all(self.squares < (width, height)))
    
    def colides(self, grid):
        return any(grid[x, y] for x, y in self.squares)
    
    def shift(self, vector):
        self.squares += vector
        self.position += vector
    
    def rotate(self, rotate_func):
        position = self.position
        for sqr in self.squares:
            sqr -= position
            rotate_func(sqr)
            sqr += position
    
    def lock(self, grid):
        for x, y in self.squares:
            grid[x, y] = self.color


class BlockO(Block):
    model = np.array([[0,0], [1,0], [0,1], [1,1]], dtype=np.int64)
    center = np.array([0,0], dtype=np.int64)
    radius = 2

class BlockI(Block):
    model = np.array([[0,-1], [0,0], [0,1], [0,2]], dtype=np.int64)
    center = np.array([0,1], dtype=np.int64)
    radius = 3

class BlockS(Block):
    model = np.array([[-1,0], [0,0], [0,-1], [1,-1]], dtype=np.int64)
    center = np.array([1,0], dtype=np.int64)
    radius = 2

class BlockZ(Block):
    model = np.array([[-1,-1], [0,-1], [0,0], [1,0]], dtype=np.int64)
    center = np.array([1,0], dtype=np.int64)
    radius = 2

class BlockL(Block):
    model = np.array([[-1,-1], [-1,0], [-1,1], [0,1]], dtype=np.int64)
    center = np.array([0,1], dtype=np.int64)
    radius = 2

class BlockJ(Block):
    model = np.array([[0,-1], [0,0], [0,1], [-1,1]], dtype=np.int64)
    center = np.array([1,1], dtype=np.int64)
    radius = 2

class BlockT(Block):
    model = np.array([[-1,0], [0,0], [1,0], [0,1]], dtype=np.int64)
    center = np.array([1,0], dtype=np.int64)
    radius = 2

SHAPES = (BlockO, BlockI, BlockS, BlockZ, BlockL ,BlockJ, BlockT)


class Tetris:
    """Implements a tetris game backend.
    
    Interface
    -------------------------------
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
        for x, y in self.current_block.squares:
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
                block_type.radius-1,
                self.width-block_type.radius+1
            ),
            self.starting_row,
            random_color()
        )
        print(f'created {type(block).__name__}')
        print(f'{block.position=}')
        print(f'{block.squares=}')
        print(f'{block.color=}\n')
        for _ in range(random.randrange(0, 4)):
            block.rotate(rotate_direct)
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
        lambda block: block.rotate(rotate_direct),
        lambda block: block.rotate(rotate_indirect)
    )
    
    rotate_right = _move_methods_fallback(
        lambda block: block.rotate(rotate_indirect),
        lambda block: block.rotate(rotate_direct)
    )
