import pygame, math
from pygame.locals import *
from assets import IMAGES
from random import randint, uniform, choice
import player, weapons, level, enemies, cam,minimap , loot

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, ranged, damage, speed, enemy, room, plr, hp):
        pygame.sprite.Sprite.__init__(self)
        
        self.enemy = enemy 
        
        self.animation = "run"
        
        self.ori = "right"
        self.image = IMAGES["enemies"][enemy][self.ori]["attack"][0]
        self.rect = self.image.get_rect(center=pos)
        self.index = 0
        self.index_max = len(IMAGES["enemies"][self.enemy][self.ori]["run"])
        self.position = pygame.math.Vector2(pos) 
        self.velocity = pygame.math.Vector2(0,0)
        self.moving = False
        self.max_vel = 0.2
        self.speed = speed
        self.ranged = ranged 
        self.dmg = damage
        self.anim_rate = 150 * uniform(1.1,1.4)
        self.next_anim = pygame.time.get_ticks() + self.anim_rate
        self.hp = hp
        
        self.start_x = pos[0]
        self.start_y = pos[1]
        
        self.took_dmg = True
        self.next_take_dmg = pygame.time.get_ticks() + 1500
        
        self.move_rate = 2500 + randint(0,100)
        self.next_move = pygame.time.get_ticks() + self.move_rate 
        self.player = plr 
        
        self.hold_time = 600
        
        self.holding = 0
        
        self.can_dmg = False
        
        self.saw_plr = False
        
        
    def update_dmg(self, dt):

        self.took_dmg = True
        
        if self.holding > self.hold_time:
            self.can_dmg = True
            self.holding = 0
            
    def update(self, camera, dt):
        self.center()
        
        self.update_dmg(dt)
        
        self.index_max = len(IMAGES["enemies"][self.enemy][self.ori][self.animation])
        
        self.move(dt)
        
        cam_scroll = pygame.math.Vector2(camera.scroll)
        self.rect = self.image.get_rect(center=(self.position - cam_scroll))
        
    def move(self, dt):
        
        self.distance_to_player = self.position.distance_to(self.player.position)
        
        time_now = pygame.time.get_ticks()
        
        if self.distance_to_player < 400 or self.saw_plr: # ---> Code for when player is in room
            self.saw_plr = True
            
            #print("saw plr", end=" ")
            if self.moving:
                if time_now > self.next_move:
                    self.moving = False
                    self.next_move = time_now + 1500
            else:
                if time_now > self.next_move - 750:
                    self.moving = True
                    self.next_move = time_now + 1500
            
            if self.moving:
                #print("go to pl")
                self.position += (self.position.move_towards(self.player.position, self.speed) - self.position ) * dt
                self.position += self.velocity
                self.velocity = self.velocity.move_towards((0,0), 0.1)
                self.speed += .1
                if self.speed > self.max_vel:
                    self.speed = self.max_vel

        
        else:# ---> Code for when player aint in room (probably gonna be a fuck around and find out ai)
            self.moving = False
            
        self.position += self.velocity * dt
        self.velocity = self.velocity.move_towards((0,0), 0.1)
                        

        #if self.moving or self.attacking:
        if self.animation == "run":
            if self.moving:
                self.do_anim()
                
            else:
                self.index = 0
        else:
            self.do_anim()
        self.do_anim()
    def do_anim(self):
        
        self.index_max = len(IMAGES["enemies"][self.enemy][self.ori][self.animation])

        if pygame.time.get_ticks() > self.next_anim:
            self.index += 1   
            if self.index > self.index_max-1:
                self.index = 0

            self.next_anim = pygame.time.get_ticks() + self.anim_rate
            
        self.anim_done = (self.index == self.index_max)

        if self.image is not IMAGES["enemies"][self.enemy][self.ori][self.animation][self.index]:
            self.image = self.image = IMAGES["enemies"][self.enemy][self.ori][self.animation][self.index]
            
    def center(self):
        x,y = self.position[0], self.position[1]
        
        if x > self.start_x + 480:    
            self.position = pygame.math.Vector2(self.start_x,self.start_y)
        if x < self.start_x - 480:    
            self.position = pygame.math.Vector2(self.start_x,self.start_y)
            
        if y > self.start_x + 480:    
            self.position = pygame.math.Vector2(self.start_x,self.start_y)
        if y < self.start_x - 480:    
            self.position = pygame.math.Vector2(self.start_x,self.start_y)