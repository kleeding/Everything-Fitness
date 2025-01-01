from tkinter import Frame, Label
from datetime import datetime

class Header(Frame):

    header_colour = "#A10A10A10"

    def __init__(self, parent):
        super().__init__(parent, bg=self.header_colour)

        self.grid_columnconfigure((0,1), uniform=True, weight=1)

        self.date = datetime.today().strftime('%d-%m-%Y')
        self.date_label = Label(self, text=self.date, font=('Segoe UI', 12), bg=self.header_colour)
        self.header_title = Label(self, text="DASHBOARD", font=('Segoe UI', 25), bg=self.header_colour)
        self.date_label.grid(padx=15, pady=(10,0), row=0, column=0, sticky="sw")
        self.header_title.grid(padx=15, pady=(0,10), row=1, column=0, sticky="nw")

        # # Potentially add some customisation like an avatar, light/dark mode, other?
        # self.avatar_label = Label(self, text="AVATAR_IMG", bg=self.header_colour)
        # self.avatar_label.grid(padx=30, row=0, column=1, rowspan=2, sticky="e")

    def update_header(self, string):
        self.header_title.config(text=string.upper())
