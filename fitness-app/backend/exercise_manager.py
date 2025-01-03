from .data_manager import DataManager

class ExerciseManager(DataManager):
    def __init__(self, name, exercise, today, dates):
        super().__init__(name, exercise, today, dates)
        self.lift_names = self.find_names()
        self.lift_data = self.sort_lift_data()

        self.recent_lifts = ["-", "-", "-"]
        self.current_lifts = [0, 0, 0]
        self.pbs_lifts = [0, 0, 0]
        
        self.weight_moved = [0, 0, 0]
        self.time_worked = [0, 0, 0]

        self.calculate_info()
        self.tracking_graph_data = self.data_to_tracking_series()

    def check_if_empty(self):
        if len(self.data) == 0:
            tup = ('19700101', 'No lift records', 0, 0, 0, 0, 0, 0)
            self.data.append(tup) # ADding a dummy record

    def find_names(self):
        names = []

        for lift in self.data:
            if lift[1] not in names:
                names.append(lift[1])

        if 'No lift records' in names:
            names.remove('No lift records')

        return names
    
    def get_names(self):
        return self.find_names()
    
    def sort_lift_data(self):
        lift_data = {}

        for name in self.lift_names:
            lifts = []
            for row in self.data:
                if row[1] == name:
                    lifts.append((row[0],)+row[2:])
            lift_data[name] = lifts

        return lift_data
    
    def get_lift_data(self):
        return self.lift_data
    
    def calculate_info(self):
        self.lift_names = self.find_names()
        self.lift_data = self.sort_lift_data()

        self.recent_lifts = self.lift_names[:3]
        self.current_lifts = self.get_recent_currents()
        self.pbs_lifts = self.get_recent_pbs()
        
        self.weight_moved, self.time_worked = self.get_weight_moved_time_worked()

    def get_recent_currents(self):
        current = []
        for lift in self.recent_lifts:
            max_lift = max(self.lift_data[lift][0][1],self.lift_data[lift][0][3],self.lift_data[lift][0][5])
            current.append(max_lift)
        return current

    def get_recent_pbs(self):
        pbs = []

        for lift in self.recent_lifts:
            pb = self.lift_pb(lift)
            pbs.append(pb)

        return pbs
    
    def lift_pb(self, lift):
        pb = 0

        lifts = self.lift_data[lift]

        for lift in lifts:
            c_max = max(lift[1], lift[3], lift[5])
            if c_max > pb:
                pb = c_max

        return pb
    
    def get_weight_moved_time_worked(self):
        weight_moved = []
        time_worked = []

        for date in self.dates:
            weight, reps = self.cal_work(date)
            weight_moved.append(weight)
            time_worked.append(reps * 4 // 6 / 10)

        return weight_moved[1:], time_worked[1:]
    
    def cal_work(self, since):
        weight = 0
        reps = 0

        for lift in self.data:
            if lift[0] > since:
                weight += lift[2] * lift[3]
                weight += lift[4] * lift[5]
                weight += lift[6] * lift[7]

                reps += (lift[3] + lift[5] + lift[7])

        return weight, reps
    
    def data_to_tracking_series(self):
        self.lift_names = self.find_names()
        self.lift_data = self.sort_lift_data()
        series_data = {}
        date = self.dates[-1]
        
        for name in self.lift_names:
            x = []
            y1, y2 = [], []
            for lift in self.lift_data[name]:
                if date > lift[0]:
                    break
                elif lift[0] > self.today:
                    pass
                else:
                    x.append(self.day_in_date(2, lift[0]))
                    min_y, max_y = 10000, -10000
                    for i in range(3):
                        entry = lift[i * 2 + 1]
                        if entry > 0:
                            min_y = min(min_y, entry)
                            max_y = max(max_y, entry)
                    if min_y < 10000:
                        y1.append(min_y)
                    if max_y > -10000:
                        y2.append(max_y)
                series_data[name] = [x, [y1, y2]]

        return series_data

    def get_info(self):
        self.calculate_info()
        info = []
        max_lifts = min(len(self.lift_names), 3)
        for i in range(max_lifts):
            info.append(self.recent_lifts[i])
            info.append(self.current_lifts[i])
            info.append(self.pbs_lifts[i])

        for i in range(3 - max_lifts):
            info.append('-')
            info.append(0)
            info.append(0)
        
        info += self.weight_moved[:3]
        info += self.time_worked[:3]

        return info