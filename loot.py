import pygame, math
from pygame.locals import *
from assets import IMAGES
from random import randint, choice
from ui import write
import player, weapons, level, template

class Chest(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = IMAGES["loot"]["chest"]
        self.rect = self.image.get_rect(center=pos)
        self.items = [PowerUp(
            
            pos,
            choice(["melee","agile","speed"]),
            20,
            0.8
            
            )]
        self.sx,self.sy = pos
        
    def update(self, camera):
    
        #self.x,self.y = self.rect.center 
        self.x = self.sx - camera.scroll[0]
        self.y = self.sy - camera.scroll[1]
        self.rect = self.image.get_rect(center=(self.x,self.y))
        
        self.items = [PowerUp(
            
            (self.sx,self.sy),
            choice(["melee","agile","speed","speed"]),
            .10,
            0.3
            
            )]
        
    def spawn_item(self, item_group):
        self.kill()
        item_group.add(choice(self.items))
        
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, pos, stat_increase, increase,velocity):
        pygame.sprite.Sprite.__init__(self)
        self.stat = stat_increase
        self.increase = increase
        self.vulnerable = False
        self.time_to_vuln = pygame.time.get_ticks() + 500
        
        self.coin_pickup = False
        
        self.pos = pos
        
        self.image = IMAGES["loot"][self.stat]
        self.rect = self.image.get_rect(center=pos)
        
        self.velocity = pygame.math.Vector2(0,velocity)
        
        self.x = self.pos[0]
        self.y = self.pos[1]   
        
        self.position = pygame.math.Vector2(self.x,self.y)     
        
    def update(self, camera, dt):
        
        if not self.vulnerable:
            if pygame.time.get_ticks() > self.time_to_vuln:
                self.vulnerable = True
        
        self.position += self.velocity * dt
        
        
        
        self.x = self.position[0] - camera.scroll[0]
        self.y = self.position[1] - camera.scroll[1]
        

        
        self.velocity = self.velocity.move_towards((0,0), 0.001)
        
        self.rect = self.image.get_rect(center=(self.x,self.y))
        
class Pickup(pygame.sprite.Sprite):
    def __init__(self, pos, amount, vel, scroll):
        pygame.sprite.Sprite.__init__(self)
        
        print("created")
        
        self.image = template.Image_tools.get_bigger(template.Image_tools, IMAGES["loot"]["coin"], 2)
        self.rect = self.image.get_rect(center=pos)
        
        self.x,self.y = pos[0] + scroll[0], pos[1] + scroll[1]
        
        self.position = pygame.math.Vector2(self.x,self.y)
        self.velocity = pygame.math.Vector2(vel)
        
        self.coin_pickup = False
        
        self.vulnerable = False
        
        self.time_to_vuln = pygame.time.get_ticks() + 500
        
        self.amount = amount
        
    def update(self, camera, dt):
        
        if not self.vulnerable:
            if pygame.time.get_ticks() > self.time_to_vuln:
                self.vulnerable = True
                print("pickup now")
        
        self.position += self.velocity * dt
        
        self.velocity = self.velocity.move_towards((0,0), 0.01)
        
        cam_scroll = pygame.math.Vector2(camera.scroll)
        
        self.image = IMAGES["loot"]["coin"]
        
        self.rect.center =self.position-cam_scroll # = self.image.get_rect(center=(self.position-cam_scroll))
        
        
        
class Proceed_Block:
    def __init__(self, pos):
        self.rect = pygame.Rect(pos[0],pos[1], 200,200)
        self.pos = pos
    def update(self, scroll, screen):
        
        self.rect = pygame.Rect(self.pos[0]-100-scroll[0], self.pos[1]-100-scroll[1], 200,200)

        pygame.draw.rect(screen, (255,255,255), self.rect)
        write(screen, "Next",(self.pos[0]-50-scroll[0], self.pos[1]-50-scroll[1]) , font=pygame.font.Font("Minecraft.ttf", 40))
        write(screen, "Level",(self.pos[0]-50-scroll[0], self.pos[1]+10-scroll[1]) , font=pygame.font.Font("Minecraft.ttf", 40))