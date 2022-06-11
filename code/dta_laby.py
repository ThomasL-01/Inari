import numpy as np
from io import StringIO
import json

#on importe les json et on les stocke dans un dictionnaire
salles = {"dispo_sol_mur":{}, "reste":{}}
p1 = {}
p2 = {}
with open("../salles/salles_p1.json", 'r') as file_p1:
    p1 = json.load(file_p1)
with open("../salles/salles_p2.json", 'r') as file_p2:
    p2 = json.load(file_p2)

for i in range(1, 37):
    #on formate les données
    salle = StringIO(p1[str(i)])
    #on convertit les données en tableau
    salles["dispo_sol_mur"][i] = np.loadtxt(salle, delimiter=',', dtype=str).tolist()
    salle = StringIO(p2[str(i)])
    salles["reste"][i] = np.loadtxt(salle, delimiter=',', dtype=str).tolist()

#renvoi un dictionnaire de dictionnaires avec les salles en tableau