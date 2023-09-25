from pathlib import Path

from contacts_parser.parsers import basic_parser

def parse_csv(file_path: Path):
    with open(file_path, encoding="utf-8") as child_data_file:
        yield from basic_parser.parse(child_data_file)
