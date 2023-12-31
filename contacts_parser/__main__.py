import logging
import sys
from argparse import ArgumentParser
from pathlib import Path

from contacts_parser import conf
from contacts_parser import processor

# Création du parser et parsing des options.
parser = ArgumentParser(prog="contact_parser",
                        description="Conversion de contacts vers un format CSV pour import dans les messageries (Actuellement limité à GMail)")
parser.add_argument("file_path", help="Chemin vers le fichier csv")
parser.add_argument("-s", "--separator",
                    help="Séparateur du fichier csv, virgule par défaut dans le fichier de conf",
                    action="store")


def validate_file_path(path: Path):
    path = Path(path)
    supported_suffixes = [".csv"]
    if not all((path.is_file(), path.suffix in supported_suffixes)):
        raise ValueError(f"Wrong file name: {path}")


def validate_separator(separator : str):
    supported_separators = [",", ";"]
    if separator not in supported_separators:
        raise ValueError(f"Not supported separator: {separator}")


args = parser.parse_args()

file_path = Path(args.file_path)
if args.separator:
    try:
        validate_separator(args.separator)
        conf.CSV_SEPARATOR = args.separator
    except ValueError:
        logging.error("Séparateur de fichier non pris en charge (%s)", args.separator)

try:
    validate_file_path(file_path)
except ValueError:
    logging.error("Impossible d'utiliser le chemin %s (fichier innexistant ou sans extension .csv)", file_path)
    sys.exit(1)

conf.setup_paths(file_path)

logging.info("Extraction des contacts de %s", conf.src_file_path)
logging.info("Écriture dans le répertoire %s", conf.destination_folder)
logging.info("Séparateur pour le csv source : %s", conf.CSV_SEPARATOR)

processor.run()
