"""
Fichier de configuration pour l'application.

Vous pouvez modifier ce fichier afin d'adapter les paramètres à votre cas en particulier le logger.
"""

from pathlib import Path

import logging

root_dir = Path(__file__).parent.parent

# Configuration de base du logger
logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s - %(message)s",
                    datefmt="%H:%M:%S",
                    filename= root_dir / "file.log",
                    )


def setup_paths(dest_path: Path):
    """
    Réalise la configuration des chemins vers le fichier source et la destination (répertoire /dest
    à la racine du fichier source).

    :param dest_path: Chemin vers le fichier source.
    """
    global src_file_path
    global destination_folder
    src_file_path = Path(dest_path).resolve()
    destination_folder = src_file_path.parent / "dest"
    if not destination_folder.exists():
        destination_folder.mkdir()


# Variable qui référence le fichier source, elle sera modifiée à l'exécution
src_file_path = None
# Répertoire d'écriture des fichiers de sortie. La variable sera modifiée à l'exécution,
# sa valeur sera "[src_file_path]/dest"
destination_folder = None

# La ligne suivante décrit la structure du fichier de données. Les différentes chaines sont
# utilisées dans le programme. Pour adapter le script à vos besoins ou à toute évolution de ce
# fichier, créez un n-uplet contenant autant d'éléments que de colonnes en utilisant les chaînes
# comme vu ci-dessous. Si le fichier contient des colonnes non-utilisées par ce script, utilisez une
# chaîne vide pour cette colonne.

#CONTACT_PARSER_STRUCTURE = ('kid_lastname', 'kid_firstname', 'birth_date', 'school_class', 'p1_civility', 'p1_lastname', 'p1_firstname', 'p1_relathionship', 'p1_mail', '', 'p2_civility', 'p2_lastname', 'p2_firstname', 'p2_relathionship', 'p2_mail')
#CONTACT_PARSER_STRUCTURE = ('school_class', 'kid_lastname', 'kid_firstname', 'p1_civility', 'p1_lastname', 'p1_firstname', '', '', '', 'p1_mail', 'p2_civility', 'p2_lastname', 'p2_firstname', '', '', '', 'p2_mail')
CONTACT_PARSER_STRUCTURE = ('kid_lastname', 'kid_firstname', 'school_class', 'p1_lastname', 'p1_firstname', '', 'p1_mail', 'p2_lastname', 'p2_firstname', '', 'p2_mail')


CSV_SEPARATOR = ';'
