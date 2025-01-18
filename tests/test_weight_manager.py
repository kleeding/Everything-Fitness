from everything_fitness.backend.weight_manager import WeightManager
from tests.test_data_manager import today, dates, data1, data2, data3 

weight_manager1 = WeightManager('', data1, today, dates)
weight_manager2 = WeightManager('', data2, today, dates)
weight_manager3 = WeightManager('', data3, today, dates)

def test_calculate_weight_change():
    result1 = weight_manager1.calculate_weight_change()
    result2 = weight_manager2.calculate_weight_change()
    result3 = weight_manager3.calculate_weight_change()

    expected1 = [-0.5, 1.5, -14.0, -14.0]
    expected2 = [0.0, 2.0, '-', '-']
    expected3 = [0.0, 0.0, '-', '-']

    assert result1 == expected1
    assert result2 == expected2
    assert result3 == expected3

def test_get_series_data():
    result1 = weight_manager1.get_series_data()
    result2 = weight_manager2.get_series_data()
    result3 = weight_manager3.get_series_data()

    expected1 = [[('20250116', 91.2, 85.0), ('20250115', 91.7, 85.0), ('20250114', 85.7, 85.0), ('20250113', 87.7, 85.0)],
                 [('20250116', 91.2, 85.0), ('20250115', 91.7, 85.0), ('20250114', 85.7, 85.0), ('20250113', 87.7, 85.0),
                  ('20250112', 89.7, 85.0), ('20250111', 91.7, 85.0), ('20250110', 92.7, 85.0), ('20250109', 95.7, 85.0),
                  ('20250108', 96.7, 85.0), ('20250107', 92.0, 85.0), ('20250106', 90.1, 85.0), ('20250105', 92.9, 85.0),
                  ('20250104', 94.1, 85.0), ('20250103', 96.4, 85.0), ('20250102', 98.2, 85.0), ('20250101', 100.0, 85.0)],
                 [('20250116', 91.2, 85.0), ('20250115', 91.7, 85.0), ('20250114', 85.7, 85.0), ('20250113', 87.7, 85.0),
                  ('20250112', 89.7, 85.0), ('20250111', 91.7, 85.0), ('20250110', 92.7, 85.0), ('20250109', 95.7, 85.0),
                  ('20250108', 96.7, 85.0), ('20250107', 92.0, 85.0), ('20250106', 90.1, 85.0), ('20250105', 92.9, 85.0),
                  ('20250104', 94.1, 85.0), ('20250103', 96.4, 85.0), ('20250102', 98.2, 85.0), ('20250101', 100.0, 85.0)]]
    
    expected2 = [[('20250115', 91.7, 85.0)],
                [('20250115', 91.7, 85.0), ('20250112', 89.7, 85.0), ('20250111', 91.7, 85.0), ('20250109', 95.7, 85.0),
                 ('20250107', 92.0, 85.0), ('20250106', 90.1, 85.0), ('20250104', 94.1, 85.0), ('20250102', 98.2, 85.0),
                 ('20250101', 100.0, 85.0)],
                [('20250115', 91.7, 85.0), ('20250112', 89.7, 85.0), ('20250111', 91.7, 85.0), ('20250109', 95.7, 85.0),
                 ('20250107', 92.0, 85.0), ('20250106', 90.1, 85.0), ('20250104', 94.1, 85.0), ('20250102', 98.2, 85.0),
                 ('20250101', 100.0, 85.0)]]
    
    expected3 = [[('20250115', 91.7, 85.0), ('20250114', 85.7, 85.0)],
                 [('20250115', 91.7, 85.0), ('20250114', 85.7, 85.0), ('20250111', 91.7, 85.0), ('20250110', 92.7, 85.0), 
                  ('20250108', 96.7, 85.0), ('20250107', 92.0, 85.0), ('20250105', 92.9, 85.0), ('20250103', 96.4, 85.0), 
                  ('20250102', 98.2, 85.0), ('20250101', 100.0, 85.0)],
                 [('20250115', 91.7, 85.0), ('20250114', 85.7, 85.0), ('20250111', 91.7, 85.0), ('20250110', 92.7, 85.0), 
                  ('20250108', 96.7, 85.0), ('20250107', 92.0, 85.0), ('20250105', 92.9, 85.0), ('20250103', 96.4, 85.0), 
                  ('20250102', 98.2, 85.0), ('20250101', 100.0, 85.0)]]

    assert result1 == expected1
    assert result2 == expected2
    assert result3 == expected3

def test_calculate_trends():
    weight_manager1.calculate_trends()
    result1 = weight_manager1.get_trends()
    weight_manager2.calculate_trends()
    result2 = weight_manager2.get_trends()
    weight_manager3.calculate_trends()
    result3 = weight_manager3.get_trends()

    expected1 = [-2.0, 1.0, -2.0]
    expected2 = [0, 1.0, 0]
    expected3 = [0, 0, 0]

    assert result1 == expected1
    assert result2 == expected2
    assert result3 == expected3
