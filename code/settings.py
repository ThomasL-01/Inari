#dimensions de la fenetre
screen_width = 1280 
screen_height = 1000

tile_size = 50  #Règle la taille des blocks a modifier si besoin (écran trop petit)
#regle le nombre de frame par secondes a 60
FPS = 60



#Données sur les monstres boss et skeleton
mob_data = {
    'boss': {'health':300, 'damage': 12, 'boss_sound': '../sounds/boss/sound_boss.mp3', 'speed': 3,  'attack_radius': 60,  'notice_radius': 450, 'knockback': 2},
    'skeleton': {'health':40, 'damage': 5, 'death_sound':'../sounds/skeleton/death.mp3', 'speed': 2, 'attack_radius': 30, 'notice_radius': 350, 'knockback': 3}
}


speech ={
    1:"Salutations jeune aventurier, pourrais tu m'aider ? Je suis à la recherche de pierres rares",
    2:'Oui je pense pouvoir vous aider',
    3:'Très bien ! Tu trouveras ces pierres sur les monstres que tu vaincras...',
    4:"En échange, je suis pret à te donner des objets qui pourraient t'être utile pour trouver la sortie de ce lieu !",
    5:'Merci beaucoup !',
    6:'Aussi je te met en garde, cet endroit regorge de pièges. Certaines portes te ramènent à ton point de départ !',
    7:'menu',
    8:'A la prochaine !',
    9:'Ah te revoilà !'
}

player_stats = {'health': 100, 'speed' : 4, 'damage': 15, 'stamina': 200, 'max_health': 200, 'max_speed':7, 'max_stamina':300, 'max_damage':30}

bar_height = 20 #hauteur barre de vie
health_bar_width = player_stats['health'] *2  #largeur barre de vie
stamina_bar_width = player_stats['stamina'] * 0.8
ui_font = '../graphics/autres/ARCADEPI.TTF' #police pour l'interface utilisateur
ui_font_size = 40   #taille de la police
