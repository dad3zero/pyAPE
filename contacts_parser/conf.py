"""
Fichier de configuration pour l'application.

Vous pouvez modifier ce fichier afin d'adapter les paramètres à votre cas en particulier le logger.
"""

from pathlib import Path

import logging

# Configuration de base du logger
logging.basicConfig(level=logging.INFO)

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

root_dir = Path(__file__).parent.parent

# Variable qui référence le fichier source, elle sera modifiée à l'exécution
src_file_path = None
# Répertoire d'écriture des fichiers de sortie. La variable sera modifiée à l'exécution,
# sa valeur sera "[src_file_path]/dest"
destination_folder = None

EXPECTED_STRUCTURE = ('Civilite', 'Nom de famille Personne', "Nom d'usage Personne", 'Prénom Personne', 'Email personne', 'Communication adresse postale et courriel', 'Ligne 1 adresse', 'Ligne 2 adresse', 'Ligne 3 adresse', 'Ligne 4 adresse', 'Libelle postal', 'Code postal', 'Lc parente', 'Nom de famille', "Nom d'usage", 'Prénom', 'Code Structure')

CSV_SEPARATOR = ','
