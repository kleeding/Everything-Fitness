from gui.components.tracking_page import TrackingPage
from gui.components.basic_form import BasicForm

class WeightTracking(TrackingPage):

    info = "On this page you can add and remove your weight. Enter a date and input your weight. \nYou can also set a new goal weight. When saving, select the entry fields you want saved." 

    def __init__(self, parent, weight_manager, name):
        super().__init__(parent, weight_manager, name)
        
        self.data_entry_form = BasicForm(self.data_form.data_entry_frame, "Weight Entry", [1,1])

        defaults = self.data_manager.get_recent_record()
        default_c = (defaults[0][1], defaults[1])
        default_g = (defaults[0][2], defaults[1])

        self.data_entry_form.create_spin_entry("Current Weight:", 
                                               default_c,
                                               50.0,
                                               200.0,
                                               "%.1f", 
                                               0.1)
        
        self.data_entry_form.create_spin_entry("Goal Weight:", 
                                               default_g,
                                               50.0,
                                               200.0,
                                               "%.1f", 
                                               0.1)
        
        self.data_entry_form.set_form_weights()