from tkinter import Canvas, Frame, LabelFrame, Button

class Graph(Canvas):

    def __init__(self, parent, name, mode, enable_axis, series, size):
        super().__init__(parent)
        self.pagename = name
        self.parent = parent
        self.mode = mode
        self.enable_axis = enable_axis
        self.series = series
        self.legend = ["Week", "Month", "Year"]
        self.size = size
        self.series_canvas = []
        self.current_series = 0
        self.series_buttons = None

        self.setup_graph(self.mode)

    def setup_graph(self, mode):
        if mode == "line":
            self.marginx = 35
            self.marginy = 35
            
            if self.pagename == "exercise":
                self.size[1] += 50
                self.legend = ["Year"]
                self.xaxis = [["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]]
                self.xsteps_p = [365]
                self.xsteps_a = [12]
            else:
                self.xsteps_p = [7, self.series[0], 365]
                self.xsteps_a = [7, self.series[0], 12]
                    
                self.xaxis = [["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                              list(i + 1 for i in range(self.series[0])),
                              ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]]
                
                self.series = self.series[1:]

                self.create_buttons()

            self.create_mainframe()
            self.create_canvas()
            if self.pagename != "exercise":
                self.set_buttons()
        elif mode == "widget_line" or mode == "widget_bar":
            self.marginx = [5, 0]
            self.marginy = [25, 0]
            self.create_mainframe()
            self.create_canvas()
            if mode == "widget_line":
                self.plot_widget_line()
            else:
                self.plot_widget_bar()

    def create_mainframe(self):
        self.graph_frame = LabelFrame(self, text="Graph", name="main_frame")
        if self.mode == "line":
            self.graph_frame.pack(padx=5, pady=5, fill="both", expand=True)
        else:
            self.graph_frame.pack(fill="both", expand=True)

    def create_buttons(self):
        self.series_buttons = []
        button_frame = Frame(self.parent)
        button_frame.pack(pady=(10,0))

        for i in range(len(self.series)):
            buttons = []
            button = Button(button_frame, text=self.legend[i], width=10, bg="#A10A10A10")
            button.pack(padx=5, pady=5, side="left", fill="x", expand=True)
            buttons.append(button)
            self.series_buttons.append(buttons)

    def set_buttons(self):
        for i in range(len(self.series_buttons)):
            for element in self.series_buttons[i]:
                element.config(command=lambda x = i: self.enable_series(x))

    def create_canvas(self):
        if self.mode == "line" and self.pagename != "exercise":
            for i in range(len(self.series)):
                graph_canvas = Canvas(self.graph_frame, width=self.size[0], height=self.size[1], bg="white")
                self.set_title(graph_canvas, i)
                self.plot_series_line(graph_canvas, i)
                if len(self.series[i]) != 0:
                    self.set_key(graph_canvas, ["#2fd033", "#41A5BE"], ["Current", "Goal"])
                self.series_canvas.append(graph_canvas)
                self.current_series = 0
                self.series_canvas[self.current_series].pack()
        elif self.mode == "line" and self.pagename == "exercise":
            self.series_canvas = {}
            for key in self.series:
                graph_canvas = Canvas(self.graph_frame, width=self.size[0], height=self.size[1], bg="white")
                self.set_title(graph_canvas, key)
                self.plot_series_line(graph_canvas, key)
                if len(self.series[key]) != 0 and self.series[key][0] != '19700101':
                    self.set_key(graph_canvas, ["#41A5BE", "#2fd033"], ["High", "Low"])
                self.series_canvas[key] = graph_canvas
            for key in self.series:
                self.series_canvas[key].pack()
                self.current_series = key
                break

        elif self.mode == "widget_line" or self.mode == "widget_bar":
            self.graph_canvas = Canvas(self.graph_frame, width=self.size[0], height=self.size[1], name="widget_canvas")
            self.graph_canvas.pack()

    def plot_series_line(self, canvas, num):
        if len(self.series[num]) > 0 and self.pagename == "exercise": # in this case num is the key
            min_y, max_y, y1, y2, xstart, stepx = self.plot_axis_line(canvas, num, 0, 10)
            self.plot_line(canvas, num, min_y, max_y, y1, y2, xstart, stepx)
        elif len(self.series[num]):
            min_y, max_y, y1, y2, xstart, stepx = self.plot_axis_line(canvas, "", num, 10)
            self.plot_line(canvas, num, min_y, max_y, y1, y2, xstart, stepx)
        else:
            canvas.create_text(self.size[0]/2, self.size[1]/2, text="No data")   

    def plot_line(self, canvas, num, max_y, min_y, y1, y2, xstart, stepx):
        x = self.series[num][0]
        rel_data = []

        for data in self.series[num][1:]:
            for lines in data:
                rel_y = []
                for data_point in lines:
                    rel = (data_point - min_y) / (max_y - min_y)
                    rel = (rel * (y2 - y1)) + y1
                    rel_y.append(rel)
                rel_data.append(rel_y)

        self.line(canvas, stepx, xstart, x, rel_data[0], "#41A5BE", 1)
        if len(rel_data) > 1:
            self.line(canvas, stepx, xstart, x, rel_data[1], "#2fd033", 0)

    def line(self, canvas, stepx, xstart, x, y, colour, mode):
        x_2, y_2 = 0, 0
        s = 3
        for i in range(len(y) - 1):
            x_1 = xstart + (x[i] - 1) * stepx
            x_2 = xstart + (x[i + 1] - 1) * stepx
            y_1 = y[i]
            y_2 = y[i + 1]
            canvas.create_line(x_1, y_1, x_2, y_2, fill=colour, width=3)
            if mode == 1 and self.pagename != "exercise":
                canvas.create_oval(x_1 - s, y_1 - s, x_1 + s, y_1 + s, fill="#be5a41", outline="#be5a41")
        if mode == 1 and self.pagename != "exercise":
            canvas.create_oval(x_2 - s, y_2 - s, x_2 + s, y_2 + s, fill="#be5a41", outline="#be5a41")

        if len(y) == 1:
            x_1 = xstart + (x[0] - 1) * stepx
            y_1 = y[0]
            if mode == 1:
                canvas.create_oval(x_1 - s, y_1 - s, x_1 + s, y_1 + s, fill="#be5a41", outline="#be5a41")

    def plot_widget_line(self):
        y1, y2 = self.marginy[0], self.size[1] - self.marginy[1]
        y_dif = y2 - y1

        if len(self.series):
            xstep = (self.size[0]) / (len(self.series) + 1)
            max_data = -10000
            min_data =  10000
            for i in range(len(self.series)):
                max_data = max(max_data, self.series[i][1])
                min_data = min(min_data, self.series[i][1])
            if max_data == min_data:
                max_data *= 1.02
                min_data *= .98
            dif = max_data - min_data
            p = []
            for i in range(len(self.series)):
                x = self.size[0] - ((i + 1) * xstep) + self.marginx[0]
                p.append(x)
                rel_y = max(((self.series[i][1] - min_data) / dif), 0.05) * y_dif
                p.append(y2 - rel_y)

            if len(p) >= 4:
                self.graph_canvas.create_line(*p, width=1, fill="#41a5be") #"#be5a41"

            for i in range(len(p) // 2):
                x = p[i * 2]
                y = p[i * 2 + 1]
                self.graph_canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="#be5a41", outline="#be5a41")
                self.graph_canvas.create_text(x, y, text=self.series[i][1], angle=45, anchor="s")
        else:
            self.graph_canvas.create_text(self.size[0] / 2, self.size[1] / 2, text="No data")

    def plot_widget_bar(self):
        y1, y2 = self.marginy[0], self.size[1] - self.marginy[1]
        y_dif = y2 - y1

        if len(self.series):
            xstep = (self.size[0]) / (len(self.series) + 1)
            pwidth = xstep * 0.2
            max_data = -10000
            min_data =  10000
            for i in range(len(self.series)):
                max_data = max(max_data, self.series[i][1])
                min_data = min(min_data, self.series[i][1])
            if max_data == min_data:
                max_data *= 1.02
                min_data *= .98
            if max_data == min_data == 0:
                max_data = 100
                min_data = 0
            dif = max_data - min_data
            for i in range(len(self.series)):
                xp = self.size[0] - ((i + 1) * xstep) + self.marginx[0]
                rel_y = max(((self.series[i][1] - min_data) / dif), 0.05) * y_dif
                y_2 = y2 - rel_y
                self.graph_canvas.create_line(xp, y2, xp, y_2, width=pwidth, fill="#41A5BE")
                self.graph_canvas.create_text(xp, y_2, text=self.series[i][1], angle=45, anchor="s")
        else:
            self.graph_canvas.create_text(self.size[0] / 2, self.size[1] / 2, text="No data")

    def plot_axis_line(self, canvas, key, num, ysteps):
        min_y =  100000
        max_y = -100000
        if self.pagename == "exercise":
            if key == 'No lift records':
                return 0, 10000, 0, 100, 10, 10
            min_y = min(self.series[key][1][0])
            max_y = max(self.series[key][1][1])
        else:
            for data in self.series[num][1]:
                for data_p in data:
                    min_y = min(min_y, data_p)
                    max_y = max(max_y, data_p)

        min_y, max_y = min_y*.98, max_y*1.02

        self.marginx = 25 + len(str(int(max_y))) * 5

        x1 = self.marginx
        x2 = self.size[0] - self.marginx
        y1 = self.marginy
        y2 = self.size[1] - self.marginy

        ## Sort x-axis
        if self.pagename == "exercise":
            num = 0

        xstep_p = self.xsteps_p[num]
        xstep_a = self.xsteps_a[num]

        stepx_axis = (x2 - x1) / (xstep_a + 2)

        axis_x_start = x1 + (stepx_axis*1.75)
        axis_x_end = x2 - (stepx_axis/1.75)

        stepx_plot = (axis_x_end - axis_x_start) / (xstep_p)

        if self.enable_axis:
            for i in range(len(self.xaxis[num])):

                xpos = axis_x_start + (stepx_axis * (i))

                axis_text = self.xaxis[num][i]
                canvas.create_line(xpos, y2, xpos, y2+3)
                canvas.create_text(xpos, y2 + 5, text=axis_text, angle=45, anchor="ne")

            # sort y-axis
            dif = (max_y - min_y) / ysteps
            stepy = (y2 - y1) / ysteps

            next_y = min_y
            for i in range(ysteps + 1):
                y = y2 - (i*stepy)
                canvas.create_line(x1 - 2, y, x1, y)
                canvas.create_text(x1 - 5, y, text=int(next_y), anchor="e")
                next_y += dif

            canvas.create_line(x1, y1, x1, y2 + 5)
            canvas.create_line(x1 - 5, y2, x2, y2)

        return min_y, max_y, y1, y2, axis_x_start, stepx_plot

    def enable_series(self, num):
        if len(self.series_canvas):
            self.series_canvas[self.current_series].pack_forget()
        self.current_series = num
        self.series_canvas[self.current_series].pack()

    def update_tracking_graph(self, series):
        if self.mode == "line":
            self.series = series
            if self.pagename != "exercise":
                self.series = series[1:]

                self.xsteps_p[1] = series[0]
                self.xsteps_a[1] = series[0]
                self.xaxis[1] = list(i + 1 for i in range(series[0]))

        current_graph = self.current_series
        if len(self.series_canvas) != 0:
            self.series_canvas[self.current_series].pack_forget()
        self.series_canvas = []

        self.create_canvas()
        if self.pagename != "exercise":
            self.enable_series(current_graph)
    
    def update_widget_graph(self, series):
        if self.mode in ["widget_line", "widget_bar"]:
            self.series = series
            if self.series[-1][0] == '19700101':
                self.series = []
            self.graph_canvas.pack_forget()       
            self.create_canvas()
            self.plot_widget_line() if self.mode == "widget_line" else self.plot_widget_bar()

    def set_title(self, canvas, title):
        if type(title) == int:
            title = self.legend[title]
        x = self.size[0] / 2
        y = 20
        canvas.create_text(x, y, font=('bold', 15), text=title)

    def set_key(self, canvas, colours, text):
        g = 10
        x1 = self.marginx + g
        y1 = self.size[1] - (self.marginy * 2)
        r_size = 20
        x2 = x1 + r_size
        y2 = y1 - r_size - g
        canvas.create_rectangle(x1, y1, x2, y1 - r_size, fill=colours[0], outline=colours[0])
        canvas.create_rectangle(x1, y2, x2, y2 - r_size, fill=colours[1], outline=colours[1])
        x3 = x2 + g
        y3a = y1 - (r_size / 2)
        y3b = y2 - (r_size / 2)
        
        canvas.create_text(x3, y3a, font=(r_size), text = text[1], anchor="w")
        canvas.create_text(x3, y3b, font=(r_size), text = text[0], anchor="w")