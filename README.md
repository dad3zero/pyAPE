# pyAPE

Des outils Open Source en Python pour les Associations de Parents d'Élèves.

Les outils proposés ici sont réalisés pour répondre avant tout au besoin de notre association. Je
souhaite évidemment qu'ils profitent au plus grand nombre aussi n'hésitez pas à forker le projet
pour l'adapter à vos besoins ou proposer une évolution.

## Besoins techniques
Les scripts proposés ici sont en Python. [Python](https://www.python.org/) doit donc être installé
sur votre poste.

## Scripts proposés dans ce projet
### Conversion de fiches contact
Une des activités les plus chonophages est la saisie des coordonnées des parents. Si l'établissement
fournit les données de manière électronique, un script sera évidemment plus efficace pour convertir
les informations afin de créer des fiches contact.

`contact_parser` permet de convertir les entrées d'un fichier CSV vers un fichier CSV de contacts à
importer dans gmail.

Pour l'utiliser, vous devez être dans le répertoire racine du projet et exécuter la commande :
```shell
python -m contact-parser /chemin/vers/fichier.csv
```

Ceci créera un répertoire `dest` dans le répertoire contenant le csv, celui-ci contiendra les fichiers par classe.

Vous pouvez aussi obtenir l'aide par
```shell
python -m contact-parser -h
```
