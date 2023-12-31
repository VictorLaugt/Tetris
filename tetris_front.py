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


class KeyControlManager:    
    def __init__(self, *, left_right_rotation_callbacks, left_right_shift_callback, down_callback):
        self.down_callback = down_callback
        self.shift_callbacks = left_right_shift_callback
        self.rotation_callbacks = left_right_rotation_callbacks
        self.last_rotation_callback = left_right_rotation_callbacks[0]
        self.rotate_mode = False
    
    
    def _input_methods_fallback(side):
        def input_method(self):
            if self.rotate_mode:
                callback = self.rotation_callbacks[side]
                self.last_rotation_callback = callback
                callback()
            else:
                self.shift_callbacks[side]()
        return input_method
    
    left = _input_methods_fallback(0)
    right = _input_methods_fallback(1)
    
    def down(self):
        if self.rotate_mode:
            self.last_rotation_callback()
        else:        
            self.down_callback()
        
    def enable_rotate_mode(self):
        self.rotate_mode = True
    
    def disable_rotate_mode(self):
        self.rotate_mode = False


class TetrisButtons(tk.Frame):
    def __init__(self, master, font):
        super().__init__(master)
        self.font = font
        
        self.button_shift_left = tk.Button(
            self,
            text='←',
            font=self.font,
            width=10,
            command=self.master.shift_left
        )
        self.button_shift_right = tk.Button(
            self,
            text='→',
            font=self.font,
            width=10,
            command=self.master.shift_right
        )
        self.button_rotate_left = tk.Button(
            self,
            text='↶ (^ ←)',
            font=self.font,
            width=10,
            command=self.master.rotate_left
        )
        self.button_rotate_right = tk.Button(
            self,
            text='↷ (^ →)',
            font=self.font,
            width=10,
            command=self.master.rotate_right
        )
        self.button_down = tk.Button(
            self,
            text='↓',
            font=self.font,
            command=self.master.accelerate
        )

        self.button_rotate_left.grid(row=0, column=0, sticky='nsew')
        self.button_shift_left.grid(row=0, column=1, sticky='nsew')
        self.button_shift_right.grid(row=0, column=2, sticky='nsew')
        self.button_rotate_right.grid(row=0, column=3, sticky='nsew')
        self.button_down.grid(row=1, column=0, columnspan=4, sticky='nsew')


# TODO: implement acceleration of the game speed
class TetrisGui(tk.Tk):
    def __init__(self, back, factor=50, font_size=5, time=500, repeat=-1):
        super().__init__()
        
        self.back = back
        
        self.factor = factor
        self.time = time
        self.repeat = repeat
        
        self.color_grid = tk.Canvas(
            self,
            width=self.back.width * self.factor,
            height=self.back.height * self.factor,
            bg='grey'
        )

        
        self.buttons = TetrisButtons(self, Font(family='Helvetica', size=font_size))
        self.key_controls = KeyControlManager(
            left_right_rotation_callbacks=(self.rotate_left, self.rotate_right),
            left_right_shift_callback=(self.shift_left, self.shift_right),
            down_callback=self.accelerate
        )        
        self.bind('<Left>', lambda _: self.key_controls.left())
        self.bind('<Right>', lambda _: self.key_controls.right())
        self.bind('<Down>', lambda _: self.key_controls.down())
        self.bind('<KeyPress-Control_L>', lambda _: self.key_controls.enable_rotate_mode())
        self.bind('<KeyRelease-Control_L>', lambda _: self.key_controls.disable_rotate_mode())
        
        self.bind_all('<Escape>', lambda _: self.back.reset())
        self.bind_all('<KeyPress-q>', lambda _: self.quit())
                
        self.color_grid.pack(side=tk.TOP)
        self.buttons.pack(side=tk.BOTTOM, expand=True)
        
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
