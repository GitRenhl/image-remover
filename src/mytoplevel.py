import tkinter as tk


class MyTopLevel(tk.Toplevel):
    def __init__(self, master, *a, **kw):
        super().__init__(master, *a, **kw)
        self.master = master

        self.master.wm_attributes("-disabled", True)
        self.transient(self.master)
        self.protocol("WM_DELETE_WINDOW", self._my_destroy)
        self.update()
        self.deiconify()

    def _my_destroy(self):
        self.master.wm_attributes("-disabled", False)
        self.destroy()

    def close(self):
        self._my_destroy()
