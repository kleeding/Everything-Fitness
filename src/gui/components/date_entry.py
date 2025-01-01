from tkinter import Frame, Label, Spinbox, StringVar
from datetime import datetime, date

class DateEntry(Frame):
    def __init__(self, parent):
        super().__init__(parent, relief="sunken", borderwidth = 1)
        self.grid_columnconfigure((0,1), uniform=True, weight=1)
        self.parent = parent

        self.setup_labels()
        self.setup_spinboxs()

    def setup_labels(self):
        self.date_label = Label(self, text="Date")
        self.date_label.grid(padx=5, pady=(5,15), row=0, column=0, columnspan=2, sticky="new")

        self.day_label = Label(self, text="Day:")
        self.day_label.grid(padx=3, pady=3, row=1, column=0, sticky="e")
        self.month_label = Label(self, text="Month:")
        self.month_label.grid(padx=3, pady=3, row=2, column=0, sticky="e")
        self.year_label = Label(self, text="Year:")
        self.year_label.grid(padx=3, pady=(5,20), row=3, column=0, sticky="e")

    def setup_spinboxs(self):
        self.selected = datetime.today().strftime('%d-%m-%Y').split("-")
        day, month, year = StringVar(self), StringVar(self), StringVar(self)
        day.set(self.selected[0])
        month.set(self.selected[1])
        year.set(self.selected[2])
        
        self.calculate_days_in_month(self.selected[1], self.selected[2])

        self.day_entry = Spinbox(self, width=5, from_=1, to=self.max_days, format="%02.0f", textvariable=day, command=self.change_day)
        self.day_entry.grid(padx=3, pady=3, row=1, column=1)
        self.month_entry = Spinbox(self, width=5, from_=1, to=12, format="%02.0f", textvariable=month, command=self.set_max_days)
        self.month_entry.grid(padx=3, pady=3, row=2, column=1)
        self.year_entry = Spinbox(self, width=5, from_=2024, to=2090, textvariable=year)
        self.year_entry.grid(padx=2, pady=(5,20), row=3, column=1)

    def get_date(self):
        day = self.day_entry.get()
        month = self.month_entry.get()
        year = self.year_entry.get()
        return [day, month, year]
    
    ## REWORK THIS, IS UGLY AF
    def change_day(self):
        day = self.day_entry.get()
        if self.selected[0] == day and day == '01':
            if self.selected[1] == '01':
                self.set_element(self.month_entry, '12')
                self.selected[1] = '12'
                year = str(int(self.selected[2]) - 1)
                self.set_element(self.year_entry, year)
                self.selected[2] = year
            else:
                month = str(int(self.selected[1]) - 1)
                month = '0'+ month if len(month) == 1 else month
                self.set_element(self.month_entry, month)
                self.selected[1] = month
            self.set_max_days()
            self.set_element(self.day_entry, self.max_days)
            self.selected[0] = self.max_days
        elif int(self.selected[0]) == int(day) and int(day) == self.max_days:
            if self.selected[1] == '12':
                self.set_element(self.month_entry, '01')
                self.selected[1] = '01'
                year = str(int(self.selected[2]) + 1)
                self.set_element(self.year_entry, year)
                self.selected[2] = year
            else:
                month = str(int(self.selected[1]) + 1)
                month = '0'+ month if len(month) == 1 else month
                self.set_element(self.month_entry, month)
                self.selected[1] = month
            self.set_element(self.day_entry, '01')
            self.set_max_days()
            self.selected[0] = '01'
        else:
            self.selected[0] = day

        self.parent.load_record()

    def set_max_days(self):
        self.selected[1] = self.month_entry.get()
        date_entry = self.get_date()
        self.calculate_days_in_month(date_entry[1], date_entry[2])
        self.day_entry.config(to=self.max_days)

    def calculate_days_in_month(self, month, year):
        if month == '12':
            days = (date(int(year) + 1, 1, 1) - date(int(year), int(month), 1)).days
        else:
            days = (date(int(year), int(month) + 1, 1) - date(int(year), int(month), 1)).days
        self.max_days = days

    def set_element(self, element, text):
        element.delete(0,"end")
        element.insert(0,text)