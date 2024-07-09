import unittest

from unittest.mock import patch, mock_open
from collections import deque

from app.aggregations import Aggregation
from app.main import main


class TestExampleWindowAggregation(unittest.TestCase):
    mock_file = (
        '{"timestamp": "2018-12-26 18:11:08.509654", "translation_id": "5aa5b2f39f7254a75aa5","source_language": "en", "target_language": "fr", "client_name": "airliberty","event_name": "translation_delivered", "nr_words": 30, "duration": 20}\n'
        '{"timestamp": "2018-12-26 18:15:19.903159", "translation_id": "5aa5b2f39f7254a75aa4","source_language": "en", "target_language": "fr", "client_name": "airliberty","event_name": "translation_delivered", "nr_words": 30, "duration": 31}\n'
        '{"timestamp": "2018-12-26 18:23:19.903159", "translation_id": "5aa5b2f39f7254a75bb3","source_language": "en", "target_language": "fr", "client_name": "taxi-eats","event_name": "translation_delivered", "nr_words": 100, "duration": 54}'
    )

    mock_file_wrong_schema = (
        '{"timestamp": "2018-12-26 18:11:08.509654", "translation_id": "5aa5b2f39f7254a75aa5","source_language": "en", "target_language": "fr", "client_name": "airliberty","event_name": "translation_delivered", "nr_words": 30, "duration": 20}\n'
        '{"timestamp": "", "translation_id": "5aa5b2f39f7254a75aa4","source_language": "en", "target_language": "fr", "client_name": "airliberty","event_name": "translation_delivered", "nr_words": 30, "duration": 31}\n'
        '{"timestamp": "2018-12-26 18:23:19.903159", "translation_id": "5aa5b2f39f7254a75bb3","source_language": "en", "target_language": "fr", "client_name": "taxi-eats","event_name": "translation_delivered", "nr_words": 100, "duration": 54}'
    )

    mock_file_wrong_json = (
        '{"timestamp": "2018-12-26 18:11:08.509654", "translation_id": "5aa5b2f39f7254a75aa5","source_language": "en", "target_language": "fr", "client_name": "airliberty","event_name": "translation_delivered", "nr_words": 30, "duration": 20}\n'
        '{"timestamp": "", "translatio "fr", "client_name": "airliberty","event_name": "translation_delivered", "nr_words": 30, "duration": 31}\n'
        '{"timestamp": "2018-12-26 18:23:19.903159", "translation_id": "5aa5b2f39f7254a75bb3","source_language": "en", "target_language": "fr", "client_name": "taxi-eats","event_name": "translation_delivered", "nr_words": 100, "duration": 54}'
    )

    correct_output = [
        '{"date":"2018-12-26 18:11:00","average_delivery_time":0}\n',
        '{"date":"2018-12-26 18:12:00","average_delivery_time":20}\n',
        '{"date":"2018-12-26 18:13:00","average_delivery_time":20}\n',
        '{"date":"2018-12-26 18:14:00","average_delivery_time":20}\n',
        '{"date":"2018-12-26 18:15:00","average_delivery_time":20}\n',
        '{"date":"2018-12-26 18:16:00","average_delivery_time":25.5}\n',
        '{"date":"2018-12-26 18:17:00","average_delivery_time":25.5}\n',
        '{"date":"2018-12-26 18:18:00","average_delivery_time":25.5}\n',
        '{"date":"2018-12-26 18:19:00","average_delivery_time":25.5}\n',
        '{"date":"2018-12-26 18:20:00","average_delivery_time":25.5}\n',
        '{"date":"2018-12-26 18:21:00","average_delivery_time":25.5}\n',
        '{"date":"2018-12-26 18:22:00","average_delivery_time":31}\n',
        '{"date":"2018-12-26 18:23:00","average_delivery_time":31}\n',
        '{"date":"2018-12-26 18:24:00","average_delivery_time":42.5}\n'
    ]

    wrong_output = [
        '{"date":"2018-12-26 18:11:00","average_delivery_time":0}\n',
        '{"date":"2018-12-26 18:12:00","average_delivery_time":20}\n',
        '{"date":"2018-12-26 18:13:00","average_delivery_time":20}\n',
        '{"date":"2018-12-26 18:14:00","average_delivery_time":20}\n',
        '{"date":"2018-12-26 18:15:00","average_delivery_time":20}\n',
        '{"date":"2018-12-26 18:16:00","average_delivery_time":20}\n',
        '{"date":"2018-12-26 18:17:00","average_delivery_time":20}\n',
        '{"date":"2018-12-26 18:18:00","average_delivery_time":20}\n',
        '{"date":"2018-12-26 18:19:00","average_delivery_time":20}\n',
        '{"date":"2018-12-26 18:20:00","average_delivery_time":20}\n',
        '{"date":"2018-12-26 18:21:00","average_delivery_time":20}\n',
        '{"date":"2018-12-26 18:22:00","average_delivery_time":0}\n',
        '{"date":"2018-12-26 18:23:00","average_delivery_time":0}\n',
        '{"date":"2018-12-26 18:24:00","average_delivery_time":54}\n'
    ]

    @patch("builtins.open", new_callable=mock_open, read_data=mock_file)
    def test_example(self, mock_file):
        aggregation = Aggregation(input_file="some_valid_file", output_file="some_valid_file",  window=10)
        aggregation.compute()
        for line in self.correct_output:
            mock_file().write.assert_any_call(line)

    @patch("builtins.open", new_callable=mock_open, read_data=mock_file_wrong_schema)
    def test_example_wrong_schema(self, mock_file):
        aggregation = Aggregation(input_file="some_valid_file", output_file="some_valid_file", window=10)
        aggregation.compute()
        for line in self.wrong_output:
            mock_file().write.assert_any_call(line)

    @patch("builtins.open", new_callable=mock_open, read_data=mock_file_wrong_json)
    def test_example_wrong_json(self, mock_file):
        aggregation = Aggregation(input_file="some_valid_file", output_file="some_valid_file", window=10)
        aggregation.compute()
        for line in self.wrong_output:
            mock_file().write.assert_any_call(line)

    @patch("builtins.open", new_callable=mock_open, read_data=mock_file)
    @patch("app.main.InputArguments.check_file_exists", return_value="some_file")
    @patch("app.aggregations.Aggregation.create_file")
    def test_main(self, mock_file, mock_exists, mock_create):

        main([
            "-i", "some_file",
            "-w", "10"
        ])
        for line in self.correct_output:
            mock_file().write.assert_any_call(line)

    @patch("app.aggregations.Aggregation.create_file")
    def test_average_window(self, mock_create):
        aggregation = Aggregation(input_file="some_valid_file", output_file="some_valid_file", window=10)
        aggregation.deque = deque([("t1", 3), ("t2", 1)])
        assert aggregation.calculate_window_average() == 2
        aggregation.deque.popleft()
        aggregation.deque.popleft()
        assert aggregation.calculate_window_average() == 0
