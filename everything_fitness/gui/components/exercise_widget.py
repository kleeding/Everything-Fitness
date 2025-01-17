from gui.components.dashboard_widget import DashboardWidget

class ExerciseWidget(DashboardWidget):

    labels1 = [["", "Current", "Personal Best"],
               ["-", "-", "-"],
               ["-", "-", "-"],
               ["-", "-", "-"]]

    labels2 = [["Week:", "-"],
               ["Month:", "-"],
               ["Year:", "-"]]

    def __init__(self, parent, exercise_manager):
        super().__init__(parent, exercise_manager)
        self.config(text="EXERCISE")

        self.create_info("Recent Lifts", self.labels1, [2, 1, 1], ['w', '', ''])
        self.create_info("Weight Moved (Kg x Reps)", self.labels2, [1, 1], ['e', ''])
        self.create_info("Time Working Out (Estimated Minutes)", self.labels2, [1, 1], ['e', ''])

        self.set_info_labels(self.data_manager.get_info())
