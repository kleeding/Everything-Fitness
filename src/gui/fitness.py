from tkinter import Frame
from gui.components.header import Header
from gui.components.navbar import Navbar
from gui.dashboard import Dashboard
from gui.exercise_tracking import ExerciseTracking
from gui.weight_tracking import WeightTracking
from gui.step_tracking import StepTracking
from gui.calorie_tracking import CalorieTracking

class Fitness(Frame):

    scenes = ['dashboard', 'exercise', 'weight', 'steps', 'calories']

    def __init__(self, parent, user):
        super().__init__(parent)
        self.user = user

        # Header Frame
        self.header = Header(self)
        self.header.pack(fill="both")

        # Navbar
        self.navbar = Navbar(self, self.scenes)
        self.navbar.pack(side="left", fill="both")

        # Dashboard Info Widgets - Main Scene/Page
        self.dashboard = Dashboard(self, self.user)

        # Exercise tracking - Page 1
        self.exercise = ExerciseTracking(self, self.user.get_exercise(), self.scenes[1])

        # Weight tracking - Page 2
        self.weight = WeightTracking(self, self.user.get_weight(), self.scenes[2])

        # Step tracking - Page 3
        self.step = StepTracking(self, self.user.get_step(), self.scenes[3])

        # Calorie tracking - Page 4
        self.calorie = CalorieTracking(self, self.user.get_calorie(), self.scenes[4])

        self.current_page_object = ""
        self.change_page(self.scenes[0])

    def change_page(self, scene):
        if scene not in self.scenes:
            return
        if self.current_page_object == "":
            self.load_page(scene)
        elif scene != self.current_page_object.name:
            self.current_page_object.pack_forget()
            self.load_page(scene)

    def load_page(self, scene):
        self.header.update_header(scene)
        if scene == self.scenes[0]:
            self.current_page_object = self.dashboard
            self.current_page_object.refresh_dashboard()
        elif scene == self.scenes[1]:
            self.current_page_object = self.exercise
        elif scene == self.scenes[2]:
            self.current_page_object = self.weight
        elif scene == self.scenes[3]:
            self.current_page_object = self.step
        elif scene == self.scenes[4]:
            self.current_page_object = self.calorie
        self.current_page_object.pack(side="right", fill="both", expand=True)