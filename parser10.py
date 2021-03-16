"""
    parser1.0
    analyseur de texte d'article scientifique
    Syntaxe :
        parser10.py [arg]
        [arg] : fichier pdf, -help
    return :
        *.txt
"""
import os
import sys

from parser_help import help
from parser_functions import *

       
if not sys.argv.__len__()!=1:
    print("Syntaxe : \n parser10.py  [arg] \n [arg] : repertoire , -help")

elif sys.argv[1]=="-help":
    help()

else :
    if os.path.exists(sys.argv[1])==False:
        print("le chemin spécifié ne correspond pas à un repertoire")
    else:
        conversions(sys.argv[1])
