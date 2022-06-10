from random import randint
import pygame
from support import import_csv_dispo
from settings import *
from player import Player
from tile import * 
from UI import *
from enemy import Enemy
from dta_laby import *
from sauvegarde import *

class Level:    #classe du jeu en entier
    def __init__(self, mdp, current_salle, utilisateur, vie, boss, s1, s2, s3, pot_3, pot_14, pot_nb, coin, gem, tile_size, sound_volume): #recupere les donnees du joueur
        self.display_surface = pygame.display.get_surface()
        self.tile_size = tile_size
        self.game_paused = False
        self.pause = False
        self.is_trading = False
        self.val = 1
        self.on_menu = False
        
        #Récupère les données du joueur
        self.utilisateur = utilisateur
        self.vie = int(vie)
        self.boss_statut = boss
        self.mdp = mdp
        self.current_salle = int(current_salle)
        self.sound_volume = sound_volume /100

        #Créer les différents groupes de sprites
        self.visible_sprites = Enemy_update()
        self.obstacles_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()
        self.key_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        
            
        #utilisateur
        self.ui = UI()
        self.win_statut = None
        self.player_spawn = '15'
        self.player_take_damage = 0
        self.damage =  15
        self.speed = 4
        
        
        #Setup des différentes clés
        self.purp_statut = s1
        self.purp_key_spawn = '8'
        self.green_statut = s2
        self.green_key_spawn = '10'
        self.red_statut = s3
        self.red_key_spawn = '9'
        
        #Sons et conditions pour pas que ça le face à l'infini
        self.key_purp_sound = True
        self.key_green_sound = True
        self.key_red_sound = True
        self.warning_statut = True
        self.pause_sound_statut = True
        self.skeleton_music_statut = True
        self.skeleton_music = pygame.mixer.Sound('../sounds/Spooky Scary Skeletons.mp3')
        self.door_sound = pygame.mixer.Sound('../sounds/door.mp3') 
        self.potion_sound = pygame.mixer.Sound('../sounds/potion.mp3')
        self.heal_sound = pygame.mixer.Sound('../sounds/heal.mp3')
        self.sound_collect = pygame.mixer.Sound('../sounds/coin copie.wav')

        #Setup des potions
        self.potion_nb = int(pot_nb)
        self.potion_statut_3 = pot_3
        self.potion_statut_14 = pot_14
        self.potion_statut = False
        self.potion_cooldown_start = None
        self.potion_cooldown = 700
        
        #setup des coins
        self.have_spawned = False
        self.coin_nb = int(coin)
        self.gem_nb = int(gem)
        self.coin_cooldown_start = None
        self.coin_cooldown = 700
        
        #save setup
        self.save_cooldown = 5000
        self.save_statut = True
        self.save_cooldown_start = None
        
        #liste de chaques types de portes pour les identifier
        self.liste_door_h = [2,3,4,5,6,7,9,10,11,13,14,18,19,21,24,25,27,28,29,35]
        self.liste_door_b = [8,9,10,11,12, 13,15,16,17,19,20,24,25,27,28,31,33,34,35]
        self.liste_door_g = [3, 2, 10, 11, 12, 14, 16, 19, 22, 23, 24, 27, 29,30, 32, 35, 36]
        self.liste_door_d = [1, 2, 7, 9, 10, 11, 13, 15, 21, 22, 23, 26, 28, 29, 30, 31, 34, 35, 36]  
        
        self.trader = None 
        self.can_collide_trader = True
        self.trader_coll_cooldown = 2000
        self.start_coll = None
        
        #Créer la salle
        self.create_salle(salles['dispo_sol_mur'][self.current_salle])
        self.create_dispo_objet(salles['reste'][self.current_salle])
                                        
    def create_salle(self, dispo): #Créer la disposition des murs et sols de la salle

        self.sprite_group = pygame.sprite.Group
        for row_index, row in enumerate(dispo):
            for col_index, col in enumerate(row):
                x = col_index * self.tile_size
                y = row_index * self.tile_size
                if col == '4':
                    sprite = Vide_sol([ self.visible_sprites], '../graphics/autres/vide.png', (x+200,y), self.current_salle)
                    self.sprite_group.add(sprite)
                if col == '3':
                    sprite = Vide_sol([ self.visible_sprites], '../graphics/autres/sol.png', (x+200,y), self.current_salle)
                    self.sprite_group.add(sprite)
                if col == '2':
                   sprite =  Mur((x+200,y),[self.visible_sprites, self.obstacles_sprites], '../graphics/autres/mur.png', self.current_salle)
                   self.sprite_group.add(sprite)
                if col == '1':
                    sprite = Mur((x+200,y),[self.visible_sprites, self.obstacles_sprites], '../graphics/autres/mur d.png', self.current_salle)
                    self.sprite_group.add(sprite)
                if col == '0':
                   sprite =  Mur((x+200,y),[self.visible_sprites, self.obstacles_sprites], '../graphics/autres/mur g.png', self.current_salle)
                   self.sprite_group.add(sprite)
                                    
    def trouve_salle(self, liste): #Vérifie si une porte se trouve bien dans la salle donnée
        for i in range(len(liste)):
            if liste[i] == self.current_salle:
                return True
        return False
                    
    def create_dispo_objet(self, dispo): #Créer le reste de la salle (clés, potions, spawns...)
        for row_index, row in enumerate(dispo):
            for col_index, col in enumerate(row):
                if col != '-1':
                    x = col_index * self.tile_size
                    y = row_index * self.tile_size
                    if self.current_salle == 6 and self.potion_statut_3 == 'on ground':
                        if col == '70':
                            self.potion_3 = Potion([self.visible_sprites, self.key_group], (x+215,y+15), self.current_salle)
                    else:
                        self.potion_3 = None
                        
                    if self.current_salle == 14 and self.potion_statut_14 == 'on ground':
                        if col == '70':
                            self.potion_14 = Potion([self.visible_sprites, self.key_group], (x+215,y+15), self.current_salle)
                    else:
                        self.potion_14 = None 
                    if self.trouve_salle(self.liste_door_g) : 
                        if col == '11':
                            #porte vers la gauche
                            self.door_g = Porte([ self.visible_sprites], '../graphics/autres/porte g.png' , (x+200,y+30), self.current_salle)
                    else:
                        self.door_g = None
                    if col == '16':
                        #torche 
                        Lux([ self.visible_sprites], (x+220,y+5), self.current_salle)
                        
                    if self.trouve_salle(self.liste_door_b):  
                        if col == '14':
                            #port vers le bas
                            self.door_b = Porte([self.visible_sprites], '../graphics/autres/porte.png', (x+200,y), self.current_salle)
                    else:
                        self.door_b = None
                        
                    if self.trouve_salle(self.liste_door_h):
                        if col == '20':
                            #porte vers le haut
                            self.door_h = Porte([self.visible_sprites], '../graphics/autres/porte.png', (x+200,y), self.current_salle)
                    else:
                        self.door_h = None
                    if self.trouve_salle(self.liste_door_d) : 
                        if col == '12':
                            #porte vers la droite
                            self.door_d = Porte([self.visible_sprites], '../graphics/autres/porte d.png', (x+200,y+30), self.current_salle)
                    else:
                        self.door_d = None
                    if col == '7':
                        #porte verouillée rouge
                        self.locked_door_red = Locked_porte_rouge([self.visible_sprites], '../graphics/autres/porte rouge.png',(x+200,y), self.red_statut, self.current_salle)
                    if col == '6':
                        #porte verouillée verte
                        self.locked_door_green =  Locked_porte_verte([self.visible_sprites], '../graphics/autres/porte verte.png',(x+200,y), self.green_statut, self.current_salle)
                    if col == '5':
                        #porte verouillée violette
                        self.locked_door_purp =  Locked_porte_violette([self.visible_sprites], '../graphics/autres/porte violette.png',(x+200,y), self.purp_statut, self.current_salle)
                    if col == self.purp_key_spawn and self.purp_statut == 'locked':
                        #clé violette (salle 5)
                        self.clé_purp = Clé_violette([self.visible_sprites, self.key_group], '../graphics/autres/cl_violette.png', (x+200,y), self.current_salle)
                    if col == self.red_key_spawn and self.red_statut == 'locked':
                        #clé rouge (salle 32)
                        self.clé_red= Clé_rouge([self.visible_sprites, self.key_group], '../graphics/autres/cl_rouge.png', (x+200,y), self.current_salle)
                    if col == self.green_key_spawn and self.green_statut == 'locked':
                        #clé verte (salle 18)
                        self.clé_green = Clé_verte([self.visible_sprites, self.key_group], '../graphics/autres/cl_verte.png', (x+200,y), self.current_salle)
                    if col == self.player_spawn:
                        #apparition joueur
                        self.player = Player((x+200,y), [self.visible_sprites, self.player_group], self.obstacles_sprites, self.current_salle, self.vie, self.coin_nb, self.gem_nb, self.sound_volume)
                    if col == '100':
                        self.trader = Trader([self.visible_sprites, self.obstacles_sprites], (x+215,y+10), self.current_salle, self.visible_sprites)       
                    if col == '13' or col == '17':
                        #apparition entitées
                        if col == '13': 
                            self.enemy = Enemy('skeleton', (x+210,y), [self.visible_sprites, self.attackable_sprites], self.obstacles_sprites, self.visible_sprites, self.damage_player, self.coin_collision, self.current_salle, self.sound_volume)
                            self.enemy_group.add(self.enemy)
                        if col == '17' and self.boss_statut == 'alive': 
                            self.boss_statut = 'alive'
                            self.enemy = Enemy('boss', (x+200,y), [self.visible_sprites, self.attackable_sprites], self.obstacles_sprites, self.visible_sprites, self.damage_player, self.coin_collision, self.current_salle, self.sound_volume)
                            self.enemy_group.add(self.enemy)
                    if col == '22':
                        Mur((x+200,y),[self.visible_sprites, self.obstacles_sprites], '../graphics/autres/baril.png', self.current_salle)
                                                               
    def check_key_collision(self): #Check la collision avec la clé et change le statut de la porte pour pouvoir l'ouvrir
        #clé violette
        if self.current_salle == 5 and self.purp_statut == 'locked':
            if pygame.sprite.collide_rect(self.player, self.clé_purp):
                self.clé_purp.kill()
                self.purp_statut = 'clé'    #change le statut de la porte
                self.purp_key_spawn = '90' #permet de ne plus faire spawn la clé en changeant son ID de spawn
                if self.key_purp_sound:
                    self.sound_collect.set_volume(self.sound_volume)
                    self.sound_collect.play()
                    self.key_purp_sound = False
                    self.ui.draw_keys('purp', 'clé')
        #clé rouge
        if self.current_salle == 32 and self.red_statut == 'locked':
            if pygame.sprite.collide_rect(self.player, self.clé_red):
                self.clé_red.kill()
                self.red_statut = 'clé'
                self.red_key_spawn = '90'
                if self.key_red_sound:
                    self.sound_collect.set_volume(self.sound_volume)
                    self.sound_collect.play()
                    self.key_red_sound = False
                    self.ui.draw_keys('red', 'clé')
        #clé verte
        if self.current_salle == 18 and self.green_statut == 'locked':
            if pygame.sprite.collide_rect(self.player, self.clé_green):
                self.clé_green.kill()
                self.green_statut = 'clé'
                self.green_key_spawn = '90'
                if self.key_green_sound:
                    self.sound_collect.set_volume(self.sound_volume)
                    self.sound_collect.play()
                    self.key_green_sound = False
        
        #Permet l'affichage de la clé dans l'inventaire
        if self.red_statut == 'clé':
            self.ui.draw_keys('red', 'clé')
        if self.green_statut == 'clé':
            self.ui.draw_keys('green', 'clé')
        if self.purp_statut == 'clé':
            self.ui.draw_keys('purp', 'clé')
        
    def change_salle(self): # permet le changement de salle
        #fake porte dans les salles 19 30 et 35 
        if self.door_g != None:
            if pygame.sprite.collide_mask(self.player, self.door_g) and self.current_salle == 19:
                self.door_sound.play()
                self.current_salle = 3
                self.player_spawn = '15'
                self.vie = self.player.health - self.player_take_damage
                self.clear_salle()
                self.create_salle(salles['dispo_sol_mur'][self.current_salle])
                self.create_dispo_objet(salles['reste'][self.current_salle])
                
                
        if self.door_d != None:
            if pygame.sprite.collide_mask(self.player, self.door_d) and self.current_salle == 30:
                self.door_sound.play()
                self.current_salle = 3
                self.player_spawn = '15'
                self.vie = self.player.health - self.player_take_damage
                self.clear_salle()
                self.create_salle(salles['dispo_sol_mur'][self.current_salle])
                self.create_dispo_objet(salles['reste'][self.current_salle])
                
        if self.door_h != None:
            if pygame.sprite.collide_mask(self.player, self.door_h) and self.current_salle == 35:    
                self.door_sound.play()
                self.current_salle = 3
                self.player_spawn = '15'
                self.vie = self.player.health - self.player_take_damage
                self.clear_salle()
                self.create_salle(salles['dispo_sol_mur'][self.current_salle])
                self.create_dispo_objet(salles['reste'][self.current_salle])

        #vraies portes pour changer de salle
        if self.door_d != None and self.current_salle != 36:
            if pygame.sprite.collide_mask(self.player, self.door_d): #porte à droite
                self.vie = self.player.health - self.player_take_damage
                self.door_sound.play()
                self.current_salle += 1
                self.player_spawn = 'Pg'
                self.clear_salle()
                self.create_salle(salles['dispo_sol_mur'][self.current_salle])
                self.create_dispo_objet(salles['reste'][self.current_salle])
        
        if self.door_g != None  and self.current_salle != 36:
            if pygame.sprite.collide_mask(self.player, self.door_g):#porte à gauche
                self.skeleton_music_statut = True
                self.skeleton_music.stop()
                self.vie = self.player.health - self.player_take_damage
                self.door_sound.play()
                self.current_salle -= 1
                self.player_spawn = 'Pd'
                self.clear_salle()
                self.create_salle(salles['dispo_sol_mur'][self.current_salle])
                self.create_dispo_objet(salles['reste'][self.current_salle])
        
        if self.door_b != None:   
            if pygame.sprite.collide_rect(self.player, self.door_b):
                self.door_sound.play()
                self.vie = self.player.health - self.player_take_damage
                self.current_salle -= 6
                self.player_spawn = 'Ph'
                self.clear_salle()
                self.create_salle(salles['dispo_sol_mur'][self.current_salle])
                self.create_dispo_objet(salles['reste'][self.current_salle])
        
        if self.door_h != None:
            if pygame.sprite.collide_rect(self.player, self.door_h):
                self.skeleton_music_statut = True
                self.skeleton_music.stop()
                self.door_sound.play()
                self.vie = self.player.health - self.player_take_damage
                self.current_salle += 6
                self.player_spawn = 'Pb'
                self.clear_salle()
                self.create_salle(salles['dispo_sol_mur'][self.current_salle])
                self.create_dispo_objet(salles['reste'][self.current_salle])        
                
        if self.current_salle == 14 and self.skeleton_music_statut:
            self.skeleton_music.play()
            self.skeleton_music.set_volume(self.sound_volume)
            self.skeleton_music_statut = False
                    
    def clear_salle(self): # permet de détruire la salle précédante pour créer la nouvelle en détruisant TOUT les sprites (y compris le joueur)
        for clear in self.visible_sprites:
            if clear.salle != self.current_salle:
                clear.kill()
                     
    def check_locked_door(self):  #vérifie les collisions avec les portes vérouillées et leur statut
        #porte rouge (salle 20)
        if self.current_salle == 20:
            if pygame.sprite.collide_mask(self.player, self.locked_door_red):
                #Vérification du statut et action correspondante
                if self.red_statut == 'open':
                    self.door_sound.play()
                    self.player_spawn = 'Pb'
                    self.current_salle += 6
                    self.vie = self.player.health - self.player_take_damage
                    self.clear_salle()
                    self.create_salle(salles['dispo_sol_mur'][self.current_salle])
                    self.create_dispo_objet(salles['reste'][self.current_salle])
                    
                elif self.red_statut == 'clé':
                    self.red_statut = 'open'
                else:
                    police = pygame.font.SysFont(ui_font, ui_font_size)
                    texte = police.render('Porte verouillée', 1 , 'red')
                    self.display_surface.blit(texte, (550, 10))
                
        #porte verte (salle 22)
        if self.current_salle == 22:
            if pygame.sprite.collide_mask(self.player, self.locked_door_green):
                if self.green_statut == 'open':
                    self.door_sound.play()
                    self.player_spawn = 'Pb'
                    self.current_salle += 6
                    self.vie = self.player.health - self.player_take_damage
                    self.clear_salle()
                    self.create_salle(salles['dispo_sol_mur'][self.current_salle])
                    self.create_dispo_objet(salles['reste'][self.current_salle])
                
                elif self.green_statut == 'clé':
                    self.green_statut = 'open'
                else:
                    police = pygame.font.SysFont(ui_font, ui_font_size)
                    texte = police.render('Porte verouillée', 1 , 'red')
                    self.display_surface.blit(texte, (550, 10))
                      
        #porte violette (salle 8)           
        if self.current_salle == 8:  
            if pygame.sprite.collide_mask(self.player, self.locked_door_purp):
                if self.purp_statut == 'open':
                    self.door_sound.play()
                    self.player_spawn = 'Pd'
                    self.current_salle -= 1
                    self.vie = self.player.health - self.player_take_damage
                    self.clear_salle()
                    self.create_salle(salles['dispo_sol_mur'][self.current_salle])
                    self.create_dispo_objet(salles['reste'][self.current_salle])
                
                elif self.purp_statut == 'clé':
                    self.purp_statut = 'open'
                else:
                    police = pygame.font.SysFont(ui_font, ui_font_size)
                    texte = police.render('Porte verouillée', 1 , 'red')
                    self.display_surface.blit(texte, (550, 10))     
                     
    def check_player_death(self): #check si le joueur meurt (vie = 0)
        if self.player.health <= 0:
            self.win_statut = 'Game over'

    def damage_player(self, amount, statut): #Fonction permettant de mettre des dégats au joueur  
        if statut != 'dead':
            if self.player.vulnerable:
                self.player.health -= amount
                self.player.vulnerable = False
                self.player.hurt_time = pygame.time.get_ticks()
                self.hurt_sound = pygame.mixer.Sound('../sounds/hurt copie.wav')
                self.hurt_sound.play()
            if self.player.health <= 25 and self.warning_statut:
                self.warning = pygame.mixer.Sound('../sounds/warning copie.wav')
                self.warning_statut = False
                self.warning.play()
            
    def player_attack_logic(self):  #systeme d'attacque du joueur (si il est en attack animation alors le monstre prends des dégats)
        if pygame.sprite.spritecollide(self.player, self.attackable_sprites, False):
            enemy_collision = pygame.sprite.spritecollide(self.player, self.attackable_sprites, False, pygame.sprite.collide_mask)
            if enemy_collision:
                for enemy in enemy_collision:
                    if self.player.status == 'right_attack' or self.player.status == 'left_attack':
                        enemy.get_damage(self.player)
        
    def check_boss(self):   #vérifie le statut du boss, pour son animation de mort et les portes bloquées
        if self.enemy.monster_name == 'boss':
            if self.enemy.health <= 0: 
                return 'dead'
            return 'alive'
     
    def check_win(self):    #Vérifie si le joueur a vaincu le boss
        #Si oui :
        if self.current_salle == 36 and self.boss_statut == 'dead':
            if pygame.sprite.collide_mask(self.player, self.door_d):
                self.win_statut = 'Win'
        
        #Si non: (le player ne peut pas sortir de la salle)
        elif self.current_salle == 36 and self.boss_statut == 'alive':
            if pygame.sprite.collide_mask(self.player, self.door_d) or pygame.sprite.collide_mask(self.player, self.door_g):
                police = pygame.font.SysFont(ui_font, ui_font_size)
                texte = police.render('Le Boss ne vous laissera pas sortir si facilement !', 1 , 'red')
                self.display_surface.blit(texte, (300, 500))        
    
    def potion_update(self):    #Systeme de potions de soin
        #Vérifie la pos et le statut de la potion (pour pas en avoir à l'infini)
        if self.current_salle == 6 and self.potion_statut_3 == 'on ground':
            if pygame.sprite.collide_rect(self.player, self.potion_3) :
                self.potion_3.kill()
                self.potion_sound.play()
                self.potion_statut_3 = 'recup'
                self.potion_nb += 1
                self.ui.draw_potions(self.potion_nb)
        #idem salle 14
        if self.current_salle == 14  and self.potion_statut_14 == 'on ground':
            if pygame.sprite.collide_rect(self.player, self.potion_14):
                self.potion_14.kill()
                self.potion_sound.play()
                self.potion_statut_14 = 'recup'
                self.potion_nb += 1
                self.ui.draw_potions(self.potion_nb)
        
        #Déssine l'inventaire des potions du joueur
        if self.potion_nb > 0:
            self.ui.draw_potions(self.potion_nb)
        keys = pygame.key.get_pressed()
        
        #systeme de soins si espace est préssée (et si le joueur n'a pas 100 pv)
        if keys[pygame.K_RETURN] and self.potion_nb > 0 and self.player.health < player_stats['health'] and self.potion_statut == False and self.player.can_get_input:
            self.potion_cooldown_start = pygame.time.get_ticks()
            self.potion_nb -= 1
            self.potion_statut = True
            self.heal_sound.play()
            if self.player.health + 30 > player_stats['health']:
                self.player.health = player_stats['health']
            else:
                self.player.health += 30
                if self.warning_statut == False and self.player.health > 25:
                    self.warning_statut = True
           
    def trader_update(self):
        if self.can_collide_trader and self.current_salle == 17:
            if self.trader != None: #rajouter un timer pour pouvoir sortir du menu sinon on sera non stop en collision
                if pygame.sprite.collide_rect(self.player, self.trader):
                    self.speech_sound = pygame.mixer.Sound('../sounds/Villager.mp3')
                    self.speech_sound.play()
                    self.is_trading = True
                    self.game_paused = True
                    self.player.can_get_input = False
     
    def coin_collision(self, coin_group, start):
        val = randint(1,3)
        current_time = pygame.time.get_ticks()
        for enemy in self.enemy_group:
            for coin in coin_group:
                
                if enemy.coin != None:
                    if current_time - start >= self.coin_cooldown and pygame.sprite.collide_rect(self.player, coin):
                        enemy.coin_statut = False
                        coin.kill()
                        self.sound_collect.set_volume(self.sound_volume /3)
                        self.sound_collect.play()
                        
                        self.coin_nb += val
                        self.player.coin += val
                if enemy.gem != None:
                    if current_time - start >= self.coin_cooldown and pygame.sprite.collide_rect(self.player, coin):
                        enemy.coin_statut = False
                        coin.kill()
                        self.sound_collect.set_volume(self.sound_volume /3)
                        self.sound_collect.play()
                        self.gem_nb += 1
                        self.player.gem += 1
        if self.enemy_group == []:
            for coin in coin_group:
                coin.kill()
                       
    def cooldowns_verif(self):
        #cooldown pour les potions (pour pas tout boire d'un coup)
        
        current_time = pygame.time.get_ticks()
        
        if self.potion_statut == True:
            if current_time - self.potion_cooldown_start >= self.potion_cooldown:
                self.potion_statut = False
                
        if self.can_collide_trader == False:
            if current_time - self.start_coll >= self.trader_coll_cooldown:
                self.can_collide_trader = True
        
                
        if self.save_statut == False:
            if current_time - self.save_cooldown_start >= self.save_cooldown:
                self.save_statut = True
        
        if self.current_salle == 8 or self.current_salle == 20 or self.current_salle == 22: 
            self.check_locked_door()
        
        #vérifie le statut du boss (si salle = 36)
        if self.current_salle == 36 and self.boss_statut == 'alive':
            self.ui.show_boss_bar(self.enemy.health, 300, self.ui.boos_bar_rect)
            self.boss_statut = self.check_boss()
            
        if self.player.stamina < player_stats['stamina'] and not self.player.attacking:
            self.player.stamina += 0.8
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s] and self.save_statut:
            self.save_statut = False
            self.save_cooldown_start = pygame.time.get_ticks()
            sauvegarde(self.utilisateur, self.mdp, int(self.current_salle), self.player.health , self.boss_statut, self.purp_statut, self.green_statut, self.red_statut, self.potion_statut_3, self.potion_statut_14, self.potion_nb, self.player.coin, self.player.gem, 'csvfile.csv')
        
        if keys[pygame.K_m]:
            self.pause = not self.pause
            self.game_paused = not self.game_paused
        if self.pause:
            if self.pause_sound_statut:
                self.pause_sound = pygame.mixer.Sound('../sounds/pause.wav')
                self.pause_sound.set_volume(self.sound_volume/2)
                self.pause_sound.play()
                self.pause_sound_statut = False
            self.pause_menu()
        if not self.pause:
            self.ui.button_list = []
            self.continue_button = None
            self.title_button = None
                            
        if self.player.coin >= 100 and self.utilisateur != 'Dev' and self.mdp != 'V.devcode':
            self.player.coin -=100
            self.potion_nb += 1
            self.potion_sound.play()
        
    def pause_menu(self):
        self.display_surface.fill('black')
        x,y = self.display_surface.get_size()
        x_pos = x // 2
        y_pos = y // 10 *4
        self.title_button = Buttons('../graphics/buttons/title/1.png', x_pos, y_pos, '', 'title', x // 2.5, y //10, 'ok', 'menu_button','../graphics/buttons/title/2.png' )
        y_pos += y // 10 * 2
        self.continue_button = Buttons('../graphics/buttons/continue/1.png', x_pos, y_pos, '', 'continue',x // 2.5, y //10, 'ok', 'menu_button', '../graphics/buttons/continue/2.png' )
        self.ui.button_list.append(self.title_button)
        self.ui.button_list.append(self.continue_button)
                                                                                             
    def run(self):        #update et crere le monde     
        if not self.game_paused:
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()
            self.check_player_death()                
            self.change_salle()
            self.trader_update()
        if not self.pause:
            self.visible_sprites.draw(self.display_surface)
            self.check_win()
            self.cooldowns_verif()
            self.potion_update()
            self.check_key_collision()
            self.ui.show_coins(self.player.coin, 'coin')
            self.ui.show_coins(self.player.gem, 'gem')
            self.ui.display(self.player)
        
        if self.is_trading:
            if self.val == 7:
                self.on_menu = True
                self.ui.trade_menu()
            if self.val == 2 or self.val == 5:
                self.ui.player_speech()
            if self.val != 2 and self.val != 5 and self.val != 7:
                self.ui.trader_speech()   
            self.ui.show_coins(self.player.coin, 'coin')
            self.ui.show_coins(self.player.gem, 'gem')
                    
class Enemy_update(pygame.sprite.Group): #classe expres pour l'udate de l'ennemi (pas trouvé d'autre moyen) 
    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy']   
        for enemy in enemy_sprites:
            enemy.enemy_update(player)