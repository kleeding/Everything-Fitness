from gui.components.dashboard_widget import DashboardWidget

class CalorieWidget(DashboardWidget):

    labels1 = [["Day:", "-", "Week:", "-"], 
               ["Month:", "-", "Year:", "-"]]
    
    def __init__(self, parent, calorie_manager):
        super().__init__(parent, calorie_manager) 
        self.config(text="CALORIES")

        self.create_info("", self.labels1, [1, 1, 1, 1], ['e', '', 'e', ''])
        self.create_graph("widget_bar", self.data_manager.get_series("widget_graph"), 95)
        self.create_trend()

        self.set_info_labels(self.data_manager.get_info())
        self.set_trend_labels(self.data_manager.get_trends())