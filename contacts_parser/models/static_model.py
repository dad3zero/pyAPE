"""
Ce mocule décrit des classes permettant de gérer une notion de _famille_ sous forme d'objets
plus facile à gérer. La classe Parent permet également de valider les informations indispensables.
"""

import logging
from email_validator import validate_email, EmailNotValidError

class EmptyParentError(ValueError):
    """
    Exception pour l'absence de parent
    """


class Parent:
    def __init__(self, lastname, firstname, civility, mail, relationship):
        """
        Permet la création d'un parent mais nécessite la présence des informations nom et prénom.

        L'adresse email est validée lors de l'initialisation. Si elle est invalide, le champs sera
        à None.

        :param lastname: Le nom de famille
        :param firstname: Le prénom
        :param civility: Civilité récupérée du fichier, normalement M./Mme
        :param mail: L'adresse mail qui sera validée lors de l'instanciation. Si invalide, sera None
        :param relationship: Relation avec l'enfant, qualificatif récupéré du fichier
        :raises EmptyParentError: si les champs nom et prénom sont vides.
        """

        if not (lastname and firstname):
            raise EmptyParentError(f"Empty data : {civility} {lastname} {firstname} {mail} {relationship}")

        self.lastname = lastname
        self.firstname = firstname
        self.title = civility
        self.relationship = relationship.capitalize()
        self.spouse = ""

        try:
            email_info = validate_email(mail, check_deliverability=False)
            self.mail = email_info.normalized
        except EmailNotValidError:
            logging.error("Email non valide %s pour %s %s", mail, firstname, lastname)
            self.mail = None


    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return ((self.lastname, self.firstname, self.mail)
                == (other.lastname, other.firstname, other.mail))


    @property
    def name(self):
        return f"{self.lastname} {self.firstname}"

    @property
    def has_mail(self):
        return self.mail not in ("0", '')


class Family:
    def __init__(self, kid, parent_1=None, parent_2=None):
        """
        Représente la notion de famille pour la gestion de contacts.

        En cas d'absence d'informations de parents, des logs seront réalisés.

        :param kid: Est attendu le namedtuple kid
        :param parent_1: Est attendu le namedtuple Parent
        :param parent_2: Est attendu le namedtuple Parent
        """
        self.kid_lastname = kid[0]
        self.kid_firstname = kid[1]
        self.school_class = kid[2]

        self.parents = []

        empty_data = 0
        for parent in (parent_1, parent_2):
            try:
                self.parents.append(Parent(*parent))
            except EmptyParentError as exc:
                logging.warning("%s, %s, %s", self.kid_lastname, self.kid_firstname, exc)
                empty_data += 1

        if empty_data == 2:
            logging.warning(" ! no parent for %s, %s", self.kid_lastname, self.kid_firstname)

    @property
    def kid_name(self):
        return f"{self.kid_lastname} {self.kid_firstname}"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        return ((self.kid_firstname, self.kid_lastname, self.school_class)
                == (other.kid_firstname, other.kid_lastname, other.school_class))

    def __str__(self):
        return f"Famille de {self.kid_name} avec {len(self.parents)} parent(s)"
