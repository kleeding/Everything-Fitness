from gui.components.dashboard_widget import DashboardWidget

class WeightWidget(DashboardWidget):

    labels1 = [["Current", "-"],
               ["Goal", "-"],
               ["Estimated TTG", "-"]]

    labels2 = [["Day:", "-", "Week:", "-"],
               ["Month:", "-", "Year:", "-"]]

    def __init__(self, parent, weight_manager):
        super().__init__(parent, weight_manager)
        self.config(text="WEIGHT")

        self.create_info("", self.labels1, [1, 1], ['e', ''])
        self.create_info("Weight Change", self.labels2, [1, 1, 1, 1], ['e', '', 'e', ''])
        self.create_graph("widget_line", self.data_manager.get_series("widget_graph"), 130)
        self.create_trend()

        self.set_info_labels(self.data_manager.get_info())
        self.set_trend_labels(self.data_manager.get_trends())
