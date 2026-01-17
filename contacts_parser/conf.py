"""
Fichier de configuration pour l'application.

Vous pouvez modifier ce fichier afin d'adapter les paramètres à votre cas en particulier le logger.
"""

from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler
import os

root_dir = Path(__file__).parent.parent
log_file = root_dir / "file.log"

# Create log file with restricted permissions (owner read/write only)
if not log_file.exists():
    log_file.touch(mode=0o600)
else:
    os.chmod(log_file, 0o600)

# Configuration du logger avec rotation
handler = RotatingFileHandler(
    log_file,
    maxBytes=1_000_000,  # 1 MB max
    backupCount=3,       # Keep 3 backup files
    encoding='utf-8'
)
handler.setFormatter(logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
))

logging.basicConfig(
    level=logging.INFO,
    handlers=[handler]
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

# Les lignes suivantes décrivent les colonnes à utiliser lors de l'extraction des éléments d'un
# parent. Ces lignes seront celles retenues par le script de transformation.

PARENT1_COLUMNS = ['NOM', 'PRENOM', 'DIV.', 'NOM LEGAL', 'PRENOM LEGAL', 'ADRESSE LEGAL', 'COURRIEL LEGAL']
PARENT2_COLUMNS = ['NOM', 'PRENOM', 'DIV.', 'NOM AUTRE LEGAL', 'PRENOM AUTRE LEGAL', 'ADRESSE AUTRE LEGAL', 'COURRIEL AUTRE LEGAL']

# Cette variable décrit les colonnes contenant un mail. Elle est utilisée pour filtrer les entrées
# sans contact. Elle doit contenir 2 noms, le premier sera utilisé pour le dernier filtre.

EMAIL_COLUMNS = ['COURRIEL LEGAL', 'COURRIEL AUTRE LEGAL']


CSV_SEPARATOR = ','
