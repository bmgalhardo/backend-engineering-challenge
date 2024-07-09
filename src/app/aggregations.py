import datetime
import logging
import json
import os.path

from typing import TextIO
from pydantic import ValidationError
from collections import deque

from .exceptions import BadLine
from .models import AggregatedOutput, TranslationDelivered


class Aggregation:

    def __init__(self, input_file: str, output_file: str, window: int) -> None:
        self.line = self.line_queue(input_file)
        self.output = self.create_file(output_file)
        self.window = window
        self.deque = deque()

    def __del__(self):
        self.output.close()

    def line_queue(self, file_path: str) -> (datetime.datetime, int):
        for line in open(file_path, "r"):
            try:
                yield self.validated_line(line)
            except BadLine:
                continue

    @staticmethod
    def create_file(file_path: str) -> TextIO:
        folder = os.path.dirname(file_path)
        if folder and not os.path.exists(folder):
            os.mkdir(folder)
        return open(file_path, "w")

    @staticmethod
    def validated_line(line: str) -> (datetime.datetime, int):
        try:
            parsed_line = json.loads(line)
            validated_line = TranslationDelivered(**parsed_line)
            return validated_line.timestamp, validated_line.duration
        except json.JSONDecodeError:
            logging.warning(f"Malformed JSON: {line}")
            raise BadLine
        except ValidationError:
            logging.warning(f"Line not in the expected schema: {line}")
            raise BadLine

    def compute(self) -> None:
        # initialize values
        file_has_lines = True
        time, value = next(self.line)
        current_time = time.replace(second=0, microsecond=0)

        # from the requirements, the first displayed date will always have avg=0 since the points in that minute window
        #   will only matter for the next minute aggregation;
        self.process_window_value(current_time, 0)

        while file_has_lines:  # each iteration increases 1 minute

            # remove values outside current rolling window
            # note the timestamp are first aggregated in the next minute, and since we are zeroing the seconds,
            #   we need to add 1 minute to current_time and then subtract the window
            #   current_time + 1 minute - W minutes = current_time - (W - 1)
            while self.deque and self.deque[0][0] <= current_time - datetime.timedelta(minutes=self.window - 1):
                self.deque.popleft()

            # add values within current minute
            while time < current_time + datetime.timedelta(minutes=1):
                self.deque.append((time, value))
                try:
                    time, value = next(self.line)
                except StopIteration:
                    file_has_lines = False
                    break

            # Calculate the average delivery time for the values within the window
            avg = self.calculate_window_average()

            # since the interval is closed on the right we need to increase before processing
            current_time += datetime.timedelta(minutes=1)
            self.process_window_value(current_time, avg)

    def calculate_window_average(self) -> float:
        if self.deque:
            return sum(v for _, v in self.deque) / len(self.deque)
        else:
            return 0

    def process_window_value(self, timestamp: datetime, value: float) -> None:
        output = self.validated_output(timestamp, value)
        self.save_result(output)

    @staticmethod
    def validated_output(timestamp: datetime, value: float) -> AggregatedOutput:
        output = AggregatedOutput(date=timestamp, average_delivery_time=value)
        return output

    def save_result(self, output: AggregatedOutput) -> None:
        output_str = f'{output.model_dump_json().replace("T", " ").replace(".0", "")}\n'
        logging.debug(output_str)
        self.output.write(output_str)
