import logging
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import TextIO

from contacts_parser import conf
from contacts_parser import processor as processor


def validate_file_path(path: str | Path, allowed_base_dir: Path | None = None) -> Path:
    """Validate file path to prevent path traversal attacks.

    :param path: Path to the CSV file to validate.
    :param allowed_base_dir: Optional base directory to restrict access to.
    :return: Resolved absolute path.
    :raises ValueError: If path is invalid, doesn't exist, or is outside allowed directory.
    """
    path = Path(path).resolve()  # Resolve to absolute path, eliminating ../ etc.

    supported_suffixes = [".csv"]

    if not path.is_file():
        raise ValueError("Le fichier spécifié n'existe pas")

    if path.suffix.lower() not in supported_suffixes:
        raise ValueError("Le format de fichier n'est pas supporté (CSV requis)")

    # If an allowed base directory is specified, ensure the file is within it
    if allowed_base_dir is not None:
        allowed_base = Path(allowed_base_dir).resolve()
        try:
            path.relative_to(allowed_base)
        except ValueError:
            raise ValueError("Accès au fichier non autorisé")

    return path


def validate_separator(separator: str):
    supported_separators = [",", ";"]
    if separator not in supported_separators:
        raise ValueError(f"Not supported separator: {separator}")


def setup_configuration(file_path: TextIO, separator: str | None = None):
    """Validate and configure file path and separator.

    :param file_path: Path to the source CSV file.
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


def run_contacts_parser(file_path: TextIO, separator: str | None = None):
    """Parse a CSV file containing student/parent data and export Gmail-compatible contacts.

    Reads the input CSV file, validates parent email addresses, and generates
    one contact file per school class in the destination folder.

    :param file_path: Path to the source CSV file containing student/parent data.
    :param separator: CSV field separator ("," or ";"). Defaults to the value in conf.
    :raises ValueError: If the file does not exist, has an unsupported extension,
        or if the separator is not supported.
    """
    setup_configuration(file_path, separator)

    logging.info("Extraction des contacts de %s", conf.src_file_path)
    logging.info("Écriture dans le répertoire %s", conf.destination_folder)
    logging.info("Séparateur pour le csv source : %s", conf.CSV_SEPARATOR)

    processor.run()


def describe_file_structure(file_path: TextIO, separator: str | None = None):
    from contacts_parser.parsers import descriptor
    descriptor.describe(file_path, separator)


def run_webapp(file_path: TextIO | None = None, separator: str | None = None):
    """Launch the Streamlit webapp."""
    import subprocess
    webapp_path = Path(__file__).parent / "webapp" / "home.py"

    cmd = [sys.executable, "-m", "streamlit", "run", str(webapp_path),
           "--browser.gatherUsageStats", "false"]

    if file_path:
        setup_configuration(file_path, separator)
        cmd.extend(["--", str(conf.src_file_path)])
        if separator:
            cmd.append(separator)

    subprocess.run(cmd)


def main():
    parser = ArgumentParser(
        prog="pyape",
        description="Outils pour les associations de parents d'élèves (APE)"
    )

    # Parent parser with shared arguments
    common_parser = ArgumentParser(add_help=False)
    common_parser.add_argument(
        "-s", "--separator",
        choices=[",", ";"],
        help="Séparateur du fichier csv, virgule par défaut"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: contacts
    contacts_subparser = subparsers.add_parser(
        "contacts",
        parents=[common_parser],
        help="Conversion de contacts vers un format CSV pour import dans les messageries (Google)"
    )
    contacts_subparser.add_argument("file_path", help="Chemin vers le fichier csv")
    contacts_subparser.add_argument("-d", "--describe", action="store_true", help="Décrit la structure du fichier.")

    # Subcommand: webapp
    webapp_subparser = subparsers.add_parser(
        "webapp",
        parents=[common_parser],
        help="Lancer l'interface web Streamlit"
    )
    webapp_subparser.add_argument(
        "-f", "--file_path",
        help="Chemin vers le fichier csv source"
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
        run_webapp(args.file_path, args.separator)


if __name__ == "__main__":
    main()
