import logging
from pathlib import Path

import pandas as pd

from contacts_parser import conf


def write(base_file_name: str, contacts_data: pd.DataFrame):
    destination_path = conf.destination_folder / Path(base_file_name).with_suffix(".csv")

    contacts_data.to_csv(destination_path, index=False)

