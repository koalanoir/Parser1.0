"""

    parser precision

    by @dorian version 26/04/2021

    calculate the precision of parser programme 

    using two directory : references one and the parser result

    syntax : parser_precision.py parser_file reference_file

    print : percentage egality between  reference_file and parser_file for each part :

    title, author, abstract and conclusion

"""

#librairie

import os

import sys

import shutil

import string

from os import listdir

from os.path import isfile,join

from os.path import basename



# definition des variables

f1=open(sys.argv[1],"r")
f2=open(sys.argv[2],"r")





# definition des fonctions

def calculWordTxt(fiLe):

    numberList=[]
    wordsNumber=0
    start=False
    end=False
    titre="<titre>"

    ftitre="</titre>"

    auteur="<auteurs>"

    fauteur="</auteurs>"

    abstract="<abstract>"

    fabstract="</abstract>"

    conclusion="<conclusion>"

    fconclusion="</conclusion>"

    line=fiLe.readline()

    while line:

        if titre in line:

            wordsNumber+=len(line)

        if ftitre in line:

            break

        line=fiLe.readline()

    numberList.append(wordsNumber)

    wordsNumber=0

    start=False

    end=False

    while line:

        if auteur in line:

            start=True

        if start==True:

            wordsNumber+=len(line)

        if fauteur in line:

            end =True

        if fauteur not in line and end==True:

            break

        line=fiLe.readline()

    numberList.append(wordsNumber)

    wordsNumber=0

    start=False

    end=False

    while line:

        if abstract in line:

            start=True

        if start==True:

            wordsNumber+=len(line)

        if fabstract in line:

            end =True

        if fabstract not in line and end==True:

            break

        line=fiLe.readline()

    numberList.append(wordsNumber)

    wordsNumber=0

    start=False

    end=False

    while line:

        if conclusion in line:

            start=True

        if start==True:

            wordsNumber+=len(line)

        if fconclusion in line:

            end =True

        if fconclusion not in line and end==True:

            break

        line=fiLe.readline()

    numberList.append(wordsNumber)

    wordsNumber=0

    start=False

    end=False

    if len(numberList)!=4:

        print("count word error")

    return numberList



def precisionParser(List):

    parts=["titre : ","auteurs : ","abstract : ","conclusion : "," précision du parser : "]

    if len(parts)!=len(List):

        return "calcul precision eror: missing parts"

    else:

        for i in range(len(List)):

            print(""+parts[i]+str(List[i])+"\n")

        return "end."

def ecarts(listA,listB):

    listDiff=[]
    total=0
    if len(listA)==len(listB):

        for i in range(len(listA)):

            percent=(listA[i]/listB[i])*100
            total+=percent
            listDiff.append(percent)
        total/=4
        listDiff.append(total)
    else:

        print("size error")    

    return listDiff 





#main

parserSize=calculWordTxt(f1)

referenceSize=calculWordTxt(f2)

print(""+basename(sys.argv[1])+" precision : "+"\n")

list=ecarts(referenceSize,parserSize)

precisionParser(list)

