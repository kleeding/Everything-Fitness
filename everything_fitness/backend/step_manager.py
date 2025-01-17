from backend.data_manager import DataManager

class StepManager(DataManager):
    def __init__(self, name, step, today, dates, prev_dates):
        super().__init__(name, step, today, dates)
        self.previous_dates = prev_dates

        self.recent_steps = 0
        self.recent_goal = 0

        self.step_info = [0, 0, 0, 0]
        self.step_info_prev = [0, 0, 0, 0]

        self.trend_info = [0, 0, 0]

        self.calculate_info()
        self.calculate_trends()
        self.tracking_graph_data = self.data_to_tracking_series()
        self.widget_graph_data = self.data_to_widget_series()

    def calculate_info(self):
        if self.data[-1][0] != '19700101':
            self.recent_steps = self.data[0][1]
            self.recent_goal = self.data[0][2]
            self.step_info = self.calculate_steps(self.dates, [self.today] * 4)
            self.step_info_prev = self.calculate_steps(self.previous_dates, self.dates)

    def calculate_steps(self, start, until):
        steps = []

        for i in range(len(start)):
            steps.append(0)
            for step_count in self.data:
                if step_count[0] > until[i]:
                    pass
                elif start[i] >= step_count[0]:
                    break
                else:
                    steps[-1] += step_count[1]

        return steps

    def get_series_data(self):
        self.series_data = []

        for date in self.dates:
            plot_data = []
            for data in self.data:
                if date >= data[0]:
                    break
                if data[0] > self.today:
                    pass
                else:
                    plot_data.append(data)
            self.series_data.append(plot_data)

        return self.series_data[1:]

    def calculate_trends(self):
        trend = [0, 0, 0]

        for i in range(3):
            cal = self.step_info[i] - self.step_info_prev[i]
            if cal > 0:
                trend[i] = 2
            elif cal < 0:
                trend[i] = -1

        self.trend_info = trend

    def get_info(self):
        return self.step_info

    def get_trends(self):
        return self.trend_info
    