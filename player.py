import pygame, math
from pygame.locals import *
from assets import IMAGES
import player, weapons, level, enemies

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, speed, hp, max_speed, melee_multi=1,agile_multi=1):
        pygame.sprite.Sprite.__init__(self)
        
        self.ori = "right"
        self.index = 0
        self.name = "player"
        self.animation = "run"
        self.anim_rate = 160
        self.next_anim = pygame.time.get_ticks() + self.anim_rate
        self.image_path = IMAGES[self.name][self.ori][self.animation]
        self.max_index = len(self.image_path)-1
        self.anim_done = False
        self.image = IMAGES[self.name][self.ori][self.animation][self.index]
        self.rect = self.image.get_rect(center=pos)
        self.timer = 0
    
        self.go_left = range(-135,-45)
        self.go_right = range(45,135)
        self.go_down = range(-44,44)
        self.go_up = list(range(-179,-136 ) ) + list(range(135,179))
        
        self.start_max_speed = pygame.math.Vector2(max_speed,max_speed )
        self.max_speed = pygame.math.Vector2(max_speed,max_speed )
        
        self.hp = 5
        
        self.velocity = pygame.math.Vector2(0,0)
        self.position = pygame.math.Vector2(pos)
        
        self.base_friction = 0.1
        self.friction = self.base_friction
        
        self.max_hp = 5
        
        self.can_dmg = True
        
        self.stamina = 100
        
        self.shift_multi = 15
        
        self.weapon = None
        
        self.init_stats(speed, hp, melee_multi, agile_multi)
        
        self.clicked_attack = False
        self.clicked_throw = False
        
        self.x,self.y = self.rect.center
        
        self.down_rate = 10
        self.last_updated = pygame.time.get_ticks() + self.down_rate
        
        self.dmg_cooldown = 1500
        self.next_dmg = pygame.time.get_ticks()
        
        self.outside = 1
        
    def set_weapon(self, weapon):
        self.weapon = weapon 
        
        
    def check_off_screen(self):
        if self.x < 0 :
            self.position = pygame.math.Vector2(600+1100,600+1100)
        if self.y < 0:
            self.position = pygame.math.Vector2(600+1100,600+1100)
        if self.x > 3600:
            self.position = pygame.math.Vector2(600+1100,600+1100)
        if self.y > 3600:
            self.position = pygame.math.Vector2(600+1100,600+1100)
            
        if not self.can_dmg:
            if pygame.time.get_ticks() > self.next_dmg:
                self.can_dmg = True
                self.next_dmg = pygame.time.get_ticks() + self.dmg_cooldown
        
    def update(self, dt,cam):
        self.changed_ori = False
        
        self.holding_weapon = True
        self.image_path = IMAGES[self.name][self.ori][self.animation]
        self.max_index = len(self.image_path)-1

        self.controls(dt)
        self.turn(True)
        self.animate()
        self.update_stats()
        
        self.check_off_screen()
        
        self.image = IMAGES[self.name][self.ori][self.animation][self.index]
        self.x,self.y = self.position
        self.rect.x = self.x - cam.scroll[0]
        self.rect.y = self.y - cam.scroll[1]
        self.rect = self.image.get_rect(center=(self.rect.x,self.rect.y))
        
    def controls(self,dt):
        
        keys = pygame.key.get_pressed()
        
        self.moving_x = keys[pygame.K_d] or keys[pygame.K_a]
        self.moving_y = keys[pygame.K_s] or keys[pygame.K_w]

        if keys[K_LSHIFT]:
            if self.stamina > 0:
                self.shift = self.shift_multi

                self.stamina -= .04 * dt
            else:
                self.shift = 1

            self.shifting = True
            
        else:
            self.shift = 1
            
            self.stamina += .07 * dt
            self.shifting = False 
            
        if self.stamina > 100:
            self.stamina = 100
            
            
        if keys[K_d]:
            self.velocity += pygame.math.Vector2((self.speed  * self.shift) ,0)
            
        if keys[K_s]:
            self.velocity += pygame.math.Vector2(0,(self.speed  * self.shift)  )
            
        if keys[K_a]:
            self.velocity -= pygame.math.Vector2(( self.speed  * self.shift) ,0)
            
        if keys[K_w]:
            self.velocity -= pygame.math.Vector2(0,( self.speed * self.shift) )
            
        
        if self.outside and not  self.room_locked:    
        
            if self.velocity[0] > self.max_speed[0]:
                self.velocity[0] = self.max_speed[0]
            if self.velocity[0] < self.max_speed[0] * -1:
                self.velocity[0] = self.max_speed[0] * -1
                
            if self.velocity[1] > self.max_speed[1]:
                self.velocity[1] = self.max_speed[1]
            if self.velocity[1] < self.max_speed[1] * -1:
                self.velocity[1] = self.max_speed[1] * -1
                
        if not self.moving_x or not self.moving_y:
            self.velocity = self.velocity.move_towards((0,0), 0.06)
                    
        #print(self.velocity, self.max_speed)
        self.position += self.velocity* dt
        
    def turn(self, mouse_based=True):
        if not mouse_based:
            
            if self.vel_x < 0:
                self.ori = "left"
            if self.vel_x > 0:
                self.ori = "right"
        
        else:
            self.pos = pygame.math.Vector2(self.rect.center)
            rel_x,rel_y = pygame.mouse.get_pos() - self.pos
            self.angle = round(math.degrees(math.atan2(rel_x, rel_y)))

            if self.angle in self.go_left and self.angle is not self.go_left:
                if self.ori != "left":
                    self.ori = "left"
                    self.changed_ori = True
            if self.angle in self.go_right and self.angle is not self.go_right:
                if self.ori != "right":
                    self.ori = "right"
                    self.changed_ori = True
            if self.angle in self.go_down and self.angle is not self.go_down:
                if self.ori != "down":
                    self.ori = "down"
                    self.changed_ori = True
            if self.angle in self.go_up and self.angle is not self.go_up:
                if self.ori != "up":
                    self.ori = "up"
                    self.changed_ori = True

    def do_anim(self):
        self.max_index = len(self.image_path)
        if not self.animation == 'run':
            if pygame.time.get_ticks() > self.next_anim:
                self.index += 1   
                
                if self.index > self.max_index -2:
                    self.weapon.stop_attack = False

                if self.index > self.max_index:
                    self.index = 0
                    
                self.next_anim = pygame.time.get_ticks() + self.anim_rate
            self.anim_done = (self.index == self.max_index)
            
        else:
            if pygame.time.get_ticks() > self.next_anim:
                self.index += 1   
                
                if self.index > self.max_index -2:
                    self.weapon.stop_attack = False

                if self.index > self.max_index:
                    self.index = 0
                self.next_anim = pygame.time.get_ticks() + self.anim_rate
            self.anim_done = (self.index == self.max_index) or not ( self.moving_x or  self.moving_y)
        
    def animate(self):
        keys = pygame.key.get_pressed()
        mouse_pressed = pygame.mouse.get_pressed()
        if self.anim_done:
            if not (self.animation == "punch" or self.animation == "throw"):
                if self.moving_x or self.moving_y:
                    self.animation = "run"
                    self.anim_rate = 150
                    if keys[K_LSHIFT] and self.stamina > 0:
                        self.anim_rate = 100
                else:
                    if self.animation == "run":
                        self.index = 0

        if keys[pygame.K_SPACE] and not self.clicked_attack :
            self.animation = "throw"
            self.anim_rate = 125
            self.clicked_throw = True
            self.index = 0
            self.vel_x, self.vel_y = 0,0
            
        elif mouse_pressed[0] and not self.clicked_attack and self.anim_done and self.weapon.eligible_for_attack:
            self.animation = "punch"
            self.anim_rate = self.weapon.anim_speed
            self.clicked_attack = True
            self.weapon.stop_attack = True
            self.index = 0
            self.vel_x, self.vel_y = 0,0
            
        self.do_anim()
        if self.anim_done:
            self.animation = "run"
            
            self.anim_rate = 150
            self.index = 0
            
        if not mouse_pressed[0]:
            self.clicked_attack = False
        if not keys[pygame.K_SPACE]:
            self.clicked_throw = True

    def init_stats(self, speed, hp, melee_multi, agile_multi):
        self.starting_speed = speed 
        self.speed = speed 

        self.starting_melee = melee_multi 
        self.melee = melee_multi
        
        self.starting_agile = agile_multi
        self.agile = agile_multi
        
        self.multis = {
            "speed" : 1,
            "melee" : 1,
            "agile" : 1
        }
        
    def update_stats(self):
        
        self.speed = self.starting_speed * self.multis["speed"] * self.shift
        
        self.max_speed = self.start_max_speed * self.multis["speed"]
        
        self.melee = self.starting_melee * self.multis["melee"]
        
        self.agile = self.starting_agile * self.multis["agile"]
        
    def level_up(self, stat, amount):
        
        self.multis[stat] += amount