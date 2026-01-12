from typing import TextIO

from contacts_parser.parsers import pandas_toolbox as parser

def describe(file_path: TextIO, separator: str | None = None) -> None:
    dataset = parser.load_dataframe(file_path, sep=separator)
    print(list(dataset.columns))