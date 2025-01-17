from tkinter import Frame
from gui.components.exercise_widget import ExerciseWidget
from gui.components.weight_widget import WeightWidget
from gui.components.step_widget import StepWidget
from gui.components.calorie_widget import CalorieWidget

class Dashboard(Frame):

    def __init__(self, parent, user):
        super().__init__(parent)
        self.name="dashboard"

        self.grid_columnconfigure((0,1), uniform=True, weight=1)
        self.grid_rowconfigure((0,1), weight=1)

        self.exercise_widget = ExerciseWidget(self, user.get_exercise())
        self.exercise_widget.grid(row=0, column=0, sticky="news", padx=(10,5), pady=(10,5))

        self.weight_widget = WeightWidget(self, user.get_weight())
        self.weight_widget.grid(row=0, column=1, sticky="news", padx=(5,10), pady=(10,5))

        self.step_widget = StepWidget(self, user.get_step())
        self.step_widget.grid(row=1, column=0, sticky="news", padx=(10,5), pady=(5,10))

        self.calorie_widget = CalorieWidget(self, user.get_calorie())
        self.calorie_widget.grid(row=1, column=1, sticky="news", padx=(5,10), pady=(5,10))

    def refresh_dashboard(self):
        self.exercise_widget.refresh()
        self.weight_widget.refresh()
        self.step_widget.refresh()
        self.calorie_widget.refresh()
