"""
    help for use parse
"""
def help():
    print("Syntaxe de la commande : \n  parser10.py  [arg] \n  [arg] :  [format],  repertoire , -help \n  [format] :  -t pour le format texte (format par défaut s'il n'est pas précisé), -x pour le format xml \n" +"Syntaxe du menu : \n  all : mot clé pour parser tous les fichiers\n  [nom],[nom], ... ,[nom] : liste des fichiers à parser (la virgule est le seul séparateur accepté)\n  [nom] : nom d'un fichier pdf\n"+ "Description : \n  parse est un outil d'aide à l'analyse de textes scientifiques.\n  Ce programme accepte en entrée un dossier contenant des fichiers au format PDF.\n  Le résultat obtenue est un sous-dossier contenant un fichier au format texte pour chaque fichier au format PDF.\n  Ces sorties texte portent le même nom que l'entrée PDF et contiennent le nom du fichier d'origine, le titre du papier et le résumé de l'auteur")
    
