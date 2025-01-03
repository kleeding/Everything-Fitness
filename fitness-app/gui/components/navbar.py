from tkinter import Frame, Button, PhotoImage
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Navbar(Frame):

    navbar_colour = "#D1D1D1"
    relative_path = 'fitness-app\\assets\\icons\\'

    def __init__(self, parent, scenes):
        super().__init__(parent)
        self.parent = parent
        self.scenes = scenes

        self.config(bg=self.navbar_colour)

        self.home_image = PhotoImage(file=resource_path(self.relative_path+'home_icon.png'))
        self.exercise_image = PhotoImage(file=resource_path(self.relative_path+'exercise_icon.png'))
        self.weight_image = PhotoImage(file=resource_path(self.relative_path+'weight_icon.png'))
        self.step_image = PhotoImage(file=resource_path(self.relative_path+'step_icon.png'))
        self.calorie_image = PhotoImage(file=resource_path(self.relative_path+'calorie_icon.png'))

        self.home_button = Button(self, image=self.home_image, command=lambda: self.parent.change_page(self.scenes[0]))
        self.home_button.grid(padx=5, pady=5, row=0, column=0)

        self.exercise_button = Button(self, image=self.exercise_image, command=lambda: self.parent.change_page(self.scenes[1]))
        self.exercise_button.grid(padx=5, pady=5, row=1, column=0)

        self.weight_button = Button(self, image=self.weight_image, command=lambda: self.parent.change_page(self.scenes[2]))
        self.weight_button.grid(padx=5, pady=5, row=2, column=0)

        self.step_button = Button(self, image=self.step_image, command=lambda: self.parent.change_page(self.scenes[3]))
        self.step_button.grid(padx=5, pady=5, row=3, column=0)

        self.calorie_button = Button(self, image=self.calorie_image, command=lambda: self.parent.change_page(self.scenes[4]))
        self.calorie_button.grid(padx=5, pady=5, row=4, column=0)