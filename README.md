# pyAPE

**pyAPE** est un ensemble d'outils en Python pour notre **Associations de Parents d'Élèves**. Le
projet contient :
 * Un script de conversion d'informations de contact
 * Un outil web pour avoir une vue sur les classes et retrouver les informations de contact  

Les outils sont adaptés à nos besoins et donc au format de fichier qui nous est communiqué par
l'établissement. Je souhaite évidemment qu'ils profitent au plus grand nombre aussi n'hésitez
pas à forker le projet pour l'adapter à vos besoins ou proposer une évolution.

## Besoins techniques
Les scripts proposés ici sont en Python. [Python](https://www.python.org/) doit donc être installé
sur votre poste.

Ce projet utilise des dépendances externes, pour les installer :
```shell
pip install -r requirements.txt
```

## Scripts proposés dans ce projet
### Gestion de contacts
Le projet est né du besoin de gérer le contact des parents d'élèves. Le project principal offre 
plusieurs fonctionalités à partir du même point d'entrée. L'aide globale peut être obtenue par :

```shell
python -m contact-parser -h
```

### Conversion de fiches contact
Une des activités les plus chronophages est la saisie des coordonnées des parents. Si l'établissement
fournit les données de manière électronique, un script sera évidemment plus efficace pour convertir
les informations afin de créer des fiches contact.

`contact_parser` permet de convertir les entrées d'un fichier CSV vers un fichier CSV de contacts à
importer dans gmail.

Pour l'utiliser, vous devez être dans le répertoire racine du projet et exécuter la commande :
```shell
python -m contact-parser contacts /chemin/vers/fichier.csv
```

Ceci créera un répertoire `dest` dans le répertoire contenant le csv (par exemple, 
`/chemin/vers/dest/` si on prend l'exemple ci-dessus). Un fichier csv de contacts sera créé par 
classe en reprendant le nom de la classe du fichier csv original.

Chaque fiche de contact contient le nom et prénom du parent ainsi que l'information "enfant".
Une note reprenant nom et prénom de l'enfant ainsi que la classe sont également ajoutés.

Ce script ne gère pas encore les doublons à savoir que s'il y a une fratrie dans l'établissement,
la fiche parent sera créée pour chaque enfant. GMail vous proposera de fusionner par la suite les
fiches.

Vous pouvez obtenir l'aide par
```shell
python -m contact-parser contacts -h
```

### Interface web
Le propose une interface web permettant d'explorer les données.

Vous pouvez le lancer avec :
```shell
python -m contact-parser webapp
```

## Dépendances
Le projet utilise les dépendances suivantes :
 * [pandas](https://pandas.pydata.org) : utilisé pour lire le fichier source et traiter les données.
 * [email-validator](https://pypi.org/project/email-validator/) : permet de valider les emails.
 * [Streamlit](https://streamlit.io) : propose une interface web pour explorer les données.