import requests
import csv
import webbrowser
import time

###INSTALLER PYTHON 

###LIEU D ENREGISTREMENT DES DONNEES OU SE TROUVE LE FICHIER CSV et le fichier defis.py (remplacer \ par \\)
path="C:\\Users\\helen\\Documents\\GitHub\\Jura7Park"


####LAncer la commande suivante une fois python installé : pip install -r requirements.txt


####Modifier le fichier defis.csv avec les données de votre choix

tab = open('ajouts.csv', 'r')
reader = csv.reader(tab, delimiter=',')
for row in reader :
    user = row[0]
    montant = row[1]
    raison = row[2]
    url = 'http://jura7park.fr/adjust/'+user+'/'+montant+'/'+raison
    print(url)
    webbrowser.open_new_tab(url)
    time.sleep(1)
