"""
    parser_functions
    definitions des fonctions pour le programme parser
"""
import os
import sys
import shutil
import string
from os import listdir
from os.path import isfile,join
from os.path import basename

#variable globale pour sauvegarder la position entre les fonctions
position=0

"""
    La fonction conversion prend le chemin d'un repertoire et convertit a l'aide de la commande pdftotext -layout
    tous les fichiers PDF contenus dans ce repertoire en fichier texte
    elle fait appel a la fonction createDescription
"""
def conversions(repertory):
    fichiers=[f for f in listdir(repertory) if isfile(join(repertory,f))]
    
    repTxt="txt_"+repertory
    
    if os.path.exists(repTxt):
    	os.system("rm -rf "+repTxt)
    	
    #creation du repertoire
    os.makedirs(repTxt)
    
    #conversion du fichier pdf
    for i in fichiers:
        txtName=basename(i)
        if ".pdf" in txtName:
            txt=txtName[:(len(txtName)-4)]+".txt"
            toPdf="pdftotext -layout "+repertory+"/"+i+" "+repTxt+"/"+txt
            print(toPdf)
            os.system(toPdf)
            createDescription(repTxt+"/"+txt,repTxt)
        else:
            print(txtName+" n'est pas un fichier pdf")


"""
    La fonction createDescription prend en parametre le chemin d'un fichier texte et le nom du repertoire contenant ce fichier
    elle ecrit la description du document dans celui-ci en faisant appel aux fonctions find_filename, find_title, find_author et find_abstract
"""
def createDescription(file,repTxt):
    doc=open(basename(file),"w+")
    fichier=open(file,"r")
    doc.write("\n"+"*************** Summarize ***************"+"\n"+"\n")
    doc.write(find_filename(file)+"\n"+"\n")
    doc.write(find_title(fichier)+"\n"+"\n")
    doc.write(find_author(fichier)+"\n"+"\n")
    doc.write(find_abstract(fichier)+"\n")
    doc.write("\n"+"\n"+"\n")
    doc.write("---------------Create with PDF_Document_Analyser---------------"+"\n")
    doc.write("\n")
    doc.write("@Copyright all right reserved UBS")
    doc.close()
    if os.path.exists(file):
    	os.remove(file)
    shutil.move(basename(file),repTxt)
    fichier.close()
    
    
"""
    La fonction find_filename prend en parametre le nom du fichier texte non ouvert
    et renvoie le nom du fichier source(PDF)
"""
def find_filename(file):
    buf ="Nom du fichier d'origine : "+basename(file)[:(len(basename(file))-3)]+"pdf"
    return buf


"""
    La fonction find_title prend en parametre le fichier texte ouvert
    et renvoie le titre du document
"""
def find_title(file_txt):
    global position
    buf="Titre du document : "
    line = file_txt.readline()
    title=line.strip()
    titre=True
    
    #taille du titre entre 15 et 65 caracteres
    #pas de ligne de séparation dans le titre
   
    while line=="\n" or len(title)<15 or len(title)>65:
        line=file_txt.readline()
        title=line.strip()
    while line!="\n" and len(title)<65 and titre==True:
        buf=buf+" "+title
        position=file_txt.tell()
        line=file_txt.readline()
        title=line.strip()
        for indice in title:
            if indice==".":
                titre=False
    return buf

"""
    La fonction find_author prend en parametre le fichier texte ouvert
    et renvoie le(s) auteur(s) de ce document
"""
def find_author(file_txt):
    global position
    file_txt.seek(position,0)
    buf=""
    line=file_txt.readline()
    author=line.strip()
    auteur=True
    while line=="\n":
        line=file_txt.readline()
        author=line.strip()
    
    #premiere ligne du/des auteur(s)
    while line!="\n":
        while auteur==True:
            #elimine les caracteres qui ne font pas partie du nom
            temp=author
            nb=string.digits
            if "1st" in temp or "2nd" in temp:
                temp=temp.replace("1st","")
                temp=temp.replace("2nd","")
            temp=temp.replace(". ",".")
            for i in temp:
                if i in nb or i=="∗" or i=="\\" or i=="[" or i=="]" or i == ",":
                    temp=temp.replace(i,"")
                temp=temp.replace("  "," ")
            if " rd " in temp:
                temp=temp.replace("rd","")
            buf=buf+" "+temp
            auteur=False
            line=file_txt.readline()
            author=line.strip()
            for indice in author:
                if indice=="-" or indice==".":
                    auteur=True
                if indice=="," or indice in nb:
                    auteur=False
        line=file_txt.readline()
        position=file_txt.tell()
    while line=="\n":
        line=file_txt.readline()
        author=line.strip()
    auteur=True
    
    while line!="\n" and auteur==True and len(author)>60 and len(author)<65:
            for indice in author:
                if indice=="," or indice in nb:
                    auteur=False
            position=file_txt.tell()
            temp=author
            for i in temp:
                temp=temp.replace("  "," ")
            buf=buf+" "+temp
            line=file_txt.readline()
            author=line.strip()
            
    aut = "Auteur(s) du document : "
    count = 0
    buf = buf.strip()
    buf = buf.replace("  "," ")
    buf = buf.replace("Le ","Le-")
    buf = buf.replace("da ","da-")
    buf = buf.replace(" and "," ")
    for indice in range(len(buf)):
        aut = aut + buf[indice]
        if buf[indice] == " ":
            count = count + 1
        if count == 2:
            aut = aut + ","
            count = 0
    return aut

"""
    La fonction find_abstract prend en parametre le nom du fichier texte ouvert
    et renvoie le abstract du document
"""
def find_abstract(file_txt):
    global position
    file_txt.seek(position,0)
    buf="Abstract de l'auteur : "
    line=file_txt.readline()
    abstract = line.strip()
    abstrait = True
    maj = list(string.ascii_uppercase)
    minu = list(string.ascii_lowercase)
    esp="                                                         "
    
    #premiere ligne de abstract
    while line == "\n" or ("ABSTRACT" not in abstract.upper()) or (abstract[0] not in maj):
        line = file_txt.readline()
        abstract = line.strip()
        for indice in abstract:
            if indice in maj:
                abstrait=False
        if line != "\n" and abstrait == False and esp not in line:
            break
    if (abstract.upper() == "ABSTRACT") or ("ABSTRACT    " in abstract.upper()):
    	line = file_txt.readline()
    	abstract = line.strip()
    while line == "\n" or abstract[0] not in maj or (esp in line and esp not in abstract):
        line = file_txt.readline()
        abstract = line.strip()
    #elimine le mot Abstract
    abstract = abstract.replace("Abstract.","")
    abstract = abstract.replace("Abstract—","")
    abstract = abstract.replace("Abstract","")
    tiret=False
    for indice in range (len(abstract)):
        if abstract[indice-1]=="-" and abstract[indice]==" ":
                tiret=True
                buf=buf[:-1]
        if abstract[indice] == " " and abstract[indice+1] ==" ":
    	    if tiret==False:
    	        buf=buf+" "
    	    break
        else:
    	    buf=buf+abstract[indice] #ecrit caractere par caractere
    if (buf[len(buf)-1] in minu or buf[len(buf)-1]=="," or buf[len(buf)-1]=="?") and tiret==False:
        buf=buf+" "
    if buf[len(buf)-1]=="-":
        buf=buf[:-1]
     
    #lignes suivantes de abstract
    line=file_txt.readline()
    abstract=line.strip()
    point=False
    while (line!="\n" and not (esp in line and esp not in abstract)) or point==False:
        tiret=False
        for indice in range (len(abstract)):
            if abstract[indice-1]=="-" and abstract[indice]==" ":
                tiret=True
                buf=buf[:-1]
            if (abstract[indice] == " " and abstract[indice+1] ==" ") or (esp in line and esp not in abstract):
    	        if "               " not in abstract and tiret==False:
    	            buf=buf+" "
    	        break
            else:
    	        buf=buf+abstract[indice]
        #ajoute un espace entre le dernier mot d'une ligne et celui de la ligne suivante
        if (buf[len(buf)-1] in minu or buf[len(buf)-1]=="," or buf[len(buf)-1]=="?") and tiret==False:
            buf=buf+" "
        if buf[len(buf)-1]=="-":
            buf=buf[:-1]
        if buf[len(buf)-1]==".":
            point=True
        line=file_txt.readline()
        abstract=line.strip()
        
    return buf
    
