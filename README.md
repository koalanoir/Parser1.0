# Parser1.0

Syntaxe de la commande :
  parser10.py [option] [arg]
  [option] : -t pour le format texte (format par défaut s'il n'est pas précisé), -x pour le format xml
  [arg] : repertoire , -help

Syntaxe du menu :
  all : mot clé pour parser tous les fichiers
  [nom],[nom], ... ,[nom] : liste des fichiers à parser (la virgule est le seul séparateur accepté)
  [nom] : nom d'un fichier pdf

Description :
  parse est un outil d'aide à l'analyse de textes scientifiques.
  Ce programme accepte en entrée un dossier contenant des fichiers au format PDF.
  Le résultat obtenue est un sous-dossier contenant un fichier au format texte pour chaque fichier au format PDF.
  Ces sorties texte portent le même nom que l'entrée PDF et contiennent le nom du fichier d'origine, le titre du papier, les noms et adresses des auteurs, le résumé de l'auteur et les références bibliographiques du document.

Système :
  Le programme fonctionne sous Linux, en ligne de commandes.
  Il est implémenté en Python3.
  Il fonctionne avec des appels systémes et le programme pdftotext -layout.
