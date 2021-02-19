"""
    parser_functions
    definitions des fonctions pour le programme parser
"""
import os
import sys
from os import listdir
from os.path import isfile, join
from os.path import basename

def conversions(repertory):
    fichiers = [f for f in listdir(repertory) if isfile(join(repertory,f))]
    
    repTxt = "txt_"+repertory
    rep_texte = "texte_"+repertory
    
    if os.path.exists(rep_texte):
    	os.system("rm -rf "+rep_texte)
    
    if os.path.exists(repTxt):
    	os.system("rm -rf "+repTxt)
    
    os.makedirs(rep_texte)
    os.makedirs(repTxt)
    
    for i in fichiers:
        txtName=basename(i)
        toPdf="pdftotext -layout "+repertory+"/"+i+" "+rep_texte+"/"+txtName[:(len(txtName)-4)]+".txt"
        print(toPdf)
        os.system(toPdf)
        
        file = open(repTxt+"/"+txtName[:(len(txtName)-4)]+".txt","w+")
        file.write(find_filename(rep_texte)+"\n")
        file.write(find_title(rep_texte)+"\n")
        file.close()
        find_resume(rep_texte)
        
    os.system("rm -rf "+rep_texte)



def find_filename(rep_texte):
    fichiers = [f for f in listdir(rep_texte) if isfile(join(rep_texte,f))]
    for i in fichiers:
    	buf="Nom du fichier d'origine: "+i[:(len(i)-3)]+"pdf"
    	return buf



def find_title(rep_texte):
    fichiers = [f for f in listdir(rep_texte) if isfile(join(rep_texte,f))]
    for i in fichiers:
        fichier = open(rep_texte+"/"+i,"r")
        buf="Titre du papier: "
        line = fichier.readline()
        title=line.strip()
        titre=True
        while line=="\n" or len(title)<15 or len(title)>65:
            line=fichier.readline()
            title=line.strip()
        while line != "\n" and len(title)<65 and titre==True:
            buf=buf+" "+title
            line=fichier.readline()
            title=line.strip()
            for indice in title:
                if indice==".":
                    titre=False
        fichier.close()
        return buf



def find_resume(rep_texte):
    fichiers = [f for f in listdir(rep_texte) if isfile(join(rep_texte,f))]
    for i in fichiers:
        fichier = open(rep_texte+"/"+i,"r")
        
