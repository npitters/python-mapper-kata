import argparse
from os.path import abspath, dirname
import json
from transformer import transform


def _load_json_file(file_name):
    with open(file_name, "r", encoding="utf-8") as read_file:
        return json.load(read_file)


if __name__ in ("__main__", "app.main"):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--file", default="", type=str, help="The json file to map"
    )
    PARSED_ARGS = parser.parse_args()

    raw_data = _load_json_file(PARSED_ARGS.file)

    transformed_data = transform(raw_data)

    print(f"Source Input:\n{raw_data}\n\nTarget Output:\n{transformed_data}\n\n")
