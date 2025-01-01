from tkinter import Frame, Label, Button
from gui.components.date_entry import DateEntry

class DataForm(Frame):
    def __init__(self, parent, page_info):
        super().__init__(parent)
        self.parent = parent

        self.info_label = Label(self, text=page_info, height=2) # Clean up the page info
        self.info_label.pack(padx=10, pady=10, fill="x")

        self.date_entry = DateEntry(self)
        self.date_entry.pack(padx=5, pady=5, side="left", fill="both")

        self.data_entry_frame = Frame(self, relief="sunken", borderwidth = 1)
        self.data_entry_frame.pack(padx=5, pady=5, side="left", fill="both", expand=True)
        self.data_entry_frame.grid_columnconfigure((0,1), uniform=True, weight=1)
        
        self.button_frame = Frame(self, relief="sunken", borderwidth = 1)
        self.button_frame.pack(padx=5, pady=5, side="right", fill="both")

        self.add_b = Button(self.button_frame, text="Save", command=self.save_record)
        self.add_b.pack(padx=10, pady=(30,5), fill="both", expand=True)

        self.remove_b = Button(self.button_frame, text="Remove", command=self.delete_record)
        self.remove_b.pack(padx=10, pady=(5,30), fill="both", expand=True)

    def load_record(self):
        date = self.date_entry.get_date()
        date_str = date[2] + date[1] + date[0]
        self.parent.load_record(date_str)
        
    def save_record(self):
        date = self.date_entry.get_date()
        date_str = date[2] + date[1] + date[0]
        self.parent.save_record(date_str)

    def delete_record(self):
        date = self.date_entry.get_date()
        date_str = date[2] + date[1] + date[0]
        self.parent.delete_record(date_str)