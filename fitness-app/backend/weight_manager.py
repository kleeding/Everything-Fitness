from backend.data_manager import DataManager

class WeightManager(DataManager):
    def __init__(self, name, weight, today, dates):
        super().__init__(name, weight, today, dates)

        self.current_weight = 0
        self.goal_weight = 0
        self.estimate_ttg = 0

        self.day_change = 0
        self.week_change = 0
        self.month_change = 0
        self.year_change = 0

        self.trend_info = [0,0,0]

        self.calculate_info()
        self.calculate_trends()
        self.tracking_graph_data = self.data_to_tracking_series()
        self.widget_graph_data = self.data_to_widget_series()

    def calculate_info(self):
        if self.data[-1][0] != '19700101':
            self.current_weight = self.data[0][1] # Current weight = most recent weigh-in
            self.goal_weight = self.data[0][2] # Goal weight = most recent goal
            self.estimate_ttg = self.cal_time_till_goal(self.current_weight, self.goal_weight)

            weight_change = self.calculate_weight_change()
            self.day_change = weight_change[0]
            self.week_change = weight_change[1]
            self.month_change = weight_change[2]
            self.year_change = weight_change[3]
    
    def cal_time_till_goal(self, current, goal):
        # Need to make this calculation based on trends, so that it gives brutally honest output from current habits
        weight_to_lose = goal - current
        return 'To be implemented'
    
    def calculate_weight_change(self):
        weight = []

        for date in self.dates:
            weight.append('-')
            for data in self.data:
                if date >= data[0]:
                    dif = self.data[0][1] - data[1]
                    weight[-1] = round(dif, 1)
                    break
                
        return weight
    
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
        recent_weight = self.data[0][1]
        recent_goal = self.data[0][2]

        needed_loss = recent_goal - recent_weight # the loss needed 

        trend = []

        changes = [self.day_change, self.week_change, self.month_change]
        for change in changes:
            if change == 0 or change == '-':
                trend.append(0)
            else:
                change_direction = change/abs(change)
                if needed_loss*change_direction > 0:
                    change_direction *= 2
                trend.append(change_direction)

        self.trend_info = trend

    # Change this
    def get_info(self):
        info = [self.current_weight,
                  self.goal_weight,
                  self.estimate_ttg,
                  self.day_change,
                  self.week_change,
                  self.month_change,
                  self.year_change]
        return info
    
    def get_trends(self):
        return self.trend_info
    
