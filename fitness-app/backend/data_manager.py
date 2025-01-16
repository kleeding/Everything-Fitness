import sqlite3
from datetime import date

class DataManager():
    def __init__(self, name, data, today, dates):
        self.name = name
        self.today = today
        self.dates = dates
        self.data = sorted(data, key=lambda x: x[0],reverse=True)

        self.check_if_empty()

    def check_if_empty(self):
        if len(self.data) == 0:
            dummy_record = ('19700101', 0, 0)
            self.data.append(dummy_record)

    def get_recent_record(self):
        recent = [self.data[0], self.today == self.data[0][0]]
        return recent

    def get_recent_records(self):
        _date = self.data[0][0]
        recent = self.today == self.data[0][0]
        records = []
        for record in self.data:
            if _date == record[0]:
                records.append(record)
            else:
                return [records, recent]
        return [records, recent]

    # Return record at specific date
    def get_records(self, _date):
        records = []
        passed = False
        for record in self.data:
            if _date == record[0]:
                passed = True
                records.append(record)
            elif passed:
                pass
        return records

    # Convert string to int/float and create tuple
    def clean_record(self, date, record):
        clean_record = (date,)
        for i in range(len(record)):
            data = record[i].replace('-', '')
            data2 = data.replace('.', '')
            if data2.isnumeric():
                if data.isnumeric():
                    clean_record += (int(record[i]),)
                else:
                    clean_record += (float(record[i]),)
            else:
                clean_record += (record[i],)
        return clean_record

    def add_record(self, _date, record, name):
        record = self.clean_record(date, record)

        index = 0
        update = False
        ## Simplify this conditional
        if name == "exercise":  ## Remove conditional, keep single for loop
            for i in range(len(self.data)):
                if  _date > self.data[i][0]:
                    break
                if _date == self.data[i][0] and record[1] == self.data[i][1]: ## <- a and ((b and c) or c)
                    self.data[i] = record
                    update = True
                    break
                else:
                    index += 1
        else: ## Remove
            for i in range(len(self.data)):
                if _date > self.data[i][0]:
                    break
                if _date == self.data[i][0]:
                    self.data[i] = record
                    update = True
                    break
                else:
                    index += 1
        if not update:
            self.data.insert(index, record)

        self.save_to_database(record, name, update)
        epoch_date = '19700101'
        if self.data[-1][0] == epoch_date:
            self.data.remove(self.data[-1])
        self.calculate_info()

    def remove_record(self, record, name):
        if record in self.data:
            self.data.remove(record)
            self.remove_from_database(record, name)
        self.check_if_empty()
        self.calculate_info()

    def save_to_database(self, record, name, update):
        conn = sqlite3.connect('user.db')

        if name == "exercise":
            if update:
                data_insert_query = """UPDATE exercise
                                       SET weight1 = ?, reps1 = ?, weight2 = ?, reps2 = ?, weight3 = ?, reps3 = ? 
                                       WHERE date = ? and name = ?"""
                data_input_tuple = (record[2], record[3], record[4], record[5], record[6], record[7], record[0], record[1])
            else:
                data_insert_query = "INSERT INTO exercise (date, name, weight1, reps1, weight2, reps2, weight3, reps3) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
                data_input_tuple = record
        else:
            if update:
                data_insert_query = "UPDATE " + name + " SET " + name + "=?, goal=? WHERE date=?"
                data_input_tuple = (record[1], record[2], record[0])
            else:
                data_insert_query = "INSERT INTO " + name + " (date, " + name + ", goal) VALUES (?, ?, ?)"
                data_input_tuple = record

        c = conn.cursor()

        c.execute(data_insert_query, data_input_tuple)

        conn.commit()
        conn.close()

    def remove_from_database(self, record, name):
        conn = sqlite3.connect('user.db')
        data_input_tuple = (str(record[0]),)

        if len(record) > 3:
            data_delete_query = "DELETE FROM " + name + " WHERE date = ? and name = ?"
            data_input_tuple += (str(record[1]),)
        else:
            data_delete_query = "DELETE FROM " + name + " WHERE date = ?"

        c = conn.cursor()

        c.execute(data_delete_query, data_input_tuple)

        conn.commit()
        conn.close()

    def data_to_tracking_series(self):
        data = self.get_series_data()
        max_days = self.calculate_days_in_month(self.today[4:6], self.today[:4])
        clean = [max_days]
        if len(data) == 0:
            return clean

        index = 0
        for series in data:
            if len(series) > 0:
                x = []
                y = []
                for i in range(len(series[0]) - 1):
                    y.append([])
                for point in series:
                    x.append(self.day_in_date(index, point[0]))
                    for i in range(len(point) - 1):
                        y[i].append(point[i + 1])

                cleaned = [x, y]
                clean.append(cleaned)
            else:
                clean.append([])
            index += 1

        return clean

    def day_in_date(self, num, data_date):
        date1 = date(int(data_date[:4]), int(data_date[4:6]), int(data_date[6:8]))
        if num == 0:
            return date1.weekday() + 1
        if num == 1:
            date2 = date(int(data_date[:4]), int(data_date[4:6]), 1)
            dif = (date1 - date2).days + 1
            return dif
        if num == 2:
            date2 = date(int(data_date[:4]), 1, 1)
            dif = (date1 - date2).days + 1
            return dif
        return 1

    def calculate_days_in_month(self, month, year):
        days = 1
        if month == '12':
            days = (date(int(year) + 1, 1, 1) - date(int(year), int(month), 1)).days
        else:
            days = (date(int(year), int(month) + 1, 1) - date(int(year), int(month), 1)).days
        return days

    def data_to_widget_series(self):
        return self.get_series_data()

    def get_tracking_graph_data(self):
        return self.tracking_graph_data

    def get_widget_graph_data(self):
        return self.widget_graph_data

    def get_series(self, mode):
        if mode == "widget_graph":
            return self.data[:9]
        elif mode == "normal":
            return 0
