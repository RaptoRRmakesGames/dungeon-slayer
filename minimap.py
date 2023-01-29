import pygame, math
from pygame.locals import *
from assets import IMAGES
import player, weapons, level, enemies, cam

class Minimap:
    def __init__(self, scale, player, room_list):
        self.border = pygame.Surface((170,170))
        self.surface = pygame.Surface((157,157))
        self.scale = scale  
        
        self.player = player
        self.rooms = []
        self.room_list = room_list
        for room in room_list:
            self.rooms.append(pygame.Rect(room.rect.x/scale,room.rect.y/scale,room.image.get_width()/scale, room.image.get_height()/scale))
        
    def update(self,screen,scroll):
        
        self.surface.fill((255,255,255))
        self.border.fill((119,207,177))
        
        for room in self.rooms:
            pygame.draw.rect(self.surface,(0,0,0) ,room)
        
        pygame.draw.circle(self.surface, (119,207,177), (self.player.x//self.scale ,self.player.y//self.scale), 120/self.scale)
        screen.blit(self.border, (10,10))
        
        screen.blit(self.surface, (15,15))    