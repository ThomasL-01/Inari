import csv

#creer une nouvelle sauvegarde
def nouvelle_sauvegarde(pseudo, mdp, current_salle, vie, boss, s_purp, s_green, s_red, pot_3, pot_14, pot_nb, coin, gem,p_stock,strength_stock,stamina_stock,health_stock,speed_stock,res_stock):
    f = open("csvfile.csv",'a')
    w = csv.DictWriter(f, ["pseudo", "mdp", "current_salle", "vie", "boss", "s_purp", "s_green", "s_red",'pot_3','pot_14', 'pot_nb', 'coin', 'gem','p_stock','strength_stock','stamina_stock','health_stock','speed_stock','res_stock'])
    w.writerow({"pseudo": pseudo, "mdp": mdp, 'current_salle': current_salle, "vie": vie, "boss": boss, "s_purp": s_purp, "s_green": s_green, "s_red": s_red,'pot_3':pot_3, 'pot_14':pot_14, 'pot_nb':pot_nb, 'coin':coin, 'gem':gem,'p_stock':p_stock,'strength_stock':strength_stock,'stamina_stock':stamina_stock,'health_stock':health_stock,'speed_stock':speed_stock,'res_stock':res_stock})
    f.close()

#verifie une sauvegarde déjà existante
def verif_sauvegarde(pseudo, mdp,  table):
    f = open(table, 'r')
    table = list(csv.DictReader(f))
    for e in table:
        if pseudo == e['pseudo'] and mdp == e['mdp'] :
            return False
    f.close()
    return True

#verifie que le pseudo choisi est original
def verifpseudo(pseudo, table):
    f = open(table, 'r')
    table =list(csv.DictReader(f))
    for e in table:
        if e ['pseudo'] == pseudo:
            return True
    f.close()
    return False

#systeme de sauvegarde en jeu
def sauvegarde(pseudo, mdp, current_salle, vie, boss, s_purp, s_green, s_red, pot_3, pot_14, pot_nb, coin, gem,p_stock,strength_stock,stamina_stock,health_stock,speed_stock,res_stock,table):
    f = open(table, 'a')
    w = csv.DictWriter(f, ["pseudo", "mdp", "current_salle", "vie", "boss", "s_purp", "s_green", "s_red",'pot_3','pot_14', 'pot_nb', 'coin', 'gem','p_stock','strength_stock','stamina_stock','health_stock','speed_stock','res_stock'])
    w.writerow({"pseudo": pseudo, "mdp": mdp, 'current_salle': current_salle, "vie": vie, "boss": boss, "s_purp": s_purp, "s_green": s_green, "s_red": s_red,'pot_3':pot_3, 'pot_14':pot_14, 'pot_nb':pot_nb, 'coin':coin, 'gem':gem,'p_stock':p_stock,'strength_stock':strength_stock,'stamina_stock':stamina_stock,'health_stock':health_stock,'speed_stock':speed_stock,'res_stock':res_stock})
    f.close()
    
 #récupère la sauvegarde d'un utilisateur   
def recup_sauvegarde(pseudo, table):
    f = open(table, 'r')
    table = list(csv.DictReader(f))
    for e in table:
        if e['pseudo'] == pseudo:
            a = {'pseudo': e['pseudo'], 'mdp': e['mdp'], 'current_salle':e['current_salle'], 'vie':e['vie'], 'boss':e['boss'], 's_purp':e['s_purp'], 's_green':e['s_green'], 's_red':e['s_red'], 'pot_3':e['pot_3'], 'pot_14':e['pot_14'], 'pot_nb':e['pot_nb'], 'coin':e['coin'], 'gem':e['gem'],'p_stock':e['p_stock'],'strength_stock':e['strenght_stock'],'stamina_stock':e['stamina_stock'],'health_stock':e['health_stock'],'speed_stock':e['speed_stock'],'res_stock':e['res_stock']}
    f.close()
    return a['pseudo'], e['mdp'],a['current_salle'], a['vie'], a['boss'], a['s_purp'], a['s_green'], a['s_red'], a['pot_3'], a['pot_14'], a['pot_nb'], a['coin'], a['gem'], a ['p_stock'], a['strength_stock'], a['stamina_stock'], a['health_stock'], a['speed_stock'], a['res_stock']
