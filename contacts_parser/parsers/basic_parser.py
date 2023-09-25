from typing import TextIO

from contacts_parser import conf
from contacts_parser.models.flow_models import Kid, Parent

def parse(file:TextIO):
    header = file.readline().rstrip().split(conf.CSV_SEPARATOR)

    for line in file:
        kid_lastname, kid_firstname, birth_date, school_class, p1_civility, p1_lastname, p1_firstname, p1_relathionship, p1_mail, _, p2_civility, p2_lastname, p2_firstname, p2_relathionship, p2_mail, _ = line.rstrip().split(conf.CSV_SEPARATOR)
        yield (Kid(kid_lastname, kid_firstname, school_class),
               Parent(p1_lastname, p1_firstname, p1_civility, p1_mail, p1_relathionship),
               Parent(p2_lastname, p2_firstname, p2_civility, p2_mail, p2_relathionship))
