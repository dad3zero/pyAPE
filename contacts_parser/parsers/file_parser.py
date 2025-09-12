from pathlib import Path

from contacts_parser.parsers import basic_parser

def parse_csv(file_path: Path):
    """
    Retourne les données extraites à partir d'un fichier.

    Le parser utilisé doit retourner les informations au format :
     * pour l'enfant : [nom, prénom, classe]
     * pour chaque parent : [nom, prénom, mail, relation, "civilité"]

    Les données doivent être des itérables (listes ou n-uplets). La relation et la civilité sont
    optionnels.

    :param file_path:
    :return:
    """
    with open(file_path, encoding="utf-8") as child_data_file:
        yield from basic_parser.parse(child_data_file)
