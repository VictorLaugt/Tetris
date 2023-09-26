import tkinter as tk

class Foo(tk.Tk):
    def __init__(self):
        super().__init__()


gui = Foo()
gui.mainloop()