from tkinter import Menu as tkMenu
from tkinter import messagebox


class TopMenu:
    _about = {
        'version': '0.1',
        'date': '2020.01.15',
        'author': 'Marcin Ożóg',
    }

    def __init__(self, master, close_func):
        self._master = master
        self._menu = tkMenu(self._master)
        self.__init(close_func)

    def __init(self, close_func):
        file_c = tkMenu(self._menu, tearoff=0)
        file_c.add_cascade(label="Exit", command=close_func)

        help_c = tkMenu(self._menu, tearoff=0)
        help_c.add_cascade(label="About", command=self._show_menu)

        self._menu.add_cascade(label="File", menu=file_c)
        self._menu.add_cascade(label="Help", menu=help_c)
        self._master.config(menu=self._menu)

    def _show_menu(self):
        msg = ''
        for k, v in self._about.items():
            msg += f"{k.capitalize()}: {v}\n"

        messagebox.showinfo("About", msg)
