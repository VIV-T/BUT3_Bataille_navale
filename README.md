# Bataille Navale
 
## Présentation
Ce projet s'inscrit dans un contexte universitaire (3ème année de BUT). Il s'agit de la continuité du code développé en deuxième année. L'idée ici fut de reprenre le code réalisé l'année précédente afin de l'améliorer et d'ajouter de nouvelles fonctionnalités.

## Arborescense
Contrairement à précédemment, il y a ici une arborescence plus complexe.
Dans le dossier "Scripts" se trouvent tous les modules Python utiles à l'execution du code.
Les tests sont regroupés dans le dossiers éponyme : "Tests".
Il faut noter quelques particularités :
 - le fichier main.py ne se situe pas dans le fichier "Scripts", mais au même niveau que ce dernier pour des raison de praticité quand à l'utilisation de pyinstaller pour créer un main.exe
 - main.exe est situé dans le dossier "dist", créé automatiquement par pyinstaller tout comme main.spec et le dossier "build"
 - Dans le dossier Backups se trouvent toutes les sauvegardes du jeu (stratégies et modes de jeu).

Le code est encore une fois divisé en plusieurs classes. Bien que de nouvelles classes pour le jeu ai été ajoutées, le véritable changement concerne la multiplication de classes de test. Afin d'améliorer le projet précédent, j'ai modifié l'organisation des tests et j'ai créer une classe de tests propre à chaque classe du jeu. Le fichier "Test.py" appel quant à lui toutes les autres classe de tests afin de pouvoir executer tous les tests avec un seul scripts.


### Remarques
Executer la cmd : pyinstaller --onefile --icon=ship.ico Scripts\\main.py
Elle permet de creer une application ".exe" à partir d'un fichier python (main.py ici).
