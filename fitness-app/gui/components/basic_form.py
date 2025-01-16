from tkinter import Frame, Label, Spinbox, IntVar, DoubleVar, Entry, Checkbutton
from tkinter.ttk import Combobox

class BasicForm(Frame):
    def __init__(self, parent, form_title, size):
        super().__init__(parent)
        self.parent = parent
        self.size = size
        self.row_elements = 0
        self.col_elements = 0

        self.title_label = Label(parent, text=form_title)
        self.title_label.pack(padx=5, pady=(5,0), fill="x")

        self.entry_frame = Frame(parent)
        self.entry_frame.pack(padx=5, pady=(0,5), fill="both", expand=True)

        self.name_elements = []
        self.entry_elements = []

        self.recent = []
        self.lifts = []

    def create_spin_entry(self, title, default_value, start, end, _format, increment):
        title_label = Label(self.entry_frame, text=title)
        title_label.grid(padx=5, row=0, column=self.col_elements, sticky="s")

        default_data = DoubleVar(self)
        default_data.set(default_value[0])

        data_entry = Spinbox(self.entry_frame, width=5, from_=start, to=end, format=_format, increment=increment, textvariable=default_data)
        data_entry.grid(padx=5, row=1, column=self.col_elements, sticky="n")

        if default_value[1]:
            self.record_exists(data_entry, 1)
        else:
            self.record_exists(data_entry, 0)

        self.entry_elements.append(data_entry)

        self.row_elements = max(self.row_elements, 2)
        self.col_elements += 1

    def create_name_entry(self, title, options, custom, default):
        self.options = options

        if 'No lift records' in self.options:
            self.options.remove('No lift records')

        title_label = Label(self.entry_frame, text=title)
        title_label.grid(padx=5, row=0, column=self.col_elements, sticky="s")

        name_select = Combobox(self.entry_frame, values=self.options)
        if self.options:
            name_select.current(self.options.index(default[0][0][1]))
        name_select.bind("<<ComboboxSelected>>", self.lift_selection)
        name_select.grid(padx=5, row=1, column=self.col_elements, sticky="new")

        self.name_elements.append(name_select)

        self.row_elements = 3 if self.row_elements < 3 else self.row_elements

        if custom:
            custome_frame = Frame(self.entry_frame)
            custome_frame.grid(padx=5, row=2, column=self.col_elements, sticky="new")
            custome_frame.columnconfigure((0,1), uniform=True, weight=1)
            custome_frame.columnconfigure(2, uniform=True, weight=2)

            self.custom_name_var = IntVar()
            def enable_custom():
                if self.custom_name_var.get() == 1:
                    name_select.config(state="disabled")
                    name_custom.config(state="normal")
                else:
                    name_select.config(state="normal")
                    name_custom.delete(0, "end")
                    name_custom.config(state="disabled")

            checkbutton = Checkbutton(custome_frame,
                                      text="New Lift:",
                                      variable=self.custom_name_var,
                                      onvalue=1,
                                      offvalue=0,
                                      command=enable_custom)
            checkbutton.pack(padx=(0,5), side="left")

            name_custom = Entry(custome_frame, state="disabled")
            name_custom.pack(padx=0, side="left", fill="both", expand=True)

            self.name_elements.append(name_custom)
            self.row_elements = 4 if self.row_elements < 4 else self.row_elements

        ## Submitted Lifts
        submitted_frame = Frame(self.entry_frame)
        submitted_frame.grid(padx=5, row=3, column=self.col_elements, sticky="new")
        submitted_frame.columnconfigure((0,1), uniform=True, weight=1)
        submitted_frame.columnconfigure(2, uniform=True, weight=2)
        
        submitted_label = Label(submitted_frame, text="Submitted:")
        submitted_label.pack(padx=(0,5), side="left")

        self.submitted_lifts = Combobox(submitted_frame)
        self.submitted_lifts.bind("<<ComboboxSelected>>", self.lift_selection)
        self.submitted_lifts.pack(padx=0, side="left", fill="both", expand=True)
        self.enable_submitted(default[1])
        if default[1]:
            self.lifts = self.names_from_records(default[0])
            self.recent = default[0] if default[1] else []
            self.submitted_lifts.config(values=self.lifts)
            self.submitted_lifts.current(0)        
            name_select.current(self.options.index(self.submitted_lifts.get()))
            self.enable_submitted(True)

        self.col_elements += 1

    def create_weight_rep_entry(self, num, default):
        weight_reps_frame = Frame(self.entry_frame)
        weight_reps_frame.grid(row=0, column=self.col_elements, rowspan=num+1, sticky="news")
        weight_reps_frame.grid_columnconfigure((0,2), weight=2)
        weight_reps_frame.grid_columnconfigure((1,3), weight=1)

        weight_label = Label(weight_reps_frame, text="Weight")
        weight_label.grid(padx=5, pady=5, row=0, column=0)
        reps_label = Label(weight_reps_frame, text="Reps")
        reps_label.grid(padx=5, pady=5, row=0, column=2)

        for i in range(num):
            weight_entry = Spinbox(weight_reps_frame, width=5, from_=0, to=500)
            weight_entry.grid(padx=2, pady=2, row=i + 1, column=0)
            self.entry_elements.append(weight_entry)

            x_label = Label(weight_reps_frame, text="x")
            x_label.grid(row=i + 1, column=1)

            reps_entry = Spinbox(weight_reps_frame, width=5, from_=0, to=100)
            reps_entry.grid(padx=2, pady=2, row=i + 1, column=2)
            self.entry_elements.append(reps_entry)

        self.row_elements = num if self.row_elements < num else self.row_elements

        if default[1]:
            self.set_weights_reps(self.recent[0])

    def set_form_weights(self):
        for i in range(self.row_elements):
            self.entry_frame.rowconfigure(i, weight=1)
            # pass
        for i in range(self.col_elements):
            self.entry_frame.columnconfigure(i, uniform=True, weight=1)

    def get_elements(self):
        return self.entry_elements

    def get_element_inputs(self):
        inputs = []

        name = self.get_name()

        if name != "":
            inputs.append(name)
        for element in self.entry_elements:  
            inputs.append(element.get())
        return inputs

    def get_name(self):
        if len(self.name_elements) > 0:
            if self.custom_name_var.get() == 0:
                return self.name_elements[0].get()
            else:
                return self.name_elements[1].get()
        return ""

    def set_elements(self, record, name):
        if name == 'exercise':
            self.set_exercise_elements(record)
            return

        if len(record) == 0:
            self.set_completed(False)
            return

        if len(record[0]) - 1 == len(self.entry_elements):
            for i in range(len(self.entry_elements)):
                _input = record[0][i + 1]
                self.set_spin_element(self.entry_elements[i], _input)
                self.record_exists(self.entry_elements[i], _input)
        else:
            self.set_completed(False)

    def set_spin_element(self, element, value):
        element.delete(0, "end")
        element.insert(0, value)

    def record_exists(self, element, _input):
        if _input not in [0, ""]:
            element.config(bg="#a9f5a4")
        else:
            element.config(bg="#f2b6a7")

    def set_completed(self, completed):
        if completed:
            for i in range(len(self.entry_elements)):
                self.record_exists(self.entry_elements[i], 1)
        else:
            for i in range(len(self.entry_elements)):
                self.record_exists(self.entry_elements[i], 0)

    def enable_submitted(self, enable):
        if enable:
            self.submitted_lifts.config(state="normal")
            self.submitted_enabled = True
        else:
            self.submitted_lifts.config(state="disabled")
            self.submitted_enabled = False

    def names_from_records(self, records):
        names = []
        for record in records:
            if record[0] != '19700101' and record[1] != 'No lift records':
                names.append(record[1])

        return sorted(names)

    def set_submitted_lifts(self, lifts):
        self.submitted_lifts.config(values=lifts)

    def set_exercise_elements(self, records):
        if len(records) == 0:
            self.recent = []
            if self.submitted_enabled:
                self.lifts = []
                self.set_submitted_lifts(self.lifts)
                self.submitted_lifts.set("")
                self.enable_submitted(False)
                return
            return

        self.recent = records

        self.lifts = self.names_from_records(records)
        self.set_submitted_lifts(self.lifts)
        self.submitted_lifts.current(0)
        self.name_elements[0].current(self.options.index(self.submitted_lifts.get()))
        self.enable_submitted(True)
        self.set_weights_reps(self.recent[0])
        self.graph.enable_series(self.submitted_lifts.get())

    def lift_selection(self, event):
        value = event.widget.get()

        if value in self.lifts:
            self.name_elements[0].current(self.options.index(value))
            self.submitted_lifts.current(self.lifts.index(value))
            self.set_weights_reps(self.recent[self.lifts.index(value)])
        else:
            record = ["", "", 0, 0, 0, 0, 0, 0]
            self.set_weights_reps(record)

        self.graph.enable_series(value)

    def set_graph(self, graph):
        self.graph = graph

    def set_weights_reps(self, record):
        for i in range(len(self.entry_elements)):
            input = record[i+2]
            self.set_spin_element(self.entry_elements[i], input)

    def update_form(self, name, records, options, mode):
        if name == "exercise":
            self.options = options
            self.name_elements[0].config(values=self.options)
            if records != []:
                self.recent = sorted(records, key=lambda x: x[1])
                self.lifts = self.names_from_records(records)

                self.set_submitted_lifts(self.lifts)

                lift_name = ""
                if mode == "saving":
                    lift_name = self.get_name()
                    self.enable_submitted(True)
                elif mode == "deleting":
                    lift_name = self.lifts[0]
                    self.name_elements[0].current(self.options.index(lift_name))

                self.submitted_lifts.current(self.lifts.index(lift_name))
                self.set_weights_reps(self.recent[self.lifts.index(lift_name)])
            else:
                self.submitted_lifts.set("")
                self.enable_submitted(False)
                self.set_weights_reps(["", "", 0, 0, 0, 0, 0, 0])
        else:
            if records != []:
                self.set_completed(True)
            else:
                self.set_completed(False)
                