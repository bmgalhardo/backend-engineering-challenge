import os
import argparse
import datetime
import logging

from app.aggregations import Aggregation


class InputArguments:

    def __init__(self, args: list[str] = None):
        parser = self.create_parser()
        arguments = parser.parse_args(args)

        self.input_file = arguments.input_file
        self.output_file = arguments.output_file
        self.window_size = arguments.window_size
        self.time = arguments.time
        self.logger = arguments.logger

    @staticmethod
    def check_file_exists(parser: argparse.ArgumentParser, file: str) -> str:
        if os.path.isfile(file):
            return file
        else:
            raise parser.error(f"File <{file}> does not exist")

    def create_parser(self) -> argparse.ArgumentParser:
        parser = argparse.ArgumentParser()
        parser.add_argument('-i', '--input_file', required=True,
                            type=lambda x: self.check_file_exists(parser, x), help='Input file')
        parser.add_argument('-w', '--window_size', required=True, type=int,
                            help='In minutes, specify the size of the moving window used for the aggregation')
        parser.add_argument('-o', '--output_file', required=False, default="output",
                            help='Output file path')
        parser.add_argument('-t', '--time', required=False, action='store_true',
                            help='display code running time')
        parser.add_argument('-l', '--logger', required=False, default=logging.INFO,
                            choices=[a for a in logging._nameToLevel],
                            help='the logging level')
        return parser


def main(args: list[str] = None):
    start_time = datetime.datetime.now()

    arguments = InputArguments(args=args)

    logging.basicConfig(level=arguments.logger)

    aggregation = Aggregation(input_file=arguments.input_file,
                              output_file=arguments.output_file,
                              window=arguments.window_size)
    aggregation.compute()

    if arguments.time:
        print(f"{arguments.input_file}: {datetime.datetime.now() - start_time}")


if __name__ == "__main__":
    main()
