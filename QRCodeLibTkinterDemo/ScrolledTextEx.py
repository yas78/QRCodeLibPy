from tkinter.scrolledtext import ScrolledText


class ScrolledTextEx(ScrolledText):
    
    def __init__(self, master = None, **kw) -> None:
        super().__init__(master, **kw)
        self.event_add("<<TextChanged>>", "<KeyRelease>")
