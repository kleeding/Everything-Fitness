from everything_fitness.backend.data_manager import DataManager

today = '20250116'
dates = ['20250115', '20250112', '20241231', '20241231']

# normal - ascending order records
data1 = [('20241215', 105.2, 85.0),
         ('20250101', 100.0, 85.0),
         ('20250102', 98.2, 85.0),
         ('20250103', 96.4, 85.0),
         ('20250104', 94.1, 85.0),
         ('20250105', 92.9, 85.0),
         ('20250106', 90.1, 85.0),
         ('20250107', 92.0, 85.0),
         ('20250108', 96.7, 85.0),
         ('20250109', 95.7, 85.0),
         ('20250110', 92.7, 85.0),
         ('20250111', 91.7, 85.0),
         ('20250112', 89.7, 85.0),
         ('20250113', 87.7, 85.0),
         ('20250114', 85.7, 85.0),
         ('20250115', 91.7, 85.0),
         ('20250116', 91.2, 85.0)]

# missing entries - ascending order
data2 = [('20250101', 100.0, 85.0),
         ('20250102', 98.2, 85.0),
         ('20250104', 94.1, 85.0),
         ('20250106', 90.1, 85.0),
         ('20250107', 92.0, 85.0),
         ('20250109', 95.7, 85.0),
         ('20250111', 91.7, 85.0),
         ('20250112', 89.7, 85.0),
         ('20250115', 91.7, 85.0)]

# missing entries - mixed order 
data3 = [('20250107', 92.0, 85.0),
         ('20250101', 100.0, 85.0),
         ('20250102', 98.2, 85.0),
         ('20250110', 92.7, 85.0),
         ('20250103', 96.4, 85.0),
         ('20250105', 92.9, 85.0),
         ('20250115', 91.7, 85.0),
         ('20250108', 96.7, 85.0),
         ('20250114', 85.7, 85.0),
         ('20250111', 91.7, 85.0)]

# would be good to add tests for 'bad data' e.g., 
# - incorrect date format
# - wrong sized entries
# - empty entries, etc

data_manager1 = DataManager('', data1, today, dates)
data_manager2 = DataManager('', data2, today, dates)
data_manager3 = DataManager('', data3, today, dates)

def test_get_recent_record():
    result1 = data_manager1.get_recent_record()
    result2 = data_manager2.get_recent_record()
    result3 = data_manager3.get_recent_record()

    expected1 = [('20250116', 91.2, 85.0), True]
    expected2 = [('20250115', 91.7, 85.0), False]
    expected3 = [('20250115', 91.7, 85.0), False]

    assert result1 == expected1
    assert result2 == expected2
    assert result3 == expected3

def test_get_recent_records():
    result1 = data_manager1.get_recent_records()
    result2 = data_manager2.get_recent_records()
    result3 = data_manager3.get_recent_records()

    expected1 = [[('20250116', 91.2, 85.0)], True]
    expected2 = [[('20250115', 91.7, 85.0)], False]
    expected3 = [[('20250115', 91.7, 85.0)], False]

    assert result1 == expected1
    assert result2 == expected2
    assert result3 == expected3

def test_get_records():
    test_dates = ['20241230', '20250101', '20250102', '20250106', '20250112', '20250114', '20250201']

    expected1 = [[],
                 [('20250101', 100.0, 85.0)],
                 [('20250102', 98.2, 85.0)],
                 [('20250106', 90.1, 85.0)],
                 [('20250112', 89.7, 85.0)],
                 [('20250114', 85.7, 85.0)],
                 []]
    expected2 = [[],
                 [('20250101', 100.0, 85.0)],
                 [('20250102', 98.2, 85.0)],
                 [('20250106', 90.1, 85.0)],
                 [('20250112', 89.7, 85.0)],
                 [],
                 []]
    expected3 = [[],
                 [('20250101', 100.0, 85.0)],
                 [('20250102', 98.2, 85.0)],
                 [],
                 [],
                 [('20250114', 85.7, 85.0)],
                 []]
    
    for x in zip(test_dates, expected1, expected2, expected3):
        result1 = data_manager1.get_records(x[0])
        result2 = data_manager2.get_records(x[0])
        result3 = data_manager3.get_records(x[0])

        assert result1 == x[1]
        assert result2 == x[2]
        assert result3 == x[3]

def test_clean_record():
    records = [('123', '234', '345', '456'),
               ('12.3', '23.4', '34.5', '45.6'),
               ('-123', '-234', '-345', '-456'),
               ('-12.3', '-23.4', '-34.5', '-45.6'),
               ('-12.3', '23.4', '-34.5', '45.6')]

    expected = [('20250101', 123, 234, 345, 456),
                ('20250101', 12.3, 23.4, 34.5, 45.6),
                ('20250101', -123, -234, -345, -456),
                ('20250101', -12.3, -23.4, -34.5, -45.6),
                ('20250101', -12.3, 23.4, -34.5, 45.6)]

    for x in zip(records, expected):
        result = DataManager.clean_record('', '20250101', x[0])
        assert result == x[1]

def test_day_in_date():
    dates = ['20240203', '20240426', '20240817', '20241119', '20250108', '20250416']
    expected = [[6, 3, 34], [5, 26, 117], [6, 17, 230], [2, 19, 324], [3, 8, 8], [3, 16, 106]]

    for x in zip(dates, expected):
        result0 = DataManager.day_in_date('', 0, x[0])
        result1 = DataManager.day_in_date('', 1, x[0])
        result2 = DataManager.day_in_date('', 2, x[0])

        assert result0 == x[1][0]
        assert result1 == x[1][1]
        assert result2 == x[1][2]

def test_calculate_days_in_month():
    months = [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    expected = [31, 31, 30 , 31, 30, 31, 31, 30, 31, 30, 31]

    for x in zip(months, expected):
        result = DataManager.calculate_days_in_month('', x[0], 2025)
        assert result == x[1]

    years = [2020, 2024, 2025, 2100]
    expected2 = [29, 29, 28, 28]
    for x in zip(years, expected2):
        result = DataManager.calculate_days_in_month('', 2, x[0])
        assert result == x[1]

def test_get_series():
    result1 = data_manager1.get_series("widget_graph")
    expected1 = [('20250116', 91.2, 85.0),
                ('20250115', 91.7, 85.0),
                ('20250114', 85.7, 85.0),
                ('20250113', 87.7, 85.0),
                ('20250112', 89.7, 85.0),
                ('20250111', 91.7, 85.0),
                ('20250110', 92.7, 85.0),
                ('20250109', 95.7, 85.0),
                ('20250108', 96.7, 85.0)]

    result2 = data_manager2.get_series("widget_graph")
    expected2 = [('20250115', 91.7, 85.0),
                 ('20250112', 89.7, 85.0),
                 ('20250111', 91.7, 85.0),
                 ('20250109', 95.7, 85.0),
                 ('20250107', 92.0, 85.0),
                 ('20250106', 90.1, 85.0),
                 ('20250104', 94.1, 85.0),
                 ('20250102', 98.2, 85.0),
                 ('20250101', 100.0, 85.0)]

    result3 = data_manager3.get_series("widget_graph")
    expected3 = [('20250115', 91.7, 85.0),
                 ('20250114', 85.7, 85.0),
                 ('20250111', 91.7, 85.0),
                 ('20250110', 92.7, 85.0),
                 ('20250108', 96.7, 85.0),
                 ('20250107', 92.0, 85.0),
                 ('20250105', 92.9, 85.0),
                 ('20250103', 96.4, 85.0),
                 ('20250102', 98.2, 85.0)]

    assert result1 == expected1
    assert result2 == expected2
    assert result3 == expected3
    