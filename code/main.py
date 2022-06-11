import sys
from tkinter import *

import pygame

from level import *
from settings import *

sound_volume = 50
class Game():
    def __init__(self, utilisateur, mdp, current_salle, vie, boss, s_purp, s_green, s_red, pot_3, po_14, pot_nb,coin,gem,p_stock,strength_stock,stamina_stock,health_stock,speed_stock,res_stock):
        #Récupération des données de l'utilisateur
        self.utilisateur = utilisateur
        self.salle = current_salle
        self.boss = boss
        self.s_purp = s_purp
        self.s_red = s_red
        self.vie = vie
        self.s_green = s_green
        self.mdp = mdp
        self.pot_3 = pot_3
        self.pot_14 = po_14
        self.pot_nb = pot_nb
        self.coin = coin
        self.gem = gem
        self.height = screen_height
        self.width = screen_width
        self.can_hit_button = True
        self.start_cooldown = None
        self.max_val = 7
        self.on_menu = False
        self.p_stock = int(p_stock)
        self.strength_stock = int(strength_stock)
        self.stamina_stock = int(stamina_stock)
        self.health_stock = int(health_stock)
        self.speed_stock = int(speed_stock)
        self.res_stock = int(res_stock)
        
            
        #creer la fenetre 
        pygame.init()       #création de la fenêtre
        pygame.mixer.music.load('../sounds/music.mp3')
        pygame.mixer.music.play(loops=-1)
        self.screen = pygame.display.set_mode((self.width,self.height), pygame.RESIZABLE)
        image = pygame.image.load('../graphics/autres/logo.gif')  
        pygame.display.set_icon(image)
        pygame.display.set_caption('INARI')
        self.clock = pygame.time.Clock()
        self.tile_size = self.screen.get_height() // 15
        
        self.trade_sound = pygame.mixer.Sound('../sounds/Trade.mp3')
        self.speech_sound = pygame.mixer.Sound('../sounds/Villager.mp3')
        
        #Prépare le level
        self.level = Level(self.mdp, self.salle, self.utilisateur, self.vie, self.boss, self.s_purp, self.s_green, self.s_red, self.pot_3, self.pot_14, self.pot_nb, self.coin, self.gem, self.tile_size, sound_volume)
        self.salle = self.level.current_salle

        for stock in range (4-int(strength_stock)):
            player_stats['damage'] += 20/100 * player_stats['damage']
            self.level.player.damage = player_stats['damage']
        for stock in range(3-int(stamina_stock)):
            if player_stats['stamina'] + 20/100 * player_stats['stamina'] > player_stats['max_stamina']:
                player_stats['stamina'] = player_stats['max_stamina']
            else:
                player_stats['stamina'] += 20/100 * player_stats['stamina']
            self.level.player.stamina = player_stats['stamina']
            stamina_bar_width = player_stats['stamina'] * 0.8
            self.level.ui.stamina_bar_rect = pygame.Rect(40,40,stamina_bar_width,bar_height) 
        for stock in range(4-int(health_stock)):
            if player_stats['health'] + 20/100 * player_stats['health'] > player_stats['max_health']:
                player_stats['health'] = player_stats['max_health'] 
            else:
                player_stats['health'] += 20/100 * player_stats['health']
            health_bar_width = player_stats['health'] *2  #largeur barre de vie
            self.level.ui.health_bar_rect = pygame.Rect(30,10,health_bar_width,bar_height) 
        for stock in range(4-int(speed_stock)):
            player_stats['speed'] += 20/100 * player_stats['speed']
            self.level.player.speed =  player_stats['speed']
        for stock in range(2-int(res_stock)):
            mob_data['skeleton']['damage'] -= 20/100 * mob_data['skeleton']['damage']
            mob_data['boss']['damage'] -= 20/100 * mob_data['boss']['damage']
            
        if self.strength_stock < 4 or self.stamina_stock < 3 or self.health_stock < 4 or self.p_stock < 5 or self.speed_stock < 4 or self.res_stock < 2:
            self.max_val = 9
            self.level.val = 9
            self.level.ui.val = 9
                       
    def run(self):  #Lance tout le jeu

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    # système de sortie du jeu lorsque l'on ferme la fenêtre
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h),pygame.RESIZABLE)
                #print(player_stats['health'], self.level.player.health, player_stats['stamina'],  self.level.player.stamina, player_stats['damage'], self.level.player.damage)
                
                if event.type == pygame.MOUSEBUTTONDOWN and self.level.ui.button_list != []:
                    for button in self.level.ui.button_list:
                        action = button.check_input(pygame.mouse.get_pos())
                        if self.can_hit_button and action != None:                            
                            self.start_cooldown = pygame.time.get_ticks()
                            
                            if action == 'continue':
                                self.level.game_paused = False
                                self.level.pause = False
                                pygame.mixer.music.unpause()
                                self.level.pause_sound_statut = True
                            if action == 'title':
                                pygame.mixer.music.stop()
                                pygame.mixer.music.load('../sounds/intro.mp3')
                                pygame.mixer.music.play()
                                menu_principal()
                                pygame.quit()
                                sys.exit()

                            if action == 'potion' and self.level.player.coin >= 20 and self.p_stock> 0:
                                self.level.potion_nb += 1
                                self.level.player.coin -= 20
                                self.p_stock-=1
                                self.level.potion_sound.play()
                                self.trade_sound.play()
                            if action == 'strenght' and self.level.player.gem >= 5 and player_stats['damage'] < player_stats['max_damage'] and self.strength_stock>0:
                                if player_stats['damage'] + 20/100 * player_stats['damage'] > player_stats['max_damage']:
                                    player_stats['damage'] = player_stats['max_damage']
                                else:
                                    player_stats['damage'] += 20/100 * player_stats['damage']
                                self.level.player.damage = player_stats['damage']
                                self.level.player.gem -= 5
                                self.strength_stock -=1
                                self.level.potion_sound.play()
                                self.trade_sound.play()
                             
                            if action == 'stamina' and self.level.player.gem >= 5 and player_stats['stamina'] < player_stats['max_stamina'] and self.stamina_stock>0:
                                if player_stats['stamina'] + 20/100 * player_stats['stamina'] > player_stats['max_stamina']:
                                    player_stats['stamina'] = player_stats['max_stamina']
                                else:
                                    player_stats['stamina'] += 20/100 * player_stats['stamina']
                                self.level.player.stamina = player_stats['stamina']
                                self.level.player.gem -= 5
                                stamina_bar_width = player_stats['stamina'] * 0.8
                                self.level.ui.stamina_bar_rect = pygame.Rect(40,40,stamina_bar_width,bar_height) 
                                self.stamina_stock -= 1
                                self.level.potion_sound.play()
                                self.trade_sound.play()
                             
                            if action == 'health' and self.level.player.gem >= 10 and player_stats['health'] < player_stats['max_health'] and self.health_stock>0:
                                if player_stats['health'] + 20/100 * player_stats['health'] > player_stats['max_health']:
                                    player_stats['health'] = player_stats['max_health'] 
                                else:
                                    player_stats['health'] += 20/100 * player_stats['health']
                                self.level.player.health =  player_stats['health']
                                self.level.player.gem -= 10
                                health_bar_width = player_stats['health'] *2  #largeur barre de vie
                                self.level.ui.health_bar_rect = pygame.Rect(30,10,health_bar_width,bar_height) 
                                self.health_stock -=1
                                self.level.potion_sound.play()
                                self.trade_sound.play()
                             
                            if action == 'speed' and self.level.player.coin >= 30 and player_stats['speed'] < player_stats['max_speed'] and self.speed_stock>0:
                                if player_stats['speed'] + 20/100 * player_stats['speed'] > player_stats['max_speed']:
                                    player_stats['speed'] = player_stats['max_speed']
                                else:
                                    player_stats['speed'] += 20/100 * player_stats['speed']
                                self.level.player.speed =  player_stats['speed']
                                self.level.player.coin -= 30
                                self.speed_stock -=1
                                self.level.potion_sound.play()
                                self.trade_sound.play()
                             
                            if action == 'res' and self.level.player.gem >= 15 and self.res_stock>0:
                                mob_data['skeleton']['damage'] -= 20/100 * mob_data['skeleton']['damage']
                                mob_data['boss']['damage'] -= 20/100 * mob_data['boss']['damage']
                                self.level.player.gem -= 15
                                self.res_stock -= 1
                                self.level.potion_sound.play()
                                self.trade_sound.play()
                            
                            if action == 'close':
                                self.max_val = 9
                                self.level.on_menu =False

                                
                            self.can_hit_button =False
            
                if event.type == pygame.MOUSEBUTTONDOWN and self.level.is_trading and self.level.val < self.max_val and not self.level.on_menu:
                    
                    #self.speech_sound.play()
                    if self.level.val == 8:
                        self.level.game_paused = False
                        self.level.pause = False
                        self.level.can_collide_trader = False
                        self.level.is_trading = False
                        self.level.player.can_get_input = True
                        self.level.start_coll = pygame.time.get_ticks()
                    self.level.val += 1
                    self.level.ui.val += 1
                
                if event.type == pygame.MOUSEBUTTONDOWN and self.level.is_trading and self.level.val == self.max_val :
                    self.level.val = 7
                    self.level.ui.val = 7
                
                if event.type == pygame.MOUSEBUTTONDOWN and self.level.is_trading and not self.level.on_menu:
                    self.speech_sound.play()

                    
            self.screen.fill((0,23,31)) # creation de la fenètre
            
            current_time = pygame.time.get_ticks()
            if self.can_hit_button ==False:
                if current_time - self.start_cooldown >= 500:
                    self.can_hit_button = True
            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_s] and self.level.save_statut:
                self.level.save_statut = False
                self.level.save_cooldown_start = pygame.time.get_ticks()
                sauvegarde(self.utilisateur, self.mdp, int(self.level.current_salle), self.level.player.health , 
                           self.level.boss_statut, self.level.purp_statut, self.level.green_statut, self.level.red_statut, 
                           self.level.potion_statut_3, self.level.potion_statut_14, self.level.potion_nb, self.level.player.coin, 
                           self.level.player.gem,self.p_stock,self.strength_stock ,self.stamina_stock,self.health_stock,
                           self.speed_stock,self.res_stock, 'csvfile.csv')
        
                    
            if self.level.current_salle == 14:  #Stop la musique pour la salle 14
                pygame.mixer.music.stop()
                
            if self.level.pause:
                self.screen.fill('black')
                texte = pygame.font.SysFont(ui_font, 75).render('  PAUSE', 1 , '#0344FF')
                self.screen.blit(texte, (self.width // 5 * 2.05, 100)) 
                pygame.mixer.music.pause()     
                
                
            if self.salle == 14 and self.level.current_salle != 14: #Vérification pour rejouer la musique du laby
                pygame.mixer.music.play()
                
            if self.salle != self.level.current_salle:  #Change la valeur de la salle dans Game par rapport a celle de Level (1 de décalage)
                self.salle = self.level.current_salle
        
            if self.level.win_statut == 'Win':  #Créer la fenetre de win 
                pygame.mixer.music.stop()
                you_win(self.utilisateur, self.mdp, self.s_purp, self.s_green, self.s_red, self.pot_3, self.pot_14)
                pygame.quit()
                sys.exit()
                
            if self.level.win_statut == 'Game over':#Créer la fenetre de Game Over
                pygame.mixer.music.stop()
                game_over(self.utilisateur, self.mdp)
                pygame.quit()
                sys.exit()
        
            #Lance le level
            self.level.run()
            if self.level.ui.button_list != []:
                for bouton in self.level.ui.button_list:
                    if bouton.action == 'potion' and self.p_stock == 0:
                        bouton.text_input = 'Épuisé'
                        bouton.text = bouton.police.render(bouton.text_input, True, 'white')
                        bouton.change_statut()

                    if bouton.action == 'strenght' and self.strength_stock == 0:
                        bouton.text_input = 'Épuisé'
                        bouton.text = bouton.police.render(bouton.text_input, True, 'white')
                        bouton.change_statut()
                    if bouton.action == 'stamina' and self.stamina_stock == 0:
                        bouton.text_input = 'Épuisé'
                        bouton.text = bouton.police.render(bouton.text_input, True, 'white')
                        bouton.change_statut()
                    if bouton.action == 'speed' and self.speed_stock == 0:
                        bouton.text_input = 'Épuisé'
                        bouton.text = bouton.police.render(bouton.text_input, True, 'white')
                        bouton.change_statut()
                    if bouton.action == 'res' and self.res_stock == 0:
                        bouton.text_input = 'Épuisé'
                        bouton.text = bouton.police.render(bouton.text_input, True, 'white')
                        bouton.change_statut()
                    if bouton.action == 'health' and self.health_stock == 0:
                        bouton.text_input = 'Épuisé'
                        bouton.text = bouton.police.render(bouton.text_input, True, 'white')
                        bouton.change_statut()
                    bouton.update()
                    bouton.change_color(pygame.mouse.get_pos())
            
            self.level.coin_nb = self.level.player.coin
            self.level.gem_nb = self.level.player.gem
            pygame.display.update()
            self.clock.tick(FPS) # regle les FPS a 60/sec            
       
def game_over(pseudo, mdp): #Fonction pour afficher le menu game over
    pygame.mixer.init()
    Go = Tk()
    Go.geometry("3840x2160")
    Go.title("GAME OVER")
    Go.minsize(480, 360)
    Go.config(bg = 'black')
    lose_music = pygame.mixer.Sound('../sounds/Game Over.mp3')
    nouvelle_sauvegarde(pseudo, mdp, 3,100,'alive','locked','locked','locked', 'on ground', 'on ground', 0, 0, 0,5,4,3,4,4,2)
        

    can = Canvas(Go, width= 3140, height= 2160, bg = "black", bd = 0, highlightthickness=0) #creation du fond d'écran
    img = PhotoImage(file= "../graphics/autres/game_over.gif")
    can.create_image(0,0, anchor= NW, image = img)
    can.place(x=-40,y=30)
    
    frame = Frame(Go, bg= 'black')#Frame pour les boutons réesaayer
        
    def retry():    #fonction pour relancer le jeu
        Go.destroy()
        recup = recup_sauvegarde(pseudo, 'csvfile.csv')
        game = Game(recup[0],recup[1], recup[2],recup[3],recup[4],
                    recup[5],recup[6], recup[7], recup[8], recup[9], 
                    recup[10], recup[11], recup[12], recup[13], recup[14], 
                    recup[15], recup[16], recup[17], recup[18])
        game.run()
        
    label_titel = Label(frame, text = "Réessayer ?", font = ("Helvetica", 30), fg='white', bg='black')
    label_titel.pack(pady=5)
    recommencer_button = Button(frame, text=('Recommencer'), font = ("Helvetica", 30), fg='black', bg='white', command= retry)
    recommencer_button.pack(fill=X, pady=10)
                
    #Bonton quitter en bas
    btn_quitter = Button(Go, text="QUITTER", bg="white", fg="black", command=Go.destroy)
    btn_quitter.pack(side=BOTTOM, fill=X)
    frame.pack(side=TOP)    
    lose_music.play()
    Go.mainloop()
         
def you_win(pseudo, mdp, s1, s2, s3, pot_3, pot_14):  #Fonction pour afficher le menu de victoire
    pygame.mixer.init()
    win = Tk()
    win.geometry("3840x2160")
    win.title("CONGRATULATIONS")
    win.minsize(480, 360)
    win.config(bg = 'black')
    win_music = pygame.mixer.Sound('../sounds/stage_clear.wav')
    nouvelle_sauvegarde(pseudo, mdp, 36, 100,'dead',s1, s2, s3, pot_3, pot_14, 200, 1000, 100,5,4,3,4,4,2)
        
    can = Canvas(win, width= 3140, height= 2160, bg = "black", bd = 0, highlightthickness=0)#background
    img = PhotoImage(file= "../graphics/autres/congratulations.gif")
    can.create_image(0,0, anchor= NW, image = img)
    can.place(x=-80,y=-20)
    
    frame = Frame(win, bg= 'black')
    label_titel = Label(frame, text = " VOUS AVEZ TROUVÉ LA SORTIE ! FÉLICITATIONS", font = ("Helvetica", 20), fg='white', bg='black')
    label_titel.pack(pady=5)
    
    btn_quitter = Button(win, text="QUITTER", bg="white", fg="black", command=win.destroy)
    btn_quitter.pack(side=BOTTOM, fill=X)
    frame.pack(side= BOTTOM, fill=X)
        
    win_music.play()    #Joue le son de victoire
    win.mainloop()
           
def menu_principal():   #genere le menu principal
    #creation de la fenetre
    window = Tk()
    window.geometry("3840x2160")
    window.title("Inari et le Labyrinthe de l'Infini")
    window.minsize(480, 360)
    window.config(background = "black")

    #creation du fond 
    can = Canvas(window, width=3840, height=2160, bg = "black", bd = 0, highlightthickness=0)
    img = PhotoImage(file= "../graphics/autres/logo.gif")
    can.create_image(0,0, anchor= NW, image = img)
    can.place(x=75,y=-300)

    frame = Frame(window, bg='black')
    settings_frame = Frame(window, bg = 'black')

    #creation du sous-titre
    soustitre = Label(frame, text= "ET LE  LABYRINTHE  DE L'INFINI", font= ("../graphics/autres/ARCADEPI.TTF", 40), bg = "black", fg = "white")
    soustitre.pack()

    #creation des boutons
    image_nouveau_button =PhotoImage(file='../graphics/autres/nouveau.gif').subsample(3)
    nouveau_button = Button(frame, text = "NOUVEAU (Si tu vas sur charger jte donne tout", image=image_nouveau_button, command = double_fonction(window.destroy, menu_nouveau))
    nouveau_button.pack()
    image_charger_button =PhotoImage(file='../graphics/autres/charger.gif').subsample(3)
    charger_button = Button(frame, text = "Gouloum: pseudo: Thomas /Mot de passe: totodu01", image= image_charger_button, command= double_fonction(window.destroy, menu_charger))
    charger_button.pack(pady=2)
    settings_image = PhotoImage(file = '../graphics/settings.gif').subsample(3)
    settings_button = Button(settings_frame, image = settings_image, command = double_fonction(window.destroy, menu_settings))
    settings_button.pack()

    #creation bouton quitter
    btn_quitter = Button(window, text="QUITTER", bg="white", fg="black", command=window.destroy)
    btn_quitter.pack(side=BOTTOM, fill=X)

    frame.pack(side=BOTTOM)
    settings_frame.pack(side = TOP, anchor=NE)
    window.mainloop()

def menu_charger():     #genere le menu pour charger un utilisateur
    #creation de la fenetre
    window1 = Tk()
    window1.title("Charger")
    window1.geometry("3840x2160")
    window1.config(background = "black")

    frame = Frame(window1, background="black")

    #creation d'image
    height = 512
    width = 700
    image = PhotoImage(file="../graphics/autres/cadenas.png", master=window1).zoom(1)
    canvas = Canvas(frame, width=width, height=height, bg="black", bd=0, highlightthickness=0 )
    canvas.create_image(width/2, height/2, image= image)
    canvas.grid(row =0, column=0, sticky=W)

    #creer une sous-boite
    right_frame = Frame(frame, bg='black')

    #creer le texte
    label_titel = Label(right_frame, text = "Veuillez vous identifier:", font = ("Helvetica", 20), bg = 'black', fg='white')
    label_titel.pack(pady=5)
    label_pseudo = Label(right_frame, text = "Votre Pseudo:", font = ("Helvetica", 20),bg = 'black', fg='white')
    label_pseudo.pack()

    #creer les champs/inputs
    pseudo_joueur = Entry(right_frame,font = ("Helvetica", 20), bg="black", fg='white', insertbackground='white')
    pseudo_joueur.pack(fill=X, pady=10)
    label_mdp = Label(right_frame, text = "Mot de Passe:", font = ("Helvetica", 20), bg="black", fg='white')
    label_mdp.pack()
    mdp_joueur = Entry(right_frame,font = ("Helvetica", 20),bg ='black', fg='white', insertbackground='white')
    mdp_joueur.pack(fill=X, pady= 10)
    erreur_text = Label(right_frame, text="Je peux mettre ce que je veux on le verra pas", font = ("Helvetica", 20), bg="black", fg='black')
    erreur_text.pack(pady=2)

    def entry():#systeme de verification d'une sauvegarde à charger
        pseudo = pseudo_joueur.get()
        mdp = mdp_joueur.get()
        erreur = verif_sauvegarde(pseudo, mdp, 'csvfile.csv')
        if erreur == True:
            erreur_text.config(fg='red', text= "Le nom d'utilisateur ou mot de passe est incorrect !")
            erreur_text.pack(pady=2)
        elif erreur == False:
            window1.destroy()
            pygame.mixer.music.stop()
            if __name__ == '__main__':
                recup = recup_sauvegarde(pseudo, 'csvfile.csv') 
                game = Game(recup[0],recup[1], recup[2],recup[3],recup[4],
                            recup[5],recup[6], recup[7], recup[8], recup[9], 
                            recup[10], recup[11], recup[12], recup[13], recup[14], 
                            recup[15], recup[16], recup[17], recup[18])
                game.run()

    #creation bouton "entrer"
    entrer_button = Button(right_frame, text= 'Entrer',font = ("Helvetica", 20), command=entry)
    entrer_button.pack(pady=10)

    #sous boite a droite de la frame
    right_frame.grid(row=0, column=1, sticky=W)
    
    #afficher la frame
    frame.pack(expand=YES)

    #afficher la fenetre + le bouton quitter
    btn_quitter = Button(window1, text="MENU PRINCIPAL", bg="white", fg="black", command=double_fonction( window1.destroy, menu_principal))
    btn_quitter.pack(side=BOTTOM, fill=X)
    window1.mainloop()

def menu_settings():
    def volume(x):
        sound_volume = volume_slider.get()
        pygame.mixer.music.set_volume(sound_volume/100)
        return sound_volume == sound_volume
        
    window = Tk()
    window.geometry("3840x2160")
    window.title("Réglages")
    window.minsize(480, 360)
    window.config(background = "black")

    frame = Frame(window, bg='black')
    volume_frame = LabelFrame(frame, text='VOLUME', font= ("../graphics/autres/ARCADEPI.TTF", 25), bg='black', fg='white', bd=0, highlightthickness=0)
    volume_frame.grid(column=0, row=0)
    
    volume_slider = Scale(volume_frame, bg='black', fg='white', orient=VERTICAL, from_=100, to=0, command=volume, length=400)
    volume_slider.set(pygame.mixer.music.get_volume()*100)
    volume_slider.pack()
    
    btn_quitter = Button(window, text="MENU PRINCIPAL", bg="black", fg="black", command=double_fonction(window.destroy, menu_principal))
    btn_quitter.pack(side=BOTTOM, fill=X)
    frame.pack(anchor=W, padx=50, pady= 100)
    window.mainloop()
    
def menu_nouveau():     #genere le menu pour creer un nouvel utilisateur
    #creation de la fenetre
    window2 = Tk()
    window2.title("Nouveau")
    window2.geometry("3840x2160")
    window2.config(background = "black")

    frame = Frame(window2, background="black")

    #creation d'image
    height = 700
    width = 700
    image = PhotoImage(file="../graphics/autres/new_user.png", master= window2).zoom(1).subsample(2)
    canvas = Canvas(frame, width=width, height=height, bg="black", bd=0, highlightthickness=0 )
    canvas.create_image(width/2, height/2, image= image)
    canvas.grid(row =0, column=0, sticky=W)

    #creer une sous-boite
    right_frame = Frame(frame, bg='black')

    #creer le texte
    label_titel = Label(right_frame, text = "Veuillez creer un compte pour jouer:", font = ("Helvetica", 20), bg="black", fg='white')
    label_titel.pack()
    label_pseudo = Label(right_frame, text = "Pseudo original:", font = ("Helvetica", 20), bg="black", fg='white')
    label_pseudo.pack()

    #creer les champs/inputs
    pseudo_joueur = Entry(right_frame,font = ("Helvetica", 20), bg="black", fg='white', insertbackground='white')
    pseudo_joueur.pack(pady=10, fill=X)
    label_mdp = Label(right_frame, text = "Mot de Passe (min 5 caractères):", font = ("Helvetica", 20), bg="black", fg='white')
    label_mdp.pack()
    mdp_joueur = Entry(right_frame,font = ("Helvetica", 20), bg="black", fg='white', insertbackground='white')
    mdp_joueur.pack(pady=10, fill=X)
    error_text = Label(right_frame, text = "Je peux mettre ce que je veux on le verra pas", font = ("Helvetica", 20), bg="black", fg='black')
    error_text.pack(pady=2)
    

    def entry(): #systeme de verification/creation d'une nouvelle sauvegarde
        pseudo = pseudo_joueur.get()
        mdp = mdp_joueur.get()
        verification = verifpseudo(pseudo, 'csvfile.csv')
        if verification == True:
            error_text.config(fg ='red', text='Ce pseudo existe déjà !')
        else:
            if len(pseudo) == 0:
                error_text.config(fg='red',  text = "Vous devez utiliser un mot de passe et un pseudo")
            elif len(mdp) < 5:
                error_text.config(fg='red', text='Le mot de passe doit faire 5 caractères minimum')
            else:
                nouvelle_sauvegarde(pseudo, mdp, 3,100,'alive','locked','locked','locked', 'on ground', 'on ground', 0,0,0,5,4,3,4,4,2)
                window2.destroy()
                pygame.mixer.music.stop()
                if __name__ == '__main__':
                    recup = recup_sauvegarde(pseudo, 'csvfile.csv') 
                    game = Game(recup[0],recup[1], recup[2],recup[3],recup[4],recup[5],recup[6], recup[7], recup[8], recup[9], recup[10], recup[11], recup[12], recup[13], recup[14], recup[15], recup[16], recup[17], recup[18])
                    game.run()       
                            
    #creation bouton "entrer"
    entrer_button = Button(right_frame, text= 'Entrer',font = ("Helvetica", 20), bg="white", command=entry)
    entrer_button.pack(pady=10)

    #sous boite a droite de la frame
    right_frame.grid(row=0, column=1, sticky=W)

    frame.pack(expand=YES)

    #afficher la fenetre + le bouton quitter
    frame.pack(expand = YES)
    btn_quitter = Button(window2, text="MENU PRINCIPAL", bg="white", fg="black", command=double_fonction(window2.destroy, menu_principal))
    btn_quitter.pack(side=BOTTOM, fill=X)
    window2.mainloop()


#Ajout du son
pygame.mixer.init()
pygame.mixer.music.load('../sounds/intro.mp3')
pygame.mixer.music.set_volume(sound_volume/100)
#lance le jeu et la musique 
pygame.mixer.music.play()
menu_principal()
