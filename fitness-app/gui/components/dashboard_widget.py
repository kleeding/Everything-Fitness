from tkinter import LabelFrame, Frame, Label
from gui.components.graph import Graph

class DashboardWidget(LabelFrame):
    def __init__(self, parent, data_manager):
        super().__init__(parent)
        self.parent = parent

        self.data_manager = data_manager

        self.output_labels = []
        self.graph = 0
        self.trend_labels = []

    def create_frame(self, label):
        if len(label) > 0:
            main_frame = LabelFrame(self, text=label)
        else:
            main_frame = Frame(self)
        main_frame.pack(padx=5, pady=5, fill="both", expand=True)
        info_frame = Frame(main_frame)
        info_frame.pack(fill="x", expand=True)
        return info_frame

    def create_info(self, frame_label, info_labels, weightings, sticks):
        frame = self.create_frame(frame_label)

        for i in range(len(weightings)):
            frame.columnconfigure(i, uniform=True, weight=weightings[i])

        for i in range(len(info_labels)):
            for j in range(len(info_labels[i])):
                text = info_labels[i][j]
                label = Label(frame, text=text)
                label.grid(padx=5, pady=2, row=i, column=j, sticky=sticks[j])
                if text == "-":
                    self.output_labels.append(label)

    def create_graph(self, mode, data, height):
        epoch_date = '19700101'
        if data[-1][0] == epoch_date:
            data = []

        frame = self.create_frame("")
        frame.pack(fill="both", expand=True)

        self.graph = Graph(frame,
                           "",
                           mode,
                           False,
                           data,
                           [320, height]) # <- 320 for a good fit
        self.graph.pack(fill="both", expand=True)

    def create_trend(self):
        frame = self.create_frame("Trend")
        frame.grid_columnconfigure((0,1,2,3,4,5), uniform="equal", weight=1)

        trend_label_text = ["Day:", "Week:", "Month:"]

        for trend_text in trend_label_text:
            item_frame = Frame(frame)
            item_frame.pack(padx=15, side="left", fill="x", expand=True)
            trend_label = Label(item_frame, text=trend_text)
            trend_label.pack(side="left", expand=True)
            trend_output = Label(item_frame, text="-")
            trend_output.pack(side="left", expand=True)
            self.trend_labels.append(trend_output)

    def set_info_labels(self, outputs):
        for output in zip(self.output_labels, outputs):
            output[0].config(text=output[1])

    def set_trend_labels(self, trends):
        for trend in zip(self.trend_labels, trends):
            self.set_trend(trend[0], trend[1])

    trend_config = [["↘","green"], ["↘","red"], ["-","blue"], ["↗","red"], ["↗","green"]]

    def set_trend(self, widget, data):
        index = int(data) + 2
        widget.config(text=self.trend_config[index][0],
                      font=('Segoe UI', 13),
                      fg=self.trend_config[index][1])
        # if data == 2:
        #     return widget.config(text="↗", font=('Segoe UI', 13), fg="green")
        # elif data == 1:
        #     return widget.config(text="↗", font=('Segoe UI', 13), fg="red")
        # elif data == -1:
        #     return widget.config(text="↘", font=('Segoe UI', 13), fg="red")
        # elif data == -2:
        #     return widget.config(text="↘", font=('Segoe UI', 13), fg="green")
        # else:
        #     return widget.config(text="-", font=('Segoe UI', 13), fg="blue")

    def refresh(self):
        if len(self.output_labels) > 0:
            self.set_info_labels(self.data_manager.get_info())
        if len(self.trend_labels) > 0:
            self.data_manager.calculate_trends()
            self.set_trend_labels(self.data_manager.get_trends())
        if self.graph != 0:
            self.graph.update_widget_graph(self.data_manager.get_series("widget_graph"))
