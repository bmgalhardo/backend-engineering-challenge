import unittest

from unittest.mock import patch

import pytest

from app.main import InputArguments


class TestInputs(unittest.TestCase):

    @patch("app.main.InputArguments.check_file_exists", return_value="some_file")
    @patch("sys.argv", ["python", "-i", "some_file", "-w", "10"])
    def test_correct_inputs(self, mock_file_exists):
        inputs = InputArguments()
        assert inputs.input_file == "some_file"
        assert inputs.window_size == 10
        assert inputs.output_file == "output"
        assert inputs.logger

    @patch("sys.argv", ["python", "-i", "some_file", "-w", "10"])
    def test_file_not_found(self):
        with pytest.raises(SystemExit):
            InputArguments()

    @patch("app.main.InputArguments.check_file_exists", return_value="some_file")
    @patch("sys.argv", ["python", "-i", "some_file", "-w", "-10"])
    def test_negative_window(self, mock_file_exists):
        with pytest.raises(SystemExit):
            InputArguments()

    @patch("app.main.InputArguments.check_file_exists", return_value="some_file")
    @patch("sys.argv", ["python", "-i", "some_file", "-w", "this_window"])
    def test_string_window(self, mock_file_exists):
        with pytest.raises(SystemExit):
            InputArguments()

    @patch("app.main.InputArguments.check_file_exists", return_value="some_file")
    @patch("sys.argv", ["python", "-i", "some_file", "-w", "1000000000000"])
    def test_large_window(self, mock_file_exists):
        with pytest.raises(SystemExit):
            InputArguments()

    @patch("sys.argv", ["python", "-w", "10"])
    def test_missing_file_input(self):
        with pytest.raises(SystemExit):
            InputArguments()

    @patch("app.main.InputArguments.check_file_exists", return_value="some_file")
    @patch("sys.argv", ["python", "-i", "some_file"])
    def test_missing_window_input(self, mock_file_exists):
        with pytest.raises(SystemExit):
            InputArguments()
