import logging
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import TextIO

from contacts_parser import conf
from contacts_parser import processorng as processor


def validate_file_path(path: str | Path):
    path = Path(path)
    supported_suffixes = [".csv"]
    if not all((path.is_file(), path.suffix in supported_suffixes)):
        raise ValueError(f"Wrong file name: {path}")


def validate_separator(separator: str):
    supported_separators = [",", ";"]
    if separator not in supported_separators:
        raise ValueError(f"Not supported separator: {separator}")


def run_contacts_parser(file_path: TextIO, separator: str | None = None):
    """Parse a CSV file containing student/parent data and export Gmail-compatible contacts.

    Reads the input CSV file, validates parent email addresses, and generates
    one contact file per school class in the destination folder.

    :param file_path: Path to the source CSV file containing student/parent data.
    :param separator: CSV field separator ("," or ";"). Defaults to the value in conf.
    :raises ValueError: If the file does not exist, has an unsupported extension,
        or if the separator is not supported.
    """
    file_path = Path(file_path)

    if separator:
        validate_separator(separator)
        conf.CSV_SEPARATOR = separator

    validate_file_path(file_path)

    conf.setup_paths(file_path)

    logging.info("Extraction des contacts de %s", conf.src_file_path)
    logging.info("Écriture dans le répertoire %s", conf.destination_folder)
    logging.info("Séparateur pour le csv source : %s", conf.CSV_SEPARATOR)

    processor.run()


def describe_file_structure(file_path: TextIO, separator: str | None = None):
    from contacts_parser.parsers import descriptor
    descriptor.describe(file_path, separator)


def run_webapp():
    """Launch the Streamlit webapp."""
    import subprocess
    webapp_path = Path(__file__).parent / "webapp" / "home.py"
    subprocess.run([sys.executable, "-m", "streamlit", "run", str(webapp_path),
                    "--browser.gatherUsageStats", "false",
                    ])


def main():
    parser = ArgumentParser(
        prog="pyape",
        description="Outils pour les associations de parents d'élèves (APE)"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: contacts
    contacts_subparser = subparsers.add_parser(
        "contacts",
        help="Conversion de contacts vers un format CSV pour import dans les messageries (Google)"
    )
    contacts_subparser.add_argument("file_path", help="Chemin vers le fichier csv")
    contacts_subparser.add_argument(
        "-s", "--separator",
        choices=[",", ";"],
        help="Séparateur du fichier csv, virgule par défaut"
    )
    contacts_subparser.add_argument("-d", "--describe", action="store_true", help="Décrit la structure du fichier.")

    # Subcommand: webapp
    subparsers.add_parser(
        "webapp",
        help="Lancer l'interface web Streamlit"
    )

    args = parser.parse_args()

    if args.command == "contacts":
        if args.describe:
            describe_file_structure(args.file_path, args.separator)
        else:
            try:
                run_contacts_parser(args.file_path, args.separator)
            except ValueError as e:
                logging.error(str(e))
                sys.exit(1)
    elif args.command == "webapp":
        run_webapp()


if __name__ == "__main__":
    main()
