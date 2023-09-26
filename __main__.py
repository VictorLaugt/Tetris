#PyDroid must import tkinter
import tetris_front
import tetris_back

game = tetris_back.Tetris(
    width=12,
    height=20, 
    starting_row=3
)
gui = tetris_front.TetrisGui(
    game,
    factor=60,
    font_size=6,
    time=500,
    repeat=1
)
gui.mainloop()

