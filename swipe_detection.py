from __future__ import annotations

import abc
import tkinter as tk


class AbstractSingleTouchHandler(tk.Frame, abc.ABC):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.start_x = None
        self.start_y = None
        self.touch_max_length = 10
        self.swipe_min_length = 50
        self.bind('<ButtonPress-1>', self.on_touch_start)
        self.bind('<ButtonRelease-1>', self.on_touch_end)

    def set_touch_max_length(self, touch_max_length: float) -> None:
        self.touch_max_length = touch_max_length

    def get_touch_max_length(self):
        return self.touch_max_length

    def set_swipe_min_length(self, swipe_min_length: float) -> None:
        self.swipe_min_length = swipe_min_length

    def get_swipe_min_length(self):
        return self.swipe_min_length

    def on_touch_start(self, event: tk.Event) -> None:
        self.start_x = event.x
        self.start_y = event.y

    def on_touch_end(self, event: tk.Event) -> None:
        dx = event.x - self.start_x
        dy = event.y - self.start_y

        if abs(dx) < self.touch_max_length and abs(dy) < self.touch_max_length:
            self.on_touch(self.start_x, self.start_y, event.x, event.y, dx, dy)
        elif dy < -self.swipe_min_length:
            self.on_swipe_up(self.start_x, self.start_y, event.x, event.y, dx, dy)
        elif dy > self.swipe_min_length:
            self.on_swipe_down(self.start_x, self.start_y, event.x, event.y, dx, dy)
        elif dx > self.swipe_min_length:
            self.on_swipe_right(self.start_x, self.start_y, event.x, event.y, dx, dy)
        elif dx < -self.swipe_min_length:
            self.on_swipe_left(self.start_x, self.start_y, event.x, event.y, dx, dy)
        else:
            self.on_other(self.start_x, self.start_y, event.x, event.y, dx, dy)

    @abc.abstractmethod
    def on_touch(self, x0: float, y0: float, x1: float, y1: float, dx: float, dy: float) -> None:
        pass

    @abc.abstractmethod
    def on_swipe_up(self, x0: float, y0: float, x1: float, y1: float, dx: float, dy: float) -> None:
        pass

    @abc.abstractmethod
    def on_swipe_down(self, x0: float, y0: float, x1: float, y1: float, dx: float, dy: float) -> None:
        pass

    @abc.abstractmethod
    def on_swipe_left(self, x0: float, y0: float, x1: float, y1: float, dx: float, dy: float) -> None:
        pass

    @abc.abstractmethod
    def on_swipe_right(self, x0: float, y0: float, x1: float, y1: float, dx: float, dy: float) -> None:
        pass

    @abc.abstractmethod
    def on_other(self, x0: float, y0: float, x1: float, y1: float, dx: float, dy: float) -> None:
        pass


class DemoTouchGestureHandler(AbstractSingleTouchHandler):
    def __init__(self, string_var: tk.StringVar) -> None:
        super().__init__()
        self.scheduling = None
        self.string_var = string_var

    def reset_text(self):
        self.string_var.set('...')

    def display_direction_name(self, direction_name: str, dx: float, dy: float) -> None:
        length = (dx*dx + dy*dy) ** .5
        self.string_var.set(f'{direction_name} (length = {length:.3f})')

        if self.scheduling is not None:
            self.after_cancel(self.scheduling)
        self.scheduling = self.after(1500, self.reset_text)

    def on_touch(self, x0: float, y0: float, x1: float, y1: float, dx: float, dy: float) -> None:
        self.display_direction_name('touch', dx, dy)

    def on_swipe_up(self, x0: float, y0: float, x1: float, y1: float, dx: float, dy: float) -> None:
        self.display_direction_name('up', dx, dy)

    def on_swipe_down(self, x0: float, y0: float, x1: float, y1: float, dx: float, dy: float) -> None:
        self.display_direction_name('down', dx, dy)

    def on_swipe_left(self, x0: float, y0: float, x1: float, y1: float, dx: float, dy: float) -> None:
        self.display_direction_name('left', dx, dy)

    def on_swipe_right(self, x0: float, y0: float, x1: float, y1: float, dx: float, dy: float) -> None:
        self.display_direction_name('right', dx, dy)

    def on_other(self, x0: float, y0: float, x1: float, y1: float, dx: float, dy: float) -> None:
        self.display_direction_name('other', dx, dy)


class DemoApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        string_var = tk.StringVar(self, '...')
        self.label = tk.Label(textvariable=string_var)
        self.swipe_detector = DemoTouchGestureHandler(string_var)

        self.label.pack()
        self.swipe_detector.pack(fill=tk.BOTH, expand=True)


if __name__ == '__main__':
    window = DemoApp()
    window.mainloop()

