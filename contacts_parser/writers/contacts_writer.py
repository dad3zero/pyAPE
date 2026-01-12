import logging
from pathlib import Path

import pandas as pd

from contacts_parser import conf
import contacts_parser.models.static_model as model

def write(class_level: str, contacts_data: pd.DataFrame):
    destination_path = conf.destination_folder / Path(class_level).with_suffix(".csv")

    contacts_data.to_csv(destination_path, index=False)


class FileWriter:
    def __init__(self, class_level: str):

        self.level = class_level
        self.destination_path = conf.destination_folder / Path(class_level).with_suffix(".csv")
        #self.destination_path = conf.destination_folder / Path("2025").with_suffix(".csv")

        if not self.destination_path.exists():
            with open(self.destination_path, "wt") as level_file:
                level_file.write("Title;First Name;Last Name;Children;E-mail Address;Gender;Keywords;Notes;Spouse;Labels\n")

    def add_informations(self, family: model.Family):
        if family.school_class != self.level:
            raise ValueError(f"Wrong data for {self.level}")

        with open(self.destination_path, "at", encoding="utf-8") as level_file:
            for parent in family.parents:
                if parent.has_mail:
                    level_file.write(
                        f";{parent.firstname};{parent.lastname};{family.kid_name};{parent.mail};;;{parent.relationship} de {family.kid_name} classe {family.school_class};;{self.level} ::: * myContacts\n")
                else:
                    logging.info("Parent %s (%s) de %s avec mail %s", parent.name, parent.relationship, family.kid_name, parent.mail)
