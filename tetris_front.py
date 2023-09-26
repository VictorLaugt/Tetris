import tkinter as tk
from tkinter.font import Font

COLORS = [
    'grey',
    'red',
    'orange',
    'yellow',
    'lawngreen',
    'dodgerblue',
    'blue'
]


# TODO: implement acceleration of the game speed
class TetrisGui(tk.Tk):
    def __init__(self, back, factor=50, font_size=5, time=500, repeat=-1):
        super().__init__()
        
        self.back = back
        
        self.factor = factor
        self.font = Font(family='Helvetica', size=font_size)
        self.time = time
        self.repeat = repeat
        
        self.color_grid = tk.Canvas(
            self,
            width=self.back.width * self.factor,
            height=self.back.height * self.factor,
            bg='grey'
        )
        self.button_shift_left = tk.Button(
            self,
            text='←',
            font=self.font,
            command=self.shift_left
        )
        self.button_shift_right = tk.Button(
            self,
            text='→',
            font=self.font,
            command=self.shift_right
        )
        self.button_rotate_left = tk.Button(
            self,
            text='↶',
            font=self.font,
            command=self.rotate_left
        )
        self.button_rotate_right = tk.Button(
            self,
            text='↷',
            font=self.font,
            command=self.rotate_right
        )
        self.button_down = tk.Button(
            self,
            text='↓',
            font=self.font,
            command=self.accelerate
        )
        
        self.color_grid.grid(row=0, column=0, columnspan=5)
        self.button_rotate_left.grid(row=1, column=0, sticky='nsew')
        self.button_shift_left.grid(row=1, column=1, sticky='nsew')
        self.button_shift_right.grid(row=1, column=2, sticky='nsew')
        self.button_rotate_right.grid(row=1, column=3, sticky='nsew')
        self.button_down.grid(row=1, column=4, sticky='nsew')
        
        self.step()
    
    def reset(self):
        self.repeat -= 1
        if self.repeat != 0:
            self.back.reset()
        else:
            self.quit()
    
    def step(self):
        if self.back.game_step():
            self.reset()
        self.refresh()
        self.after(self.time, self.step)
    
    def refresh(self):
        self.color_grid.delete(tk.ALL)
        y_limit = self.back.starting_row * self.factor
        self.color_grid.create_line(0, y_limit, self.back.width * self.factor, y_limit)
        for u, v, color_id in self.back.colored_squares():
            x, y = u*self.factor, v*self.factor
            self.color_grid.create_rectangle(
                x, y, x+self.factor, y+self.factor,
                fill=COLORS[color_id]
            )

    def shift_left(self):
        self.back.shift_left()
        self.refresh()
    
    def shift_right(self):
        self.back.shift_right()
        self.refresh()
    
    def rotate_left(self):
        self.back.rotate_left()
        self.refresh()
    
    def rotate_right(self):
        self.back.rotate_right()
        self.refresh()
    
    def accelerate(self):
        if self.back.accelerate():
            self.reset()
        self.refresh()
