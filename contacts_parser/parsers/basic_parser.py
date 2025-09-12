from typing import TextIO

import pandas as pd

from contacts_parser import conf
from contacts_parser.models.flow_models import Kid, Parent


def load_dataframe(file_path: TextIO, encoding:str = "utf-8", sep=";") -> pd.DataFrame:
    return pd.read_csv(file_path, encoding=encoding, sep=sep)


def parse(file:TextIO):
    """
    Parse les informations de famille à partir d'un fichier.

    La fonction a besoin d'un descripteur de la stricture du fichier csv dans le fichier de
    configuration.

    :param file: fichier contenant les informations des familles.
    :return:
    """

    csv_data_location = {item: index for index, item in enumerate(conf.CONTACT_PARSER_STRUCTURE)}

    header = file.readline().rstrip().split(conf.CSV_SEPARATOR)

    for line in file:
        elements = line.rstrip().split(conf.CSV_SEPARATOR)
        yield (Kid(elements[csv_data_location["kid_lastname"]], elements[csv_data_location["kid_firstname"]], elements[csv_data_location["school_class"]]),
               Parent(elements[csv_data_location["p1_lastname"]], elements[csv_data_location["p1_firstname"]], elements[csv_data_location["p1_mail"]], ""),
               Parent(elements[csv_data_location["p2_lastname"]], elements[csv_data_location["p2_firstname"]], elements[csv_data_location["p2_mail"]], ""))

