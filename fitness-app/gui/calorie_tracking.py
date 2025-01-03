from gui.components.tracking_page import TrackingPage
from gui.components.basic_form import BasicForm

class CalorieTracking(TrackingPage):

    info = "On this page you can add your daily consumed calories. Enter a date and input your total daily calories. \nYou can also set a new daily calorie goal. When saving, select the entry fields you want saved." 
    
    def __init__(self, parent, calorie_manager, name):
        super().__init__(parent, calorie_manager, name)
        
        self.data_entry_form = BasicForm(self.data_form.data_entry_frame, "Calorie Entry", [1,1])

        defaults = self.data_manager.get_recent_record()
        default_c = (defaults[0][1], defaults[1])
        default_g = (defaults[0][2], defaults[1])

        self.data_entry_form.create_spin_entry("Current Calories Consumed:", 
                                               default_c,
                                               0,
                                               20000,
                                               "%0.f", 
                                               1)
        
        self.data_entry_form.create_spin_entry("Daily Calorie Goal:", 
                                               default_g,
                                               0,
                                               20000,
                                               "%0.f", 
                                               1)
        
        self.data_entry_form.set_form_weights()