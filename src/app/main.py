import os
import argparse
import datetime
import logging

from typing import Optional

from .aggregations import Aggregation


class InputArguments:

    def __init__(self, args: Optional[list[str]] = None):
        parser = self.create_parser()
        arguments = parser.parse_args(args)

        self.input_file = arguments.input_file
        self.output_file = arguments.output_file
        self.window_size = arguments.window_size
        self.logger = arguments.logger

    @staticmethod
    def check_file_exists(file: str) -> str:
        if os.path.isfile(file):
            return file
        else:
            raise argparse.ArgumentTypeError(f"File <{file}> does not exist")

    @staticmethod
    def check_window(value: int) -> int:
        try:
            i_value = int(value)
        except ValueError:
            raise argparse.ArgumentTypeError(f"Window value ({value}) must be integer")
        if i_value <= 0:
            raise argparse.ArgumentTypeError(f"Window value ({value}) must be positive")
        elif i_value > 10**6:
            raise argparse.ArgumentTypeError(f"Window value ({value}) must be lower than 1e6")
        return i_value

    def create_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser()
        parser.add_argument('-i', '--input_file', required=True,
                            type=lambda x: self.check_file_exists(x), help='Input file')
        parser.add_argument('-w', '--window_size', required=True,
                            type=lambda x: self.check_window(x),
                            help='In minutes, specify the size of the moving window used for the aggregation')
        parser.add_argument('-o', '--output_file', required=False, default="output",
                            help='Output file path')
        parser.add_argument('-l', '--logger', required=False, default=logging.INFO,
                            choices=["DEBUG", "INFO", "WARNING", "ERROR"],
                            help='the logging level')
        return parser


def main(args: Optional[list[str]] = None):
    start_time = datetime.datetime.now()

    arguments = InputArguments(args=args)

    logging.basicConfig(level=arguments.logger)
    logging.info(f"Input file: {arguments.input_file}")
    logging.info(f"Output file: {arguments.output_file}")
    logging.info(f"Window size: {arguments.window_size}")

    aggregation = Aggregation(input_file=arguments.input_file,
                              output_file=arguments.output_file,
                              window=arguments.window_size)
    aggregation.compute()

    logging.info(f"Runtime: {datetime.datetime.now() - start_time}\n")


if __name__ == "__main__":
    main()
