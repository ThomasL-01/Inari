import pygame
from os import walk
from csv import reader

def import_folder(path):    #importe des fichiers et les parcours (pour trouver les imgs des animations)
    surface_list = []
    for _, __, filenames in walk(path): #Ou A et B sont des infos obligatoires mais inutiles
        for image in filenames:
            if image.endswith('png'):
                full_path = path + "/" + image
                image_surf = pygame.image.load(full_path).convert_alpha()
                surface_list.append(image_surf)
            
    return surface_list 

def import_csv_dispo(path):     #pour que les .csv soient vus comme des maps
    terrain_map = []
    with open(path) as level_map :
        layout = reader(level_map, delimiter = ',')
        for raw in layout:
            terrain_map.append(list(raw))
        return terrain_map

