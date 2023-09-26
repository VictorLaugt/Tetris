import tkinter as tk

TOUCH = 0
SWIPE_UP = 1
SWIPE_LEFT = 2
SWIPE_RIGHT = 3
SWIPE_DOWN = 4
OTHER = 5


class TouchGestureHandler(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_x = None
        self.start_y = None
        self.commands = [lambda: None] + [lambda _: None] * 5
        self.sensitivity = 50

        self.bind("<ButtonPress-1>", self.on_touch_start)
        self.bind("<ButtonRelease-1>", self.on_touch_end)

    def bind_touch_event(self, touch_event, function):
        self.commands[touch_event] = function
    
    def set_sensitivity(self, new_sensitivity):
        self.sensitivity = new_sensitivity

    def on_touch_start(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_touch_end(self, event):
        dx = event.x - self.start_x
        dy = event.y - self.start_y

        if abs(dx) < 10 and abs(dy) < 10:
            self.commands[TOUCH]()
        elif dy < -self.sensitivity:
            self.commands[SWIPE_UP]((dx, dy))
        elif dy > self.sensitivity:
            self.commands[SWIPE_DOWN]((dx, dy))
        elif dx > self.sensitivity:
            self.commands[SWIPE_RIGHT]((dx, dy))
        elif dx < -self.sensitivity:
            self.commands[SWIPE_LEFT]((dx, dy))
        else:
            self.commands[OTHER]((dx, dy))
        

if __name__ == '__main__': #demo
    class Foo(tk.Tk):
        def __init__(self):
            super().__init__()
            self.text = tk.StringVar(self, '...')
            self.label = tk.Label(textvariable=self.text)
            
            self.swipe_detector = TouchGestureHandler(self)
            self.swipe_detector.bind_touch_event(TOUCH, self.touch)
            self.swipe_detector.bind_touch_event(SWIPE_LEFT, self.left)
            self.swipe_detector.bind_touch_event(SWIPE_RIGHT, self.right)
            self.swipe_detector.bind_touch_event(SWIPE_DOWN, self.down)
            self.swipe_detector.bind_touch_event(SWIPE_UP, self.up)
            self.swipe_detector.bind_touch_event(OTHER, self.other)
            self.swipe_detector.set_sensitivity(100)
            
            self.label.pack()
            self.swipe_detector.pack(fill=tk.BOTH, expand=True)
        
        def touch(self):
            self.text.set('touch')
            self.after(3000, self.reset_text)
        
        def up(self, length):
            self.text.set(f'up {length}')
            self.after(3000, self.reset_text)
        
        def down(self, length):
            self.text.set(f'down {length}')
            self.after(3000, self.reset_text)
        
        def left(self, length):
            self.text.set(f'left {length}')
            self.after(3000, self.reset_text)
        
        def right(self, length):
            self.text.set(f'right {length}')
            self.after(3000, self.reset_text)
        
        def other(self, length):
            self.text.set(f'other {length}')
            self.after(3000, self.reset_text)
        
        def reset_text(self):
            self.text.set('...')

    window = Foo()
    window.mainloop()

