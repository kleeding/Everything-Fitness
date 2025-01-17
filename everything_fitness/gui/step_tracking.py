from gui.components.tracking_page import TrackingPage
from gui.components.basic_form import BasicForm

class StepTracking(TrackingPage):

    info = "On this page you can add and remove your daily total steps. Enter a date and input the total steps taken in that day. \nYou can also set a new daily step goal. When saving, select the entry fields you want saved."

    def __init__(self, parent, weight_manager, name):
        super().__init__(parent, weight_manager, name)

        self.data_entry_form = BasicForm(self.data_form.data_entry_frame, "Step Entry", [1,1])

        defaults = self.data_manager.get_recent_record()
        default_c = (defaults[0][1], defaults[1])
        default_g = (defaults[0][2], defaults[1])

        self.data_entry_form.create_spin_entry("Current Steps Taken:",
                                               default_c,
                                               0,
                                               20000,
                                               "%0.f", 
                                               1)

        self.data_entry_form.create_spin_entry("Daily Step Goal:",
                                               default_g,
                                               0,
                                               20000,
                                               "%0.f", 
                                               1)

        self.data_entry_form.set_form_weights()
