import pygame, math
from pygame.locals import *
from assets import IMAGES
from random import randint, choice
import player, weapons, level, enemies, loot

LEVEL = 0 

class Room(pygame.sprite.Sprite):
    def __init__(self, pos, num, action, plr):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = IMAGES["levels"]["level"]
        self.rect = self.image.get_rect(center=pos)
        
        self.start_pos = pos 
        self.num = num
        self.pos = pos
        self.generated_mine = False
        self.locked = False
        self.use = action
        
        self.items_group = pygame.sprite.Group()
        
        if self.use == "fight":
            print("many monsters", self.num)
            self.enemies = pygame.sprite.Group()
            for i in range(randint(2,6)):
                self.enemies.add(enemies.Enemy(pygame.math.Vector2(self.rect.center) + pygame.math.Vector2(randint(-100,100), randint(-100,100)), False, 5, 0.1, "base", self, plr, randint(18,36)))
      
        if self.use == "merchant":
            print("time to spend ur moneh", self.num)
      
        if self.use == "chest":
            print("ooh shiny ", self.num)
            self.items_group.add(loot.Chest(self.rect.center))
        
        if self.use == "proceed":
            print("MOVING ON", self.num)
            self.block = loot.Proceed_Block(self.rect.center)
            
    def update(self, camera, screen, plr):


        if self.use == "fight":
            if plr.last_room == self:
                if not len(self.enemies) < 1:
                    self.locked = True 
                if len(self.enemies) < 1:
                    self.locked = False
        
        self.x,self.y = (self.start_pos[0] - camera.scroll[0], self.start_pos[1] - camera.scroll[1])
        self.rect = self.image.get_rect(center=(self.x,self.y) )
        
        
        
def generate_levels(plr):
    
    rooms = [
            (600,600),
            (600+1100,600),
            (600+1100+1100, 600),
            (600,600+1100),
            (600+1100,600+1100),
            (600+1100+1100, 600+1100),
            (600,600+1100+1100),
            (600+1100,600+1100+1100),
            (600+1100+1100, 600+1100+1100),

    ]
    mid_room = Room(rooms[4],4, choice(["fight", "empty", "chest"]), plr)
    room_list = [mid_room]

    # ["fight", "empty", "chest", "merchant"]
    force_add = ["proceed"]
    choices = ["fight", "empty", "chest"]

    while len(room_list) < 3:
        for i in range(randint(1,2)):
            for room in room_list:
                try:
                    next_add = force_add[0]
                except IndexError:
                    next_add = choice(choices)

                chance = randint(0,3)
                if chance  == 2:
                    if room.num-3 >= 0 and (rooms[room.num-3] not in [r.pos for r in room_list]) and not (room.num-3) in [x.num for x in room_list]:
                        room_list.append(Room(rooms[room.num-3], room.num-3, next_add, plr) )
                        

                if chance == 1:
                    if room.num+1 <= 8 and (rooms[room.num+1] not in [r.pos for r in room_list]) and not (room.num+1) in [x.num for x in room_list]:
                        room_list.append(Room(rooms[room.num+1], room.num+1, next_add, plr))
                        
     
                if chance == 3:
                    if room.num+3 <= 8 and (rooms[room.num+3] not in [r.pos for r in room_list]) and not (room.num+3) in [x.num for x in room_list]:
                        room_list.append(Room(rooms[room.num+3], room.num+3, next_add, plr))
                        

                if chance == 0:
                    if room.num-1 >= 0 and (rooms[room.num-1] not in [r.pos for r in room_list]) and not (room.num-1) in [x.num for x in room_list]:
                        room_list.append(Room(rooms[room.num-1], room.num-1, next_add, plr))
                        
                if next_add == "proceed":
                    force_add = []
            
    return room_list
            