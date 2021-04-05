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

maj=list(string.ascii_uppercase) #liste de toutes les majuscules
minu=list(string.ascii_lowercase) #liste de toutes les minuscules
nb=string.digits #liste des chiffres

"""
    La fonction conversion prend le chemin d'un repertoire et convertit a l'aide de la commande pdftotext -layout
    tous les fichiers PDF contenus dans ce repertoire en fichier texte
    elle fait appel a la fonction createDescription
"""
def conversions(repertory,param):
    fichiers=[f for f in listdir(repertory) if isfile(join(repertory,f))]
    
    print("Liste des fichiers contenus dans le répertoire : ")
    name=""
    parseList=[]
    name_error=""
    for i in fichiers:
        print(basename(i))
        name=name+basename(i)+","
    name=name[0:-1]
    parseList=parseList+name.split(",")
    name=input("Veuillez indiquer quel(s) fichier(s) analyser en écrivant le(s) nom(s), utilisez une virgule comme séparateur entre chaque nom (indiquez all pour analyser tous les fichiers) :" + "\n")
    name=name.replace(" ","")
    if name=="":
        print("Aucun fichier analysé. Veuillez entrer un nom de fichier à parser")
    if name!="all":
        parseList=[]+name.split(",")
    
    if param=="-t":
        repTxt="txt_"+repertory
        
        #verification d'existence du repertoire txt
        if os.path.exists(repTxt):
    	    os.system("rm -rf "+repTxt)
        
        #creation du repertoire txt
        os.makedirs(repTxt)
        
        #conversion du fichier pdf avec la commande pdftotext -layout
        for i in parseList:
            txtName=basename(i)
            if txtName not in fichiers:
                name_error=name_error+txtName
                if ".pdf" not in txtName:
                    name_error=name_error+" n'est pas un fichier pdf\n"
                else:
                    name_error=name_error+" n'a pu etre analysé. Veuillez verifier l'orthographe du fichier indiqué\n"
                continue
            if ".pdf" in txtName:
                txt=txtName[:(len(txtName)-4)]+".txt"
                toPdf="pdftotext -layout "+repertory+"/"+i+" "+repTxt+"/"+txt
                print(toPdf)
                os.system(toPdf)
                createDescription(repTxt+"/"+txt,repTxt,"-t")
        if name_error!="":
            print(name_error[0:-1])
    
    elif param=="-x":
        repXml="xml_"+repertory
    
        #verification d'existence du repertoire xml
        if os.path.exists(repXml):
    	    os.system("rm -rf "+repXml)
    
        #creation du repertoire xml
        os.makedirs(repXml)
        
        #conversion du fichier pdf avec la commande pdftotext -layout
        for i in parseList:
            xmlName=basename(i)
            if xmlName not in fichiers:
                name_error=name_error+xmlName
                if ".pdf" not in xmlName:
                    name_error=name_error+" n'est pas un fichier pdf\n"
                else:
                    name_error=name_error+" n'a pu etre analysé. Veuillez verifier l'orthographe du fichier indiqué\n"
                continue
            if ".pdf" in xmlName:
                xml=xmlName[:(len(xmlName)-4)]+".xml"
                toPdf="pdftotext -layout "+repertory+"/"+i+" "+repXml+"/"+xml
                print(toPdf)
                os.system(toPdf)
                createDescription(repXml+"/"+xml,repXml,"-x")
        if name_error!="":
            print(name_error[0:-1])


"""
    La fonction createDescription prend en parametre le chemin d'un fichier texte et le nom du repertoire contenant ce fichier
    elle ecrit la description du document dans celui-ci en faisant appel aux fonctions find_filename, find_title, find_author et find_abstract
"""
def createDescription(file,repTxtXml,param):
    doc=open(basename(file),"w+") #ouverture du document texte ou xml pour l'ecriture dedans
    fichier=open(file,"r") #ouverture du fichier pour la lecture
    
    #ecriture dans le fichier
    if param=="-t":
        doc.write("*************** Summarize ***************"+"\n"+"\n")
        doc.write("Nom du fichier d'origine : "+find_filename(file)+"\n"+"\n")
        doc.write("Titre du document : "+find_title(fichier)+"\n"+"\n")
        doc.write("Auteur(s) du document : \n"+create_author(fichier,param)+"\n"+"\n")
        doc.write("Abstract de l'auteur : "+find_abstract(fichier)+"\n"+"\n")
        doc.write("Introduction du document : "+find_introduction(fichier)+"\n"+"\n")
        doc.write("Corps du document: "+find_corps(fichier)+"\n"+"\n")
        doc.write("Conclusion du document : "+find_conclusion(fichier)+"\n"+"\n")
        doc.write("Discussion du document : "+find_discussion(fichier)+"\n"+"\n")
        doc.write("Références bibliographiques du document : "+find_references(fichier)+"\n")
        doc.write("\n"+"\n"+"\n"+"---------------Create with PDF_Document_Analyser---------------"+"\n"+"\n")
        doc.write("@Copyright all right reserved UBS")
    
    elif param=="-x":
        doc.write("<article>"+"\n"+"\n")
        doc.write("\t"+"<preamble>"+find_filename(file)+"</preamble>"+"\n"+"\n")
        doc.write("\t"+"<titre>"+find_title(fichier)+"</titre>"+"\n"+"\n")
        doc.write("\t"+"<auteurs>\n"+create_author(fichier,param)+"\t</auteurs>"+"\n"+"\n")
        doc.write("\t"+"<abstract>"+find_abstract(fichier)+"</abstract>"+"\n"+"\n")
        doc.write("\t"+"<introduction>"+find_introduction(fichier)+"</introduction>"+"\n"+"\n")
        doc.write("\t"+"<corps>"+find_corps(fichier)+"</corps>"+"\n"+"\n")
        doc.write("\t"+"<conclusion>"+find_conclusion(fichier)+"</conclusion>"+"\n"+"\n")
        doc.write("\t"+"<discussion>"+find_discussion(fichier)+"</discussion>"+"\n"+"\n")
        doc.write("\t"+"<biblio>"+find_references(fichier)+"</biblio>"+"\n"+"\n")
        doc.write("</article>")
    
    doc.close() #fermeture du document
    if os.path.exists(file):
    	os.remove(file)
    shutil.move(basename(file),repTxtXml)
    fichier.close() #fermeture du fichier


"""
    La fonction find_filename prend en parametre le nom du fichier texte non ouvert
    et renvoie le nom du fichier source(PDF)
"""
def find_filename(file):
    buf = basename(file)[:(len(basename(file))-3)]+"pdf" #nom du fichier texte ou xml où l'on remplace l'extension par pdf
    return buf


"""
    La fonction find_title prend en parametre le fichier texte ouvert
    et renvoie le titre du document
"""
def find_title(file_txt):
    global position
    buf=""
    line = file_txt.readline() #lecture de la ligne suivante
    title=line.strip()
    titre=True
    
    #pas de ligne de séparation dans le titre
    while line=="\n" or len(title)<15 or len(title)>65:
        line=file_txt.readline()
        title=line.strip()
    while line!="\n" and len(title)<65 and titre:
        buf=buf+" "+title
        position=file_txt.tell() #on memorise la position
        line=file_txt.readline()
        title=line.strip()
        for indice in title:
            if indice==".": #condition d'arret: un point sur la ligne
                titre=False
        if buf[0]==" ":
            buf=buf[1:len(buf)]
                
    #suppression de certains espaces dans le titre
    if "and" in buf and "with" not in buf:
        buf=buf.replace("and","And")
        for i in buf:
            for j in buf:
                if i in maj and j in minu:
                    buf=buf.replace(i+" "+j,i+j)
                if i in minu and j in minu:
                    buf=buf.replace(i+" "+j,i+j)
    
    buf=buf
    return buf


"""
    La fonction find_email prend en parametre le fichier texte ouvert
    et renvoie les adresses éléctroniques du/des auteur(s) du document
"""
def find_email(file_txt):
    global position
    file_txt.seek(position,0) #recupere la derniere position enregistree
    buf=""
    temp=""
    line=file_txt.readline() #lecture de la ligne suivante
    email=line.strip()
    no_stop=False
    arrobase=False
    accolade=False
    col="§"
    #reperage de l'adresse mail avec le symbole "@"
    while line!="\n":
        if ".edu" in email and "      " not in email and "{" not in email:
            email=email.replace("Q","@")
            buf=buf+"{"
            for j in email:
                if j=="@":
                    buf=buf+"}"
                buf=buf+j
            email=buf
            buf=""
        if "@" in email:
            email=email+" "
            col="§"
            #si "@" en debut de ligne: adresse sur deux lignes
            if email[0]=="@":
                buf=buf+mail #ligne precedente
            for i in range(len(email)):
                if email[i]=="{":
                    accolade=True
                if email[i]=="}":
                    accolade=False
                if email[i]=="@":
                    arrobase=True
                if email[i]==" " and not accolade:
                    if arrobase:
                        buf=buf+col+temp
                        arrobase=False
                    temp=""
                if email[i]==" " and email[i-1]==" " and email[i-2]!=" ":
                    col=col+"§"
                temp=temp+email[i]
            #si "-" ou "." en fin de ligne: adresse sur deux lignes
            if email[len(email)-2]=="-" or email[len(email)-2]==".":
                no_stop=True
        #sauvegarde de la ligne precedente
        mail=email
        line=file_txt.readline()
        email=line.strip()
        #seconde ligne de l'adresse
        if no_stop:
            for i in email:
                if i==" ":
                    temp=""
                temp=temp+i
            buf=buf+temp
        no_stop=False
    buf=buf.replace(". ",".")
    buf=buf.replace("- ","-")
    buf=buf.replace(" mx"," ")
    
    temp=""
    bufer=""
    copie=False
    if "(" in buf or "{" in buf:
        for j in buf:
            if j=="@":
                copie=True
            if copie:
                bufer=bufer+j
        buf=buf.replace("(","").replace(")","").replace("{","").replace("}","").replace(" ","")
        for i in buf:
            if i==",":
                temp=temp+bufer
            temp=temp+i
        continu=False
    else:
        continu=True
        temp=""
        bufer=""
        copie=False
    while continu:
        continu=False
        bufer=""
        for indice in range(len(buf)):
            if buf[indice]=="§" and buf[indice-1]!="§" and buf[indice+1]!="§":
                copie=True
            if buf[indice]=="§" and buf[indice+1]=="§":
                copie=False
            if copie:
                temp=temp+buf[indice]
            if not copie:
                bufer=bufer+buf[indice]
                if buf[indice]!="§":
                    continu=True
        bufer=bufer.replace("§§","§")
        buf=bufer
    temp=temp.replace("§","").strip()
    
    for indice in range(len(temp)):
        if temp[indice]==" " and temp[indice-1]!=",":
            temp=temp.replace(" ",",")
    
    return temp


"""
    La fonction find_affiliation prend en parametre le fichier texte ouvert
    et renvoie les affiliations et adresses des affiliations du/des auteur(s) du document
"""
def find_affiliation(file_txt):
    global position
    file_txt.seek(position,0) #recupere la derniere position enregistree
    buf=""
    line=file_txt.readline() #lecture de la ligne suivante
    affil=line.strip()
    cache=""
    parent=False
    pos=0
    while line!="\n" and "ABSTRACT" not in line.upper():
        if "@" in line and "      " in affil:
            for i in range(len(affil)):
                if affil[i]==" " and affil[i-1]==" ":
                    pos=i
                if affil[i]=="@":
                    affil=affil[0:pos]
                    break
            pos=0
        if "@" not in affil and ("[" not in affil or "]" not in affil) and ".edu" not in affil and ".fr" not in affil:
            buf=buf+"$"
            for indice in range(len(affil)):
                if affil[indice]=="(":
                    parent=True
                if affil[indice]==")":
                    parent=False
                    buf=buf+cache
                    cache=""
                if parent and affil[indice]==".":
                    cache=""
                    break
                if parent:
                    cache=cache+affil[indice]
                else:
                    buf=buf+affil[indice]
            if " mx" in buf:
                buf=buf[0:-2]
        line=file_txt.readline()
        affil=line.strip()
    
    #pour la lecture des colonnes
    copie=False
    not_copie=False
    continu=True
    bufer=""
    temp=""
    if "      " not in buf:
        temp=buf
    while "      " in buf and continu:
        bufer=""
        for i in range(len(buf)):
            if buf[i-1]=="$" and buf[i-2]!="[":
                copie=True
                not_copie=False
            if (buf[i]==" " and buf[i-1]==" ") or (buf[i]=="U" and buf[i-1]==" " and buf[i-2]=="d"):
                copie=False
            if copie:
                temp=temp+buf[i]
            if not copie and buf[i]!=" ":
                not_copie=True
            if not_copie:
                bufer=bufer+buf[i]
        temp=temp+"¤"
        for j in range(len(bufer)):
            if bufer[j]!="$":
                continu=True
                break
            else:
                continu=False
        buf=bufer
    buf=""
    for j in range(len(bufer)):
        if bufer[j]!="$":
            temp=temp+bufer
            bufer=""
            break
    if temp!="":
        temp="¤"+temp.replace("$"," ").strip()
        temp=temp.replace("N e w Y o r k","New York").replace("N Y","NY").replace("U S A","USA")
        
    return temp


"""
    La fonction find_author prend en parametre le fichier texte ouvert
    et renvoie le(s) auteur(s) du document
"""
def find_author(file_txt):
    global position
    file_txt.seek(position,0) #recupere la position apres lecture du titre
    buf=""
    line=file_txt.readline() #lecture de la ligne suivante
    author=line.strip()
    auteur=True
    while line=="\n": #on elimine les lignes vides entre le titre et le/les auteur(s)
        line=file_txt.readline()
        author=line.strip()
    
    #premiere ligne du/des auteur(s)
    while line!="\n": #on va jusqu'a la prochaine ligne vide pour se positionner au bon endroit pour la lecture de abstract
        while auteur:
            if "1st" in author or "2nd" in author or "rd " in author: #on elimine les nombres cardinaux
                author=author.replace("1st","").replace("2nd","").replace("rd","")
            author=author.replace(". ",".")
            author=author.replace(" and "," & ")
            for i in author:
                if i in nb or i=="∗" or i=="\\" or i=="[" or i=="]" or i == ",":
                    author=author.replace(i,"")
                author=author.replace("  "," ") #on remplace le double espace par un simple espace
            buf=buf+" "+author
            
            position=file_txt.tell()
            email=find_email(file_txt) #appel de la fonction pour recuperer les adresses mails que l'on stocke dans une variable
            affiliation=find_affiliation(file_txt)
            file_txt.seek(position,0)
            
            auteur=False
            line=file_txt.readline()
            author=line.strip()
            for indice in author:
                if indice=="-" or indice==".": #condition de continuation: un tiret ou un point dans la ligne
                    auteur=True
                if indice=="," or indice in nb: #condition d'arret: une virgule ou un chiffre
                    auteur=False
        line=file_txt.readline()
        position=file_txt.tell() #on memorise la position
        
    while line=="\n": #on se positionne sur la prochaine ligne non vide
        line=file_txt.readline()
        author=line.strip()
    
    pos=position
    position=file_txt.tell()
    mail=find_email(file_txt) #appel de la fonction pour recuperer les adresses mails dans la seconde section d'auteurs que l'on stocke dans une variable
    if mail!="":
        file_txt.seek(position,0)
    else:
        position=pos
    
    #seconde ligne du/des auteurs
    auteur=True
    pos=False
    while line!="\n" and auteur and len(author)>60 and len(author)<65:
        for indice in author:
            if indice=="," or indice in nb: #condition d'arret: une virgule ou un chiffre
                auteur=False
        position=file_txt.tell() #on memorise la position
        pos=True
        for i in author:
            author=author.replace("  "," ") #on remplace le double espace par un simple espace
        buf=buf+" "+author
        line=file_txt.readline()
        author=line.strip()
    if pos:
        affil=find_affiliation(file_txt)
        file_txt.seek(position,0)
    
    #ajout des virgules comme séparateur entre les noms
    temp = ""
    count = 0
    buf = buf.strip()
    buf=buf.replace("Torres Moreno","Torres-Moreno")
    for indice in range(len(buf)):
        if buf[indice]==" " and not ((buf[indice]==" " and buf[indice-1]=="e" and buf[indice-2]== "L") or (buf[indice]==" " and buf[indice-1]=="a" and buf[indice-2]== "d")):
            count = count + 1 #comptage des espaces
        if (buf[indice]==" " and buf[indice+1]=="&") or (buf[indice]==" " and buf[indice-1]=="&"):
            count=0
        if count == 2:
            temp = temp + ","
            count = 0
        temp = temp + buf[indice]
    
    #on ajoute les adresses mails à la suite du/des nom(s) d'auteur(s)
    temp=temp+"\n$"+email
    if mail!="":
        temp=temp+","+mail
    temp=temp+"\n£"+affiliation
    if pos:
        temp=temp+" "+affil
    temp=temp.replace("  "," ")
    temp=temp.replace(", ,",",")
    
    return temp


"""
    La fonction find_abstract prend en parametre le nom du fichier texte ouvert
    et renvoie le abstract du document
"""
def find_abstract(file_txt):
    global position
    global position2
    file_txt.seek(position,0) #recupere la position apres lecture du/des auteur(s)
    buf=""
    line=file_txt.readline() #lecture de la ligne suivante
    abstract = line.strip()
    abstrait = False
    esp="                                                         " #espace dans la ligne
    
    #premiere ligne de abstract
    while line == "\n" or ("ABSTRACT" not in abstract.upper()) or (abstract[0] not in maj): #condition pour débuter abstract: une ligne non vide et le mot Abstract ou une majuscule
        position2 = file_txt.tell()
        line = file_txt.readline()
        abstract = line.strip()
        for indice in abstract:
            if indice in maj:
                abstrait=True
        if line != "\n" and abstrait and esp not in line:
            break
    if (abstract.upper() == "ABSTRACT") or ("ABSTRACT    " in abstract.upper()): #on saute la ligne qui ne contient que le mot Abstract
        position2 = file_txt.tell()
        line = file_txt.readline()
        abstract = line.strip()
    while line == "\n" or abstract[0] not in maj or (esp in line and esp not in abstract): #condition pour débuter le paragraphe abstract: une ligne non vide et une colonne non vide et une majuscule
        position2 = file_txt.tell()
        line = file_txt.readline()
        abstract = line.strip()
    abstract = abstract.replace("Abstract.","")
    abstract = abstract.replace("Abstract—","")
    abstract = abstract.replace("Abstract","")
    tiret=False
    for indice in range (len(abstract)):
        if abstract[indice-1]=="-" and abstract[indice]==" ":
                tiret=True
        if abstract[indice] == " " and abstract[indice+1] ==" ": #condition d'arret quand deux colonnes: deux espaces à suivre
    	    break
        buf=buf+abstract[indice]
    #ajout d'un espace entre le dernier mot d'une ligne et celui de la ligne suivante
    if (buf[len(buf)-1] in minu or buf[len(buf)-1]=="," or buf[len(buf)-1]=="?") and not tiret:
        buf=buf+" "
    #suppression du tiret en fin de ligne quand une seule colonne
    if buf[len(buf)-1]=="-" or tiret:
        buf=buf[:-1]
        
    #lignes suivantes de abstract
    line=file_txt.readline()
    abstract=line.strip()
    point=False
    while (line!="\n" and not (esp in line and esp not in abstract)) or not point: #condition d'arret: quand un point en fin de ligne ou colonne suivi d'une ligne ou colonne vide
        tiret=False
        if "Index Terms" in abstract or "Keywords" in abstract:
            break
        for indice in range (len(abstract)):
            if abstract[indice-1]=="-" and abstract[indice]==" ":
                tiret=True
                buf=buf[:-1]
            if (abstract[indice] == " " and abstract[indice+1] ==" ") or (esp in line and esp not in abstract): #condition d'arret quand deux colonnes: deux espaces à suivre ou colonne vide
    	        if "               " not in abstract and not tiret:
    	            buf=buf+" "
    	        break
            buf=buf+abstract[indice]
    	
        #ajout d'un espace entre le dernier mot d'une ligne et celui de la ligne suivante
        if (buf[len(buf)-1] in minu or buf[len(buf)-1]=="," or buf[len(buf)-1]=="?") and not tiret:
            buf=buf+" "
        #suppression du tiret en fin de ligne quand une seule colonne
        if buf[len(buf)-1]=="-":
            buf=buf[:-1]
        #verification du point pour la boucle
        if buf[len(buf)-1]==".":
            point=True
        if buf[0]==" ":
            buf=buf[1:len(buf)]
        
        line=file_txt.readline()
        abstract=line.strip()
        
    position=file_txt.tell() #on memorise la position
    
    buf=buf.replace("  "," ")
    buf=buf.replace(" .",".")
    buf=buf.replace("dis tributed","distributed")
    buf=buf.replace("multipledocument","multiple-document")
    buf=buf.replace("S MMR","SMMR")
    buf=buf.replace("F RESA","FRESA")
    buf=buf.replace("C OVERAGE","COVERAGE")
    buf=buf.replace("R ESPONSIVENESS","RESPONSIVENESS")
    buf=buf.replace("P YRAMIDS","PYRAMIDS")
    return buf


"""
    la fonction find_Introduction prend en parametre le nom du fichier texte ouvert
    et renvoie l'introduction du document
"""
def find_introduction(file_txt):
    global position2
    global position3
    buf = " "
    line = file_txt.readline()
    intro = line.strip()
    drap = True
    col = False
    pos2 = False
    while(line == "\n" or ("INTRODUCTION" not in intro.upper() and "I NTRODUCTION" not in intro.upper()) ):
        line = file_txt.readline()
        intro = line.strip()
        if("      " in intro):
            col = True
    while drap and line:
        while not pos2:
            # verification du point d'arret ou de passage a la deuxieme colonne
            if ("2 " in line[:4] and ".2" not in line[:4]) or "2. " in line[:4] or "II. " in intro[:4]:
                drap = False
                break
            elif line == "\n" or (col  and "         " in line and "        " not in intro) or ("                                           " in line and "      " not in intro):
                line = file_txt.readline()
                intro = line.strip()
                break
            elif(intro.isdigit() and len(intro) < 4) or intro[:20].strip().isdigit():
                file_txt.seek(position2,0)
                pos2 = True
                line = file_txt.readline()
                intro = line.strip()
                break      
            elif(intro.isdigit() and len(intro) < 4) or intro[:20].strip().isdigit() or "distribution [8]." in line:
                file_txt.seek(position2,0)
                pos2 = True
                line = file_txt.readline()
                intro = line.strip()
                break
            elif "" in line or "" in line or "I. " in line or "https:" in line or ("     " in intro and len(intro.replace(" ","")) < 3):
                line = file_txt.readline()
                intro = line.strip()
                break
               
            #lecture des lignes de la premier colonne      
            if "     " in intro:
                buf = buf + intro[:intro.find("     ")] + " "
            else:
                buf = buf + intro + " "
            buf = buf.replace("\n"," ")
            line = file_txt.readline()
            intro = line.strip() 
            
        while pos2:
            #verification d'arret
            if line == "\n":
                line = file_txt.readline()
                intro = line.strip()
                position2 = file_txt.tell()
                break
            elif (intro.isdigit() and len(intro) < 4) or intro[:20].strip().isdigit():
                pos2 = False
                position2 = file_txt.tell()
                line = file_txt.readline()
                intro = line.strip()
                break
            elif "     "in intro and ("2 " in intro[intro.find("     "):].strip()[:4] or "2. " in intro[intro.find("     "):].strip()[:4] or "II. " in intro[intro.find("     "):].strip()[:4]):
                drap = False
                break
                
            #lecture des lignes
            if "    " in intro:
                buf = buf + intro[intro.find("    "):].strip() + " "
                
            elif "                                           " in line and "      " not in intro:
                buf = buf + intro + " "
            line = file_txt.readline()
            intro = line.strip()
   
    if not pos2 and "2 The" in line:
        position2 = file_txt.tell()
        print
    buf = buf.replace("\n","")
    while buf.find("  ") > -1:
        buf = buf.replace("  "," ")
    
    return buf


"""
    La fonction find_corps prend en parametre le nom du fichier texte ouvert
    et renvoie le corps du document
"""
def find_corps(file_txt):
    global position
    global position2
    global position3
    if position2==8468:
        file_txt.seek(position2,0)
    else:
        file_txt.seek(position3,0)
    buf = ""
    line = file_txt.readline()
    corps = line.strip()
    pos2 = False
    drap = True
    col = False
    
    while (line == "\n" or (("2  " not in line[:5] or ".2  " in line[:5]) and "2. " not in line[:4] and "II." not in corps[:4]) and line) and position2!=8468:
        if "     "in corps and ("2  " in corps[corps.find("     "):].strip()[:5] or "2.  " in corps[corps.find("     "):].strip()[:5] or "II." in corps[corps.find("     "):].strip()[:4]):
            pos2 = True
            break
        if "      " in corps:
            col = True 
        line = file_txt.readline()
        corps = line.strip()
    saut=False
    while line and drap:
        while not pos2 and line:
            #condition de passage a la deuxieme ligne ou d'arrét ou de saut de ligne
            if ("D ISCUSSION" in corps.upper()[:corps.find("    ")] or "DISCUSSION" in corps.upper()[:corps.find("    ")] or "  DISCUSION" in corps.upper() or "Discussion" in corps) and "," not in corps and "-" not in corps and len(corps)<=40:
                drap = False
                break
            elif ("C ONCLUSION" in corps.upper()[:corps.find("    ")] or "CONCLUSION" in corps.upper()[:corps.find("    ")] or "  CONCLUSION" in corps.upper() or "Conclusion" in corps) and saut:
                drap = False
                position=file_txt.tell()-120
                break
            elif "R EFERENCES  " in corps.upper()[:corps.find("    ")+2] or "REFERENCES  " in corps.upper()[:corps.find("    ")+2] or "  REFERENCES" in corps.upper() or "References" in corps and len(corps)<=40:
                drap = False
                break
            elif "ACKNOWLEDGMENT" in corps.upper()[:corps.find("    ")] or "A CKNOWLEDGMENT" in corps.upper()[:corps.find("    ")]:
                drap = False
                break
            elif corps.isdigit() and len(corps) < 4 or "" in line:
                file_txt.seek(position2,0)
                pos2 = True
                line = file_txt.readline()
                corps = line.strip()
                break
                
            #lecture des lignes de corps
            if "    " in corps:
                buf = buf + corps[:corps.find("    ")] + " "
            elif "        " in line and "           " not in corps:
                line = file_txt.readline()
                corps = line.strip()
                break
            else:
                buf = buf + corps + " "
            
            if line=="\n" or ".          " in line:
                saut=True
            else:
                saut=False
            position=file_txt.tell()
            line = file_txt.readline()
            corps = line.strip()
            
        while pos2 and line:
            #condition de passage a la premiere ligne ou d'arret ou de saut de ligne
            if ("D ISCUSSION" in corps.upper()[:corps.find("    ")] or "DISCUSSION" in corps.upper()[:corps.find("    ")]) and "," not in corps and "-" not in corps and len(corps)<=50:
                drap = False
                break
            elif "C ONCLUSION" in corps.upper()[corps.find("    "):] or "CONCLUSION" in corps.upper()[corps.find("    "):] and len(corps)<=130:
                drap = False
                break
            elif corps.isdigit() and len(corps) < 4 or "" in line:
                position2 = file_txt.tell()
                pos2 = False
                line = file_txt.readline()
                corps = line.strip()
                break
            
            
            #lecture des lignes de corps
            if "    " in corps:
                buf = buf + corps[corps.find("    "):].strip() + " "
            elif "    " in line and "    " not in corps:
                buf = buf + corps + " "
            position=file_txt.tell()
            line = file_txt.readline()
            corps = line.strip()
        
    buf = buf.replace("\n","")
    while buf.find("  ") > -1:
        buf = buf.replace("  "," ")        
    return buf


"""
    La fonction find_discussion prend en parametre le nom du fichier texte ouvert
    et renvoie les discussions du document
"""
def find_discussion(file_txt):
    global position
    buf=""
    file_txt.seek(position,0)
    line=file_txt.readline()
    discussion=line.strip()
    pos=0
    limit=0
    while "discussion" not in line.lower() and line:
        line=file_txt.readline()
        discussion=line.strip()
    if "Discussion" in discussion:
        pos=discussion.find("discussion")
        while "conclusion" not in line.lower() and "c onclusion" not in line.lower() and "References" not in line and "R eferences" not in line and "Acknowledgment" not in line:
            line=file_txt.readline()
            discussion=line.strip()
            if pos>=13:
                limit=discussion.find("   ")
                discussion=discussion[limit:]
                buf+=discussion.strip()
            else:
                limit=discussion.find("   ")
                discussion=discussion[:limit]
                buf+=discussion.strip()
    if buf=="":
        buf="ce document ne comporte pas de section 'discussion'." 
    return buf


"""
    La fonction find_conclusion prend en parametre le nom du fichier texte ouvert
    et renvoie la conclusion du document
"""
def find_conclusion(file_txt):
    global position
    buf = ""
    file_txt.seek(position,0)
    line = file_txt.readline()
    conclusion=line.strip()
    pos=0
    drap=0
    limit=0
    while "conclusion" not in line.lower() and "c onclusion" not in line.lower() and "references  " not in line.lower() and "r eferences  " not in line.lower() and "  r eferences" not in line.lower() and "references"!=conclusion.lower() and "TURE WORK" not in line:
        line=file_txt.readline()
        conclusion=line.strip()
    if "conclusion"  in line.lower() or "c onclusion"  in line.lower() or "TURE WORK" in line:
        if "conclusion"  in line.lower():
            pos=line.lower().find("conclusion")
            lg=len(conclusion)
        else:
            pos=conclusion.find("c onclusion")
            lg=len(conclusion)
        if "TURE WORK" in line:
            pos=line.lower().find("TURE WORK")
            lg=len(conclusion)
        while "references  " not in line.lower() and "r eferences  " not in line.lower()  and "r eferences  " not in line.lower() and "  r eferences" not in line.lower() and "references"!=conclusion.lower():
            line=file_txt.readline()
            conclusion=line.strip()
            if pos>15 or lg==125:
                enter=True
                if "17      " in conclusion:
                    drap=1
                    continue
                if drap==0:
                    
                    limit=conclusion.find("   ")
                    conclusion=conclusion[limit:]
                    if "acknowledgments" in conclusion.lower():
                        break
                    if "follow-up work" in conclusion.lower():
                        break
                    buf+=conclusion.strip()
                else:
                    buf+=conclusion
                    if len(conclusion.split())>16:
                        posit=file_txt.tell()
                        if conclusion=="":
                            drap=2
                            continue
                        if drap==2:
                            file_txt.seek(posit,0)
                            drap=3
                        if drap==3:
                            conclusion=conclusion[limit:]
                            conclusion=conclusion.strip()
                            if "acknowledgments" in conclusion.lower():
                                break
                            if "follow-up work" in conclusion.lower():
                                break
                            buf+=conclusion.strip()
                        elif drap!=3 and drap!=2:
                            if "          " in line and "          " not in line.strip():
                                continue
                            conclusion=conclusion[:limit]
                            conclusion=conclusion.strip()
                            if "acknowledgments" in conclusion.lower():
                                break
                            if "follow-up work" in conclusion.lower():
                                break
                            buf+=conclusion
            
            elif pos<=15 and lg!=125:
                limit=conclusion.find("   ")
                if "          " in line and "          " not in line.strip():
                    continue
                ligne=conclusion[:limit] 
                if "acknowledgments" in ligne.lower():
                    break
                if "follow-up work" in conclusion.lower():
                    break
                buf+=ligne
    posit=file_txt.tell()
    if buf=="":
        buf="ce document ne comporte pas de section 'conclusion'."        
    return buf


"""
    La fonction find_reference prend en parametre le nom du fichier texte ouvert
    et renvoie les references du document
"""
def find_references(file_txt):
    global position2
    buf = ""
    file_txt.seek(position2,0)
    line = file_txt.readline()
    ref = line.strip()
    col = False
    pos2 = False
    mark = False
    not_mark=False
    while(line == "\n" or  ("REFERENCES  " not in ref.upper() and "R EFERENCES " not in ref.upper() and ref.upper() != "REFERENCES") and line):
        if "                 " in ref:
            col = True
        if(ref.isdigit() == True and col == True):
            position2=file_txt.tell()
        if(line == "\n" and col == True):
            posi = file_txt.tell()
            line = file_txt.readline()
            ref = line.strip()
            if line == "\n":
                position2 = file_txt.tell()
            else:
                file_txt.seek(posi,0)
        
        line = file_txt.readline()
        ref = line.strip()
        if("    " in ref and ("    REFERENCES" in ref.upper() or "    R EFERENCES" in ref.upper()) and ref[0].upper() != "R"):
            line2 = ""
            for i in range(len(ref)):
                if("     " in ref and ref[i] == " " and ref[i+1] == " " and ref[i+2] == " "):
                    break
            while(i < len(ref)):
                line2 = line2 + ref[i]
                i = i + 1
            ref2 = line2.strip()
            if(("REFERENCES" in ref2.upper() or "R EFERENCES" in ref2.upper()) and ref2[0].upper() == "R"):
                pos2 = True
                mark = True
                break
       
    drap = True               
    while(drap == True and line):
        while(line and pos2 != True):
            for i in range (len(ref)):
                if("         " in line and "    " not in ref):
                    break
                buf = buf+ref[i]
                if("    " in ref and ref[i] == " " and ref[i+1] == " " and ref[i+2] == " "):
                    break
            buf = buf+"\n"
            line = file_txt.readline()
            ref  = line.strip()
            if(not line):
                drap = False
                break
            elif((ref.isdigit() and col == True) or ("1967." in ref)):
                file_txt.seek(position2,0)
                pos2 = True
            elif(line == "\n"):
                line = file_txt.readline()
                ref = line.strip()
                if(not line and col == True):
                    file_txt.seek(position2,0)
                    pos2 = True
                elif(( line == "\n" or ref.isdigit()) and col == True):
                    file_txt.seek(position2,0)
                    line = file_txt.readline()
                    ref = line.strip()
                    pos2 = True

        while(line and pos2 == True):
            mark2 = True
            esp = ref.find("       ")
            if(esp != -1):
                ref2 = ref[esp : len(ref)].strip()
                if(ref2.find("   ") != -1):
                    mark2 = False 
            if("     " in ref and mark2 == True):
                line2 = ""
                i = len(ref)-1
                while(ref[i] != " " or ref[i-1] != " " or ref[i-2] != " "):
                    line2 = line2 + ref[i]
                    i = i - 1
                i = len(line2)-1
                ref2 = ""
                while(i >= 0 ):
                    ref2 = ref2+line2[i]
                    i = i-1
                if( "*" not in ref2 and "+" not in ref2 and "=" not in ref2):
                    buf = buf + ref2 + "\n"
            if("                             " in line and "              "not in ref and len(ref)>20 and "*" not in ref and "+" not in ref and "=" not in ref):
                buf = buf + ref + "\n" 
            line = file_txt.readline()
            ref = line.strip()
            if not line:
                drap = False
            elif "     " in ref and mark:
                pos2 = False
            elif(ref.isdigit()):
                pos2 = False
                position2 = file_txt.tell()
            elif(line == "\n"):
                posi = file_txt.tell()
                line = file_txt.readline()
                ref = line.strip()
                if(not line):
                    drap = False
                elif(line == "\n"):
                    position2 = file_txt.tell()
                    pos2 = False
                else:
                    file_txt.seek(posi,0)
    buf = buf.replace("\n"," ")
    buf = buf.replace("References","")
    buf = buf.replace("R EFERENCES","")
    return buf
