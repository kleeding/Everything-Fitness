from tkinter import Frame
from gui.components.data_form import DataForm
from gui.components.graph import Graph

class TrackingPage(Frame):

    def __init__(self, parent, data_manager, name):
        super().__init__(parent)
        self.data_manager = data_manager
        self.name = name

        self.data_form = DataForm(self, self.info)
        self.data_form.pack(fill="both")

        series_data = self.data_manager.get_tracking_graph_data()

        self.graph = Graph(self, 
                        self.name,
                        "line",
                        True,
                        series_data,
                        [700,400])
        self.graph.pack(fill="both", expand=True)

    def load_record(self, date):
        records = self.data_manager.get_records(date)
        self.data_entry_form.set_elements(records, self.name)

    def save_record(self, date):
        record_data = self.data_entry_form.get_element_inputs()
        self.data_manager.add_record(date, record_data, self.name)

        self.update_form(date, "saving")
        self.update_graph()

    def delete_record(self, date):
        records = self.data_manager.get_records(date)
        if self.name == "exercise":
            lift = self.data_entry_form.get_name()
            for record in records:
                if lift == record[1]:
                    self.data_manager.remove_record(record, self.name)
                    break
        else:
            if len(records) == 1:
                self.data_manager.remove_record(records[0], self.name)
        

        self.update_form(date, "deleting")
        self.update_graph()

    def update_form(self, date, mode):
        records = self.data_manager.get_records(date)
        if self.name == "exercise":
            options = self.update_options()
        else:
            options = []
        self.data_entry_form.update_form(self.name, records, options, mode)

    def update_graph(self):
        series_data = self.data_manager.data_to_tracking_series()
        self.graph.update_tracking_graph(series_data)