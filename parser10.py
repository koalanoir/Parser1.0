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
import time

from parser_help import help
from parser_functions import *

#il manque un argument
if sys.argv.__len__()==1:
    print("Syntaxe : \n parser10.py  [arg] \n [arg] : repertoire , -help")

#argument help
elif sys.argv[1]=="-help":
    help()

#argument du format non précisé
elif sys.argv.__len__()==2:
    if os.path.exists(sys.argv[1])==False:
        print("le chemin spécifié ne correspond pas à un repertoire")
    else:
        conversions(sys.argv[1],"-t")

#argument du format précisé
elif sys.argv.__len__()==3:
    if os.path.exists(sys.argv[2])==False:
        print("le chemin spécifié ne correspond pas à un repertoire")
    else:
        conversions(sys.argv[2],sys.argv[1])
