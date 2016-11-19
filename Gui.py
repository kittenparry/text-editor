import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from strings import *

class Gui(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.top = tk.Frame(master, relief='raised')
        self.toolbar = tk.Frame(master)
        self.table = tk.Frame(master)

        self.top.pack(side='top', fill='x')
        self.toolbar.pack(side='top', fill='x')
        self.table.pack(side='top')

        self.menu = tk.Menubutton(self.top, text=txt_file, underline=0)
        self.menu.grid(row=0, column=0)
        self.menu_sub = tk.Menu(self.menu, tearoff=0)
        self.menu['menu'] = self.menu_sub
        self.menu_sub.add_command(label=txt_new, underline=0, command=self.new_func)
        self.menu_sub.add_command(label=txt_open, underline=0, command=self.open_func)
        self.menu_sub.add_command(label=txt_save, underline=0, command=self.save_func)
        self.menu_sub.add_separator()
        self.menu_sub.add_command(label=txt_exit, command=self.exit_func)

        self.label_toolbar = tk.Label(self.toolbar, text=txt_tools)
        self.label_toolbar.grid(row=0, column=1)
        #toolbar stuff

        self.area = tk.Text(self.table, width=50, height=25, wrap='none')
        self.area.grid(row=0, column=0)

        self.scrollx = tk.Scrollbar(self.table, orient='horizontal', command=self.area.xview)
        self.scrollx.grid(row=1, column=0, sticky='we')
        self.scrolly = tk.Scrollbar(self.table, orient='vertical', command=self.area.yview)
        self.scrolly.grid(row=0, column=1, sticky='ns')
        self.area.configure(xscrollcommand=self.scrollx.set, yscrollcommand=self.scrolly.set)

        self.types = [(txt_text_files, '*.txt')]

    def save_func(self):
        f = fd.asksaveasfile(title=txt_save_file_title, mode='w', defaultextension='.txt', filetypes=self.types)
        if f is None:
            return #TODO: abort the upcoming sections
        text = str(self.area.get('1.0', 'end'))
        f.write(text)
        f.close()

    def open_func(self):
        path = fd.askopenfilename(title=txt_open_file_title, filetypes=self.types)
        print('selected path: %s' % path)
        self.change_det(txt_open_conf_title, txt_open_conf_msg)
        self.open_file(path)

    def open_file(self, path):
        try:
            f = open(path, 'r')
            self.area.delete('1.0', 'end')
            self.area.insert('1.0', f.read())
            self.area.edit_modified(False)
            f.close()
        except IOError:
            print('error')

    def exit_func(self):
        self.change_det(txt_exit_conf_title, txt_exit_conf_msg)
        self.quit()

    def change_det(self, title, msg):
        if self.area.get('1.0 + 1 c', 'end'):
            if self.area.edit_modified():
                if not mb.askyesno(title, msg):
                    self.save_func()

    def new_func(self):
        self.change_det(txt_open_conf_title, txt_open_conf_msg)
        self.area.delete('1.0', 'end')


if __name__ == '__main__':
    root = tk.Tk()
    root.title(txt_title)
    root.geometry('500x500')
    app = Gui(master=root)
    app.mainloop()
