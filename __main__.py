#PyDroid must import tkinter
import tetris_front
import tetris_back

game = tetris_back.Tetris(
    width=10,
    height=20, 
    starting_row=3
)
gui = tetris_front.TetrisGui(
    game,
    # factor=60,
    factor=47,
    font_size=16,
    time=500,
    repeat=1
)
gui.mainloop()

