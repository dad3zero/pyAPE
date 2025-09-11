
from contacts_parser import conf
from contacts_parser.parsers import file_parser as parser
from contacts_parser.models import static_model as models
from contacts_parser.writers import contacts_writer as writer

def run() -> None:
    """
    Exécution du parsing du fichier et écriture des fichiers cibles.
    """
    for kid, first_parent, second_parent in parser.parse_csv(conf.src_file_path):

        family = models.Family(kid, first_parent, second_parent)

        if any(parent.has_mail for parent in family.parents):
            contact_writer = writer.FileWriter(family.school_class)
            contact_writer.add_informations(family)

