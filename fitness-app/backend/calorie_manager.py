from backend.data_manager import DataManager

class CalorieManager(DataManager):
    def __init__(self, name, calorie, today, dates, prev_dates):
        super().__init__(name, calorie, today, dates)
        self.previous_dates = prev_dates

        self.recent_calories = 0
        self.recent_goal = 0

        self.calorie_info = [0,0,0,0]
        self.calorie_counter = 0
        self.calorie_info_prev = [0,0,0,0]
        self.calorie_counter_prev = 0

        self.trend_info = [0,0,0]

        self.calculate_info()        
        self.calculate_trends()
        self.tracking_graph_data = self.data_to_tracking_series()
        self.widget_graph_data = self.data_to_widget_series()
    
    def calculate_info(self):
        self.recent_calories = self.data[0][1]
        self.recent_goal = self.data[0][2]
        self.calorie_info, self.calorie_counter = self.calculate_calories(self.dates, [self.today] * 4)
        self.calorie_info_prev, self.calorie_counter_prev = self.calculate_calories(self.previous_dates, self.dates)
    
    def calculate_calories(self, start, until):
        calories = []
        counter = []

        for i in range(len(start)):
            calories.append(0)
            counter.append(0)
            for calorie_count in self.data:
                if calorie_count[0] > until[i]:
                    pass
                elif start[i] >= calorie_count[0]:
                    break
                else:
                    calories[-1] += calorie_count[1]
                    counter[-1] += 1

        return calories, counter
    
    def get_series_data(self):
        series_data = []

        for date in self.dates:
            plot_data = []
            for data in self.data:
                if date >= data[0]:
                    break
                elif data[0] > self.today:
                    pass
                else:
                    plot_data.append(data)
            series_data.append(plot_data)

        return series_data[1:]

    def calculate_trends(self):
        trend = [0, 0, 0]

        daily_goal = self.data[0][2] # Need to make sure things like this don't fail when there are no datapoints

        for i in range(3):
            if self.calorie_counter[i] > 0:
                cal_avg = self.calorie_info[i] / self.calorie_counter[i]
            else:
                cal_avg = 0
            if self.calorie_counter_prev[i] > 0 :
                cal_avg_prev = self.calorie_info_prev[i] / self.calorie_counter_prev[i]
            else:
                cal_avg_prev = daily_goal

            cal_dif = cal_avg - cal_avg_prev
            cal_goal_dif = cal_avg - daily_goal

            if cal_dif > 0:
                # calorie consumption has increased
                if cal_goal_dif > 0:
                    # consumed more calories than goal
                    # UP AND BAD
                    trend[i] = 1
                else:
                    # consumed less or equal calories than goal
                    # UP AND GOOD
                    trend[i] = 2
            elif cal_dif < 0:
                # calorie consumption as decreased
                if cal_goal_dif < 0:
                    # consumed less than goal
                    # DOWN AND BAD
                    trend[i] = -1
                else:
                    # consumed more or equal to goal
                    # DOWN AND GOOD
                    trend[i] = -2

        self.trend_info = trend
    
    def get_info(self):
        return self.calorie_info
    
    def get_trends(self):
        return self.trend_info    