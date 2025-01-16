from gui.components.tracking_page import TrackingPage
from gui.components.basic_form import BasicForm

class ExerciseTracking(TrackingPage):

    info = "On this page you can add and remove exercise data. Enter a date and select a workout. \nIf the workout does not exist, add it by selecting new." 

    def __init__(self, parent, exercise_manager, name):
        super().__init__(parent, exercise_manager, name)

        self.options = self.update_options()
        self.recent = self.data_manager.get_recent_records()

        self.data_entry_form = BasicForm(self.data_form.data_entry_frame, "Exercise Entry", [1,1])

        self.data_entry_form.create_name_entry("Exercise Name:", self.options, True, self.recent)

        self.data_entry_form.set_graph(self.graph)

        self.data_entry_form.create_weight_rep_entry(3, self.recent)

        self.data_entry_form.set_form_weights()

    def update_options(self):
        return sorted(self.data_manager.get_names())
    