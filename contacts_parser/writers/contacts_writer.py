import csv
import logging
from pathlib import Path

import pandas as pd

from contacts_parser import conf


def sanitize_csv_value(value) -> str:
    """Sanitize value to prevent CSV injection attacks.

    Prefixes dangerous characters with a single quote to prevent
    spreadsheet applications from interpreting them as formulas.
    """
    if pd.isna(value):
        return ""

    value_str = str(value)

    # Characters that could start a formula in spreadsheets
    if value_str and value_str[0] in ('=', '+', '-', '@', '|', '%'):
        return "'" + value_str

    return value_str


def write(base_file_name: str, contacts_data: pd.DataFrame, sanitize_csv: bool = False):
    destination_path = conf.destination_folder / Path(base_file_name).with_suffix(".csv")

    if sanitize_csv:
        contacts_data.to_csv(destination_path, index=False)
    else:
        # Sanitize all string columns to prevent CSV injection
        sanitized_data = contacts_data.copy()
        for col in sanitized_data.columns:
            if sanitized_data[col].dtype == 'object':
                sanitized_data[col] = sanitized_data[col].apply(sanitize_csv_value)

        sanitized_data.to_csv(destination_path, index=False, quoting=csv.QUOTE_NONNUMERIC)

