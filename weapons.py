import pygame, math
from pygame.locals import *
from assets import IMAGES
from random import randint, choice
import player, weapons, level, template

class Weapon:
    def __init__(self, name, user, attack_cd, damage, special_ability, colour):
        
        self.user = user 
        self.user.weapon = self
        
        self.name = name
        
        self.colour = colour
        
        self.attacked = False
        
        tools = template.Image_tools() 
        
        self.base_attack_cd = attack_cd
        self.attack_cd = attack_cd * self.user.multis["speed"]
        self.next_attack = pygame.time.get_ticks() + attack_cd
        self.eligible_for_attack = False
        
        self.base_anim_speed = attack_cd // 1.5
        self.anim_speed = self.base_anim_speed * self.user.multis["speed"]
        self.next_anim = pygame.time.get_ticks() + self.anim_speed
        self.index = 0 
        self.index_max = IMAGES["weapons"][self.name]
        self.image =  IMAGES["weapons"][self.name][0]
        
        if self.name == "axe" or self.name == "fists":
            self.images = {
                "right": self.image ,
                "left" : tools.flip_x(self.image),
                "up" : tools.rotate(90,self.image),
                "down" : tools.rotate(-90,self.image),
            }
        if self.name == "sword":
            self.images = {
                "up": self.image ,
                "left" : tools.rotate(90,self.image),
                "down" : tools.rotate(180,self.image),
                "right" : tools.rotate(-90,self.image),
            }
        
        
        self.pos = pygame.math.Vector2(self.user.rect.center )
        
        self.image = self.index_max[self.index]
        self.rect = self.image.get_rect(center=self.pos)
        
        self.base_dmg = damage 
        self.damage = self.base_dmg * self.user.multis["melee"]
        
        self.attacking = self.user.animation == "punch"
        self.ultimating = self.user.animation == "throw"
        self.attack_add_y = 0
        self.attack_add_x = 0
        
        self.stop_attack = False
        
        self.buff = False
        
        self.rotation = 0
        
        self.set_to_zero = False
        self.rotated = False
        
        self.next_regen = pygame.time.get_ticks() + 2000
        
    def update(self, scroll, screen):
        time_now = pygame.time.get_ticks()
        
        self.attacking = self.user.animation == "punch"
        self.ultimating = self.user.animation == "throw"
        
        self.regenerate()
        
        if self.name == "axe" or self.name == "fists":
            self.positions = {
                "right" :  (self.user.rect.center[0] +7 , self.user.rect.center[1] - 40),
                "left" : (self.user.rect.center[0] -40  , self.user.rect.center[1] - 40),
                "up" :  (self.user.rect.center[0] -47  , self.user.rect.center[1] - 40),
                "down" : (self.user.rect.center[0]-20  , self.user.rect.center[1] + 5 ),
            }
        if self.name == "sword":
            self.positions = {
                "right" :  (self.user.rect.center[0] +7   , self.user.rect.center[1] -12),
                "left" : (self.user.rect.center[0] -55  , self.user.rect.center[1] - 10),
                "up" :  (self.user.rect.center[0] -10  , self.user.rect.center[1] - 55),
                "down" : (self.user.rect.center[0]-10  , self.user.rect.center[1] + 5 ),
            }
        if not self.stop_attack:
            self.image = self.images[self.user.ori]
            self.rotated = False
            self.attack_add_y = 0
            self.attack_add_x = 0
        else:
            if not self.rotated or self.user.changed_ori:
                self.image = self.images[self.user.ori]
                
                if self.name == "axe":
                    if self.user.ori == "right":
                        self.image = template.Image_tools.rotate(template.Image_tools, -45, self.image)
                    if self.user.ori == "up":
                        self.image = template.Image_tools.rotate(template.Image_tools, -45, self.image)
                        self.attack_add_y =-35
                    if self.user.ori == "down":
                        self.image = template.Image_tools.rotate(template.Image_tools, -45, self.image)
                        self.attack_add_x = -10
                    if self.user.ori == "left":
                        self.image = template.Image_tools.rotate(template.Image_tools, 45, self.image)
                        self.attack_add_x = -30
                        
                if self.name == "sword":
                    if self.user.ori == "right":

                        self.attack_add_x = 20
                    if self.user.ori == "up":
                        self.attack_add_y =-25
                    if self.user.ori == "down":
                        self.attack_add_y = 10
                    if self.user.ori == "left":
                        self.attack_add_x = -20
                        
                self.rotated = True
        
        self.x,self.y = self.positions[self.user.ori][0] + self.attack_add_x, self.positions[self.user.ori][1]+self.attack_add_y
        
        self.eligible_for_attack = time_now > self.next_attack 
        
        self.rect = self.image.get_rect(topleft=(self.x,self.y))
        
        screen.blit(self.image, (self.rect.x,self.rect.y))

        
    def regenerate(self):
        if pygame.time.get_ticks() > self.next_regen:
            self.user.hp += 1
            self.next_regen += pygame.time.get_ticks() + 2000
            
            if self.user.hp > self.user.max_hp:
                self.user.hp = self.user.max_hp
            print("regen")
    
    def do_anim(self):
        time_now = pygame.time.get_ticks()
        
        if time_now > self.next_anim:
            if self.rotation < -60:
                self.set_to_zero = False
                self.rotation = 0
            else:
            
                self.next_anim = time_now + self.anim_speed
        
        
        
        