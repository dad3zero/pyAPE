from typing import TextIO

import pandas as pd

def load_dataframe(file_path: TextIO, encoding:str = "utf-8", sep=";") -> pd.DataFrame:
    return pd.read_csv(file_path, encoding=encoding, sep=sep)

def extract_unusable_data(full_dataset: pd.DataFrame,
                          column_email_labels: tuple[str, str],
                          sorting_columns: tuple[str, str] | None = None,
                          ) -> pd.DataFrame:
    """
    Extrait et retourne les données sans emails pour les deux parents.

    :param full_dataset: Les données à filtrer.
    :param column_email_labels: Les noms de colonnes à prendre en compte (doit contenir 2 données).
    :param sorting_columns: Les colonnes selon lesquelles faire un tri si nécessaire.
    :return: Les données sans emails pour les deux parents qui peuvent contenir des lignes vides.
    """
    missing_mail_values = full_dataset[full_dataset[column_email_labels[0]].isna() & full_dataset[
        column_email_labels[1]].isna()]

    if sorting_columns is not None:
        return missing_mail_values.sort_values(list(sorting_columns))
    else:
        return missing_mail_values


def clean_dataset(full_dataset: pd.DataFrame,
                  column_email_labels: list[str],
                  ) -> None:
    """
    Supprime les lignes où toutes les colonnes spécifiées sont vides (NaN). Ces colonnes sont
    attendues comme étant les adresses email.

    :param full_dataset: Les données à filtrer.
    :param column_email_labels: Les noms de colonnes à prendre en compte.
    """
    full_dataset.dropna(subset=list(column_email_labels), how="all", inplace=True)

def build_dataset_of_parents(full_dataset: pd.DataFrame,
                             first_parent_labels: tuple[str],
                             second_parent_labels: tuple[str],
                             label_names: tuple[str, str] | None = None,
                             ) -> pd.DataFrame:
    """
    Réarrange les données pour n'avoir qu'un parent par ligne. Les labels des deux parents et de
    renommage doivent être *alignés* en termes de colonnes (même nombre, même information au même
    endroit).

    :param full_dataset: Les données à filtrer.
    :param first_parent_labels: Les données à extraire pour le premier parent
    :param second_parent_labels: Les données à extraire pour le second parent
    :param label_names: Les noms des colonnes à uniformiser. En absence, les noms des colonnes du
           premier parent seront utilisées.
    :return: Les données transformées.
    """

    if len(first_parent_labels) != len(second_parent_labels):
        raise ValueError(f"Parents description must have same length, got {len(first_parent_labels)} and {len(second_parent_labels)}.")

    if label_names is  not None and len(label_names) != len(first_parent_labels):
        raise ValueError(f"Parents new description must have same length as parents data, got {len(first_parent_labels)} and {len(label_names)}.")

    first_parent = full_dataset[list(first_parent_labels)].copy()
    second_parent = full_dataset[list(second_parent_labels)].copy()
    if label_names is not None:
        first_parent.columns = label_names
        second_parent.columns = label_names
    else:
        second_parent.columns = first_parent_labels

    return pd.concat([first_parent, second_parent], ignore_index=True)


def to_gmail_csv(full_dataset: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({
        'First Name': full_dataset['PRENOM LEGAL'],
        'Last Name': full_dataset['NOM LEGAL'],
        'Children': full_dataset['PRENOM'] + " " + full_dataset['NOM'],
        'E-mail Address': full_dataset['COURRIEL LEGAL'],
        'Notes': full_dataset.apply(
            lambda row: f"Parent de {row['PRENOM']} {row['NOM']}, classe {row['DIV.']}", axis=1)
    })
