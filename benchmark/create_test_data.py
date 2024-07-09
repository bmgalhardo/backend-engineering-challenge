import argparse
import datetime
import json
import os

from random import randint


def create_entry(date: datetime.datetime) -> dict:
    entry = {
        "timestamp": str(date.replace(microsecond=0)),
        "translation_id": "5aa5b2f39f7254a75aa5",
        "source_language": "en",
        "target_language": "fr",
        "client_name": "airliberty",
        "event_name": "translation_delivered",
        "nr_words": 30,
        "duration": randint(1, 1000)
    }
    return entry


def get_file_path(output_file: str) -> str:
    if output_file is None:
        filename = f"data_s{data_size}_d{days}"
    else:
        filename = cli_arguments.output

    data_path = os.path.join(os.path.dirname(__file__), "data")
    if not os.path.exists(data_path):
        os.mkdir(data_path)

    return os.path.join(data_path, filename)


def generate_random_timestamps(start_date: datetime.datetime,
                               end_date: datetime.datetime,
                               number_of_points: int):

    total_seconds = int((start_date - end_date).total_seconds())

    timestamps = []
    for _ in range(number_of_points):
        random_timestamp = start_date + datetime.timedelta(seconds=randint(0, total_seconds))
        timestamps.append(random_timestamp)

    timestamps.sort()

    return timestamps


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='unbabel aggregation challenge [benchmark]')
    parser.add_argument('-l', '--lines', required=True, help='the number of lines to generate', type=int)
    parser.add_argument('-d', '--days', required=True, help='the number of days in the file', type=int)
    parser.add_argument('-o', '--output', required=False, help='the name of the output file')

    cli_arguments = parser.parse_args()

    data_size = cli_arguments.lines
    days = cli_arguments.days
    file_path = get_file_path(cli_arguments.output)

    now = datetime.datetime.now()
    time = generate_random_timestamps(start_date=now,
                                      end_date=now-datetime.timedelta(days=days),
                                      number_of_points=data_size)

    f = open(file_path, "w")
    for t in time:
        f.write(json.dumps(create_entry(t)))
        f.write("\n")
    f.close()
