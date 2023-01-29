import pygame 
from pygame.locals import *
import template
import time

time_now = time.time()

tools = template.Image_tools()

screen = pygame.display.set_mode((1000,1000))

times_smaller = 3

IMAGES = { 
    "player" : {
        
        "right" : {
           "punch" : [
            tools.get_smaller(pygame.image.load("animations/player/punch_0.png").convert_alpha(), times_smaller),
            tools.get_smaller(pygame.image.load("animations/player/punch_1.png").convert_alpha(), times_smaller),
            tools.get_smaller(pygame.image.load("animations/player/punch_2.png").convert_alpha(), times_smaller),
            tools.get_smaller(pygame.image.load("animations/player/punch_3.png").convert_alpha(), times_smaller),
           ],
           "run" : [
            tools.get_smaller(pygame.image.load("animations/player/run0.png").convert_alpha(), times_smaller),
            tools.get_smaller(pygame.image.load("animations/player/run1.png").convert_alpha(), times_smaller),
            tools.get_smaller(pygame.image.load("animations/player/run2.png").convert_alpha(), times_smaller),
            tools.get_smaller(pygame.image.load("animations/player/run3.png").convert_alpha(), times_smaller),
           ],
           
           "throw" : [
            tools.get_smaller(pygame.image.load("animations/player/throw0.png").convert_alpha(), times_smaller),
            tools.get_smaller(pygame.image.load("animations/player/throw1.png").convert_alpha(), times_smaller),
            tools.get_smaller(pygame.image.load("animations/player/throw2.png").convert_alpha(), times_smaller),
            tools.get_smaller(pygame.image.load("animations/player/throw3.png").convert_alpha(), times_smaller),
            tools.get_smaller(pygame.image.load("animations/player/throw4.png").convert_alpha(), times_smaller),
            tools.get_smaller(pygame.image.load("animations/player/throw4.png").convert_alpha(), times_smaller),
            tools.get_smaller(pygame.image.load("animations/player/throw4.png").convert_alpha(), times_smaller),
           ],
            },
        
        "left" : {
           "punch" : [
            tools.flip_x(tools.get_smaller(pygame.image.load("animations/player/punch_0.png").convert_alpha(), times_smaller)),
            tools.flip_x(tools.get_smaller(pygame.image.load("animations/player/punch_1.png").convert_alpha(), times_smaller)),
            tools.flip_x(tools.get_smaller(pygame.image.load("animations/player/punch_2.png").convert_alpha(), times_smaller)),
            tools.flip_x(tools.get_smaller(pygame.image.load("animations/player/punch_3.png").convert_alpha(), times_smaller)),
           ],
           "run" : [
            tools.flip_x(tools.get_smaller(pygame.image.load("animations/player/run0.png").convert_alpha(), times_smaller)),
            tools.flip_x(tools.get_smaller(pygame.image.load("animations/player/run1.png").convert_alpha(), times_smaller)),
            tools.flip_x(tools.get_smaller(pygame.image.load("animations/player/run2.png").convert_alpha(), times_smaller)),
            tools.flip_x(tools.get_smaller(pygame.image.load("animations/player/run3.png").convert_alpha(), times_smaller)),
           ],
           
           "throw" : [
            tools.flip_x(tools.get_smaller(pygame.image.load("animations/player/throw0.png").convert_alpha(), times_smaller)),
            tools.flip_x(tools.get_smaller(pygame.image.load("animations/player/throw1.png").convert_alpha(), times_smaller)),
            tools.flip_x(tools.get_smaller(pygame.image.load("animations/player/throw2.png").convert_alpha(), times_smaller)),
            tools.flip_x(tools.get_smaller(pygame.image.load("animations/player/throw3.png").convert_alpha(), times_smaller)),
            tools.flip_x(tools.get_smaller(pygame.image.load("animations/player/throw4.png").convert_alpha(), times_smaller)),
            tools.flip_x(tools.get_smaller(pygame.image.load("animations/player/throw4.png").convert_alpha(), times_smaller)),
            tools.flip_x(tools.get_smaller(pygame.image.load("animations/player/throw4.png").convert_alpha(), times_smaller)),
           ],
            },
        
        "down" : {
           "punch" : [
            tools.rotate(-90, tools.get_smaller(pygame.image.load("animations/player/punch_0.png").convert_alpha(), times_smaller) ),
            tools.rotate(-90,tools.get_smaller(pygame.image.load("animations/player/punch_1.png").convert_alpha(), times_smaller)),
            tools.rotate(-90,tools.get_smaller(pygame.image.load("animations/player/punch_2.png").convert_alpha(), times_smaller)),
            tools.rotate(-90,tools.get_smaller(pygame.image.load("animations/player/punch_3.png").convert_alpha(), times_smaller)),
           ],
           "run" : [
            tools.rotate(-90,tools.get_smaller(pygame.image.load("animations/player/run0.png").convert_alpha(), times_smaller)),
            tools.rotate(-90,tools.get_smaller(pygame.image.load("animations/player/run1.png").convert_alpha(), times_smaller)),
            tools.rotate(-90,tools.get_smaller(pygame.image.load("animations/player/run2.png").convert_alpha(), times_smaller)),
            tools.rotate(-90,tools.get_smaller(pygame.image.load("animations/player/run3.png").convert_alpha(), times_smaller)),
           ],
           
           "throw" : [
            tools.rotate(-90,tools.get_smaller(pygame.image.load("animations/player/throw0.png").convert_alpha(), times_smaller)),
            tools.rotate(-90,tools.get_smaller(pygame.image.load("animations/player/throw1.png").convert_alpha(), times_smaller)),
            tools.rotate(-90,tools.get_smaller(pygame.image.load("animations/player/throw2.png").convert_alpha(), times_smaller)),
            tools.rotate(-90,tools.get_smaller(pygame.image.load("animations/player/throw3.png").convert_alpha(), times_smaller)),
            tools.rotate(-90,tools.get_smaller(pygame.image.load("animations/player/throw4.png").convert_alpha(), times_smaller)),
            tools.rotate(-90,tools.get_smaller(pygame.image.load("animations/player/throw4.png").convert_alpha(), times_smaller)),
            tools.rotate(-90,tools.get_smaller(pygame.image.load("animations/player/throw4.png").convert_alpha(), times_smaller)),
           ],
            },
        
        "up" : {
           "punch" : [
            tools.rotate(90, tools.get_smaller(pygame.image.load("animations/player/punch_0.png").convert_alpha(), times_smaller) ),
            tools.rotate(90,tools.get_smaller(pygame.image.load("animations/player/punch_1.png").convert_alpha(), times_smaller)),
            tools.rotate(90,tools.get_smaller(pygame.image.load("animations/player/punch_2.png").convert_alpha(), times_smaller)),
            tools.rotate(90,tools.get_smaller(pygame.image.load("animations/player/punch_3.png").convert_alpha(), times_smaller)),
           ],
           "run" : [
            tools.rotate(90,tools.get_smaller(pygame.image.load("animations/player/run0.png").convert_alpha(), times_smaller)),
            tools.rotate(90,tools.get_smaller(pygame.image.load("animations/player/run1.png").convert_alpha(), times_smaller)),
            tools.rotate(90,tools.get_smaller(pygame.image.load("animations/player/run2.png").convert_alpha(), times_smaller)),
            tools.rotate(90,tools.get_smaller(pygame.image.load("animations/player/run3.png").convert_alpha(), times_smaller)),
           ],
           
           "throw" : [
            tools.rotate(90,tools.get_smaller(pygame.image.load("animations/player/throw0.png").convert_alpha(), times_smaller)),
            tools.rotate(90,tools.get_smaller(pygame.image.load("animations/player/throw1.png").convert_alpha(), times_smaller)),
            tools.rotate(90,tools.get_smaller(pygame.image.load("animations/player/throw2.png").convert_alpha(), times_smaller)),
            tools.rotate(90,tools.get_smaller(pygame.image.load("animations/player/throw3.png").convert_alpha(), times_smaller)),
            tools.rotate(90,tools.get_smaller(pygame.image.load("animations/player/throw4.png").convert_alpha(), times_smaller)),
            tools.rotate(90,tools.get_smaller(pygame.image.load("animations/player/throw4.png").convert_alpha(), times_smaller)),
            tools.rotate(90,tools.get_smaller(pygame.image.load("animations/player/throw4.png").convert_alpha(), times_smaller)),
           ],
            },

    },
    
    "levels" : {
        "level" : tools.get_bigger(pygame.transform.scale(pygame.image.load("animations/level_imgs/level.png").convert_alpha(),(800,800)),1.2),
        "pathway" : {
            "x" : pygame.image.load("animations/level_imgs/pathway_x.png") ,
            "y" : pygame.image.load("animations/level_imgs/pathway_y.png")  
        },
    },
    
    "loot" : {
        "chest" : pygame.image.load("animations/loot/chest.png")    ,
        
        "melee" : tools.get_smaller(pygame.image.load("animations/loot/melee.png").convert_alpha(),2),
        "speed" : tools.get_smaller(pygame.image.load("animations/loot/speed.png").convert_alpha(),2),
        "agile" : tools.get_smaller(pygame.image.load("animations/loot/agile.png").convert_alpha(),2),
        "coin" : tools.get_smaller(pygame.image.load("animations/loot/coin.png").convert_alpha(),2),
    },
    
    "enemies" : {
        "base" : {
            
            "right" : {
                "run" : [
                    tools.get_smaller(pygame.image.load("animations/enemies/base_enemy_run_0.png").convert_alpha(),times_smaller),
                    tools.get_smaller(pygame.image.load("animations/enemies/base_enemy_run_1.png").convert_alpha(),times_smaller),
                    tools.get_smaller(pygame.image.load("animations/enemies/base_enemy_run_2.png").convert_alpha(),times_smaller),
                    tools.get_smaller(pygame.image.load("animations/enemies/base_enemy_run_3.png").convert_alpha(),times_smaller),
                ],
                "attack" : [
                    tools.get_smaller(pygame.image.load("animations/enemies/base_enemy_attack_0.png").convert_alpha(),times_smaller),
                    tools.get_smaller(pygame.image.load("animations/enemies/base_enemy_attack_1.png").convert_alpha(),times_smaller),
                    tools.get_smaller(pygame.image.load("animations/enemies/base_enemy_attack_2.png").convert_alpha(),times_smaller),
                ]
                
            },
            
            "left" : {
                "run" : [
                    tools.get_smaller(tools.flip_x(pygame.image.load("animations/enemies/base_enemy_run_0.png").convert_alpha()),times_smaller),
                    tools.get_smaller(tools.flip_x(pygame.image.load("animations/enemies/base_enemy_run_1.png").convert_alpha()),times_smaller),
                    tools.get_smaller(tools.flip_x(pygame.image.load("animations/enemies/base_enemy_run_2.png").convert_alpha()),times_smaller),
                    tools.get_smaller(tools.flip_x(pygame.image.load("animations/enemies/base_enemy_run_3.png").convert_alpha()),times_smaller),
                ],
                "attack" : [
                    tools.get_smaller(tools.flip_x(pygame.image.load("animations/enemies/base_enemy_attack_0.png").convert_alpha()),times_smaller),
                    tools.get_smaller(tools.flip_x(pygame.image.load("animations/enemies/base_enemy_attack_1.png").convert_alpha()),times_smaller),
                    tools.get_smaller(tools.flip_x(pygame.image.load("animations/enemies/base_enemy_attack_2.png").convert_alpha()),times_smaller),
                ]
                
            },
            
            "up" : {
                "run" : [
                    tools.get_smaller(tools.rotate(90,pygame.image.load("animations/enemies/base_enemy_run_0.png").convert_alpha()),times_smaller),
                    tools.get_smaller(tools.rotate(90,pygame.image.load("animations/enemies/base_enemy_run_1.png").convert_alpha()),times_smaller),
                    tools.get_smaller(tools.rotate(90,pygame.image.load("animations/enemies/base_enemy_run_2.png").convert_alpha()),times_smaller),
                    tools.get_smaller(tools.rotate(90,pygame.image.load("animations/enemies/base_enemy_run_3.png").convert_alpha()),times_smaller),
                ],
                "attack" : [
                    tools.get_smaller(tools.rotate(90,pygame.image.load("animations/enemies/base_enemy_attack_0.png").convert_alpha()), times_smaller),
                    tools.get_smaller(tools.rotate(90,pygame.image.load("animations/enemies/base_enemy_attack_1.png").convert_alpha()), times_smaller),
                    tools.get_smaller(tools.rotate(90,pygame.image.load("animations/enemies/base_enemy_attack_2.png").convert_alpha()), times_smaller),
                ]
                
            },
            
            "down" : {
                "run" : [
                    tools.get_smaller(tools.rotate(-90,pygame.image.load("animations/enemies/base_enemy_run_0.png").convert_alpha()),times_smaller),
                    tools.get_smaller(tools.rotate(-90,pygame.image.load("animations/enemies/base_enemy_run_1.png").convert_alpha()),times_smaller),
                    tools.get_smaller(tools.rotate(-90,pygame.image.load("animations/enemies/base_enemy_run_2.png").convert_alpha()),times_smaller),
                    tools.get_smaller(tools.rotate(-90,pygame.image.load("animations/enemies/base_enemy_run_3.png").convert_alpha()),times_smaller),
                ],
                "attack" : [
                    tools.get_smaller(tools.rotate(-90,pygame.image.load("animations/enemies/base_enemy_attack_0.png").convert_alpha()),times_smaller),
                    tools.get_smaller(tools.rotate(-90,pygame.image.load("animations/enemies/base_enemy_attack_1.png").convert_alpha()),times_smaller),
                    tools.get_smaller(tools.rotate(-90,pygame.image.load("animations/enemies/base_enemy_attack_2.png").convert_alpha()),times_smaller),
                ]
                
            },
            
        },
    },
    
    "weapons" : {
        "fists" : [
            tools.get_smaller(pygame.image.load("animations/weapons/fists.png").convert_alpha(),2.5),
                   ],
        
        "axe" : [
            tools.get_smaller(pygame.image.load("animations/weapons/axe.png").convert_alpha(),2.5),
            tools.get_smaller(tools.rotate(25,pygame.image.load("animations/weapons/axe.png").convert_alpha()),2.5),
            tools.get_smaller(tools.rotate(45,pygame.image.load("animations/weapons/axe.png").convert_alpha()),2.5),
            ],
        
        "sword" : [tools.get_smaller(pygame.image.load("animations/weapons/sword.png").convert_alpha(),2.5)],
    
    },
    
    "ui" : {
        "heart" : pygame.image.load("animations/ui/heart.png")
    },
    
    "mainmenu" : {
        "logo" : pygame.image.load("animations/main_menu/logo.png")  
    },
    
} 

print(f"finished loading in {round(time.time()-time_now,2)} seconds")