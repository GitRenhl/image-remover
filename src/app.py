import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
import tkinter.messagebox
import os
import re
import logging
from src.mytoplevel import MyTopLevel
from src.menu import TopMenu

LOG = logging.getLogger('guiapp')


class App:
    img_types = {
        0: "jpg",
        1: "jpeg",
        2: "JPG",
        3: "JPEG",
        4: "png",
        5: "PNG",
    }

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('410x575')
        self.root.resizable(False, True)
        self.root.protocol("WM_DELETE_WINDOW", self.close_app)
        self.root.title("Usuwanie plików")
        TopMenu(self.root, self.close_app)

        self.path_string = tk.StringVar()
        # self.path_string.set("G:/Python2019/files_remover/zdj")
        self.radio_btn_var = tk.IntVar()

        path_frame = tk.LabelFrame(self.root,
                                   text="Ścieżka do plików:")
        self.input_path = ttk.Entry(path_frame,
                                    textvariable=self.path_string,
                                    width=50)
        self.input_path.pack(side=tk.LEFT)

        ttk.Button(path_frame,
                   text='Pokaż pliki..',
                   command=self._show_files).pack(side=tk.RIGHT)
        ttk.Button(path_frame,
                   text='...',
                   command=self._get_dir).pack(side=tk.RIGHT)
        path_frame.pack(expand=True, fill=tk.X)

        ################################################

        radio_frame = tk.Frame(self.root)

        radio_label_frame = tk.LabelFrame(radio_frame,
                                          text='Typ plików:')
        self.radio_btn_var.set(0)
        for mode, name in self.img_types.items():
            r = ttk.Radiobutton(radio_label_frame,
                                text=name,
                                variable=self.radio_btn_var,
                                value=mode)
            r.pack(anchor=tk.W, fill=tk.X)
        radio_label_frame.pack()
        radio_frame.pack(expand=True, fill=tk.BOTH)

        ################################################

        nums_frame = tk.LabelFrame(self.root,
                                   text='Numery plików:')
        self.files_num = tk.Text(nums_frame, width=40, height=20)
        self.files_num.pack()
        nums_frame.pack(expand=True, fill=tk.X)

        ################################################

        btn_frame = tk.Frame(self.root)
        ttk.Button(btn_frame,
                   text="Usuń",
                   command=self._delete_files).place(relx=0.5,
                                                     rely=0.5,
                                                     anchor=tk.CENTER)
        btn_frame.pack(expand=True, fill=tk.BOTH)

    def run(self):
        self.root.mainloop()

    def close_app(self):
        self.root.bell()
        value = tk.messagebox.askyesno("Exit",
                                       "Czy na pewno chcesz zamknąć program?")
        if value:
            self.root.destroy()

    def _get_dir(self, event=None):
        dir_path = tk.filedialog.askdirectory()
        if dir_path:
            self.path_string.set(dir_path)

    def _get_text_to_list(self):
        text = self.files_num.get(0.0, tk.END).strip()
        if not text:
            return False

        splited = ''.join(text.split()).split(',')
        return tuple(splited)

    def is_path_correct(self, path=None):
        valid = True
        if path is None:
            path = self.path_string.get()

        if not os.path.exists(path):
            valid = False
        return valid

    def assert_path(self):
        if not self.is_path_correct():
            tk.messagebox.showwarning(
                'Ścieżka nie została znaleziona',
                f'Podana ścieżka nie istnieje lub jest nieprawidłowa:\n"{self.path_string.get()}"')
            return True
        else:
            return False

    def _get_all_ext_del_file_names(self):
        ext_items = []
        del_items = []
        not_file = []
        to_remove = self._get_text_to_list()
        if not to_remove:
            to_remove = ()

        path = self.path_string.get()
        all_items = os.listdir(path)
        extension = '.' + self.img_types.get(self.radio_btn_var.get())

        for name in all_items:
            if not os.path.isfile(path + '/' + name):
                not_file.append(name)

            elif extension in name:
                ext_items.append(name)
                num = re.findall(r'\d+', name)
                if len(num) == 0:
                    continue
                num = num[-1]
                if num in to_remove:
                    del_items.append(name)

        for name in not_file:
            all_items.remove(name)

        return all_items, ext_items, del_items

    def _move_files_to_folder(self, path, files):
        LOG.debug(f'Begin moving files {files}')
        if self.assert_path():
            return
        else:
            if path[-1] not in r"\/":
                path += '/'
            del_path = f'{path}usuniete/'

        if not os.path.exists(del_path):
            try:
                os.makedirs(del_path)
            except PermissionError as e:
                LOG.warning(f"Os makedir: {e}")
                return

        for f in files:
            LOG.debug(f"MOVE '{f}' from {path} to {del_path}")
            try:
                os.rename(path + f, del_path + f)
            except Exception as e:
                LOG.warning(
                    f"Cannot move '{f}' from {path} to {del_path}: {e}")
        LOG.debug(f"DONE!")

    def _delete_files(self):
        if self.assert_path():
            return

        _, _, del_files = self._get_all_ext_del_file_names()
        path = self.path_string.get()

        if len(del_files) == 0:
            tk.messagebox.showinfo('Brak plików',
                                   'Brak plików do usunięcia.')
            return

        top = MyTopLevel(self.root)
        top.geometry('260x350')

        tk.Label(top, text="Czy chcesz usunąć poniższe pliki?").pack()

        box = tk.Frame(top)
        lbox = tk.Listbox(box)
        scrollbarY = tk.Scrollbar(box,
                                  orient=tk.VERTICAL,
                                  command=lbox.yview)
        scrollbarX = tk.Scrollbar(box,
                                  orient=tk.HORIZONTAL,
                                  command=lbox.xview)
        lbox.config(yscrollcommand=scrollbarY.set)
        lbox.config(xscrollcommand=scrollbarX.set)
        scrollbarY.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbarX.pack(side=tk.BOTTOM, fill=tk.X)
        lbox.pack(side=tk.LEFT, expand=True, fill=tk.X)
        lbox.insert(tk.END, *del_files)
        box.pack(expand=True, fill=tk.X)

        def close():
            self._move_files_to_folder(path, del_files)
            top.close()

        ttk.Button(top,
                   text='Usuń',
                   command=close).pack()

    def _show_files(self):
        if self.assert_path():
            return

        top = MyTopLevel(self.root)
        top.minsize(425, 100)

        all_items, ext_items, del_items = self._get_all_ext_del_file_names()
        extension = '.' + self.img_types.get(self.radio_btn_var.get())

        frame_all = tk.Frame(top)
        frame_ext = tk.Frame(top)
        frame_del = tk.Frame(top)
        tk.Label(frame_all, text='Wszystkie').pack()
        tk.Label(frame_ext, text=f'Pliki {extension}').pack()
        tk.Label(frame_del, text='Do usunięcia').pack()
        box_all = tk.Listbox(frame_all)
        box_ext = tk.Listbox(frame_ext)
        box_del = tk.Listbox(frame_del)
        scrollbar0y = tk.Scrollbar(frame_all, orient=tk.VERTICAL,
                                   command=box_all.yview)
        scrollbar0x = tk.Scrollbar(frame_all, orient=tk.HORIZONTAL,
                                   command=box_all.xview)
        scrollbar1y = tk.Scrollbar(frame_ext, orient=tk.VERTICAL,
                                   command=box_ext.yview)
        scrollbar1x = tk.Scrollbar(frame_ext, orient=tk.HORIZONTAL,
                                   command=box_ext.xview)
        scrollbar2y = tk.Scrollbar(frame_del, orient=tk.VERTICAL,
                                   command=box_del.yview)
        scrollbar2x = tk.Scrollbar(frame_del, orient=tk.HORIZONTAL,
                                   command=box_del.xview)

        box_all.config(yscrollcommand=scrollbar0y.set)
        box_all.config(xscrollcommand=scrollbar0x.set)
        box_ext.config(yscrollcommand=scrollbar1y.set)
        box_ext.config(xscrollcommand=scrollbar1x.set)
        box_del.config(yscrollcommand=scrollbar2y.set)
        box_del.config(xscrollcommand=scrollbar2x.set)

        scrollbar0y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar0x.pack(side=tk.BOTTOM, fill=tk.X)
        scrollbar1y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar1x.pack(side=tk.BOTTOM, fill=tk.X)
        scrollbar2y.pack(side=tk.RIGHT, fill=tk.Y)
        scrollbar2x.pack(side=tk.BOTTOM, fill=tk.X)
        box_all.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        box_ext.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        box_del.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        frame_all.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        frame_del.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        frame_ext.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        box_all.insert(tk.END, *all_items)
        box_ext.insert(tk.END, *ext_items)
        box_del.insert(tk.END, *del_items)
