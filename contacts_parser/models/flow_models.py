"""
Ce module décrit les modèles sous forme de namedtuples utilisés dans les flux. Les fonctions
de parsing doivent retourner sous la forme suivante :

((nom enfant, prénom enfant, classe), (infos parent 1), (infos parent 2))

où les infos parent sont :

(nom parent, civilité, prénom parent, mail parent, relation).

`Relation` est l'information "père" ou "mère".

Ces structures sont décrites avec ces namedtuples

"""
from collections import namedtuple

Kid = namedtuple('Kid', ['last_name', 'first_name', 'school_class'])
Parent = namedtuple('Parent', ['last_name', 'first_name', 'email', 'relationship'])
