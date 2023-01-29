import pygame, math,time
from pygame.locals import *
from assets import IMAGES, tools
from random import uniform, randint
from ui import *
import player, weapons, level, enemies, cam,minimap , loot, weapons, template, threading

def gen_lvl(plr):
    import level

    level_list = level.generate_levels(plr)

    room_group = pygame.sprite.Group()
    for level in level_list:
        room_group.add(level)
    print(level_list, len(level_list))
    
    return room_group,level_list

screen_width, screen_height = 1000,1000

screen = pygame.display.set_mode((screen_width,screen_height))

clock = pygame.time.Clock()

player_group = pygame.sprite.Group()
plr = player.Player((600+1100,600+1300), 0.15, 200, 0.4)
player_group.add(plr)

cam = cam.Camera(.1,screen)

item_group = pygame.sprite.Group()

enter_key = False

playing = False

last_time = pygame.time.get_ticks()

coins = 0

level_num = 1

dt = 0

room_group,level_list = gen_lvl(plr)
map = minimap.Minimap(21.8, plr, level_list)

weapons = {#                 Name    user, speed   dmg   ulti  #outline colour
    "fists" : weapons.Weapon("fists", plr, 110,    0.2,  None,(255,249,201)),
    "axe" : weapons.Weapon(  "axe",   plr, 200,    .5, None,(100,165,181)),
    "sword" : weapons.Weapon("sword", plr, 130,    .4,  None,(255,249,201)),
}

plr.set_weapon(weapons["sword"])

item_group = pygame.sprite.Group()

def outline(img, loc, colour=(255,255,255), width=3):
    mask = pygame.mask.from_surface(img)
    mask_outline = mask.outline()
    n = 0 
    for point in mask_outline:
        mask_outline[n] = (point[0] + loc[0], point[1] + loc[1])
        n+=1
    pygame.draw.polygon(screen, colour, mask_outline,width)


def draw_around():
    
    for item in room_group.sprites():
        if screen.get_rect().colliderect(item.rect):
            screen.blit(item.image, item.rect.topleft)
      
    for item in item_group.sprites():
        if screen.get_rect().colliderect(item.rect):
            screen.blit(item.image, item.rect.topleft)
            
    for room in level_list:
        for item in room.items_group.sprites():
            if screen.get_rect().colliderect(item.rect):
                screen.blit(item.image, item.rect.topleft)
                
        try:
            for item in room.enemies.sprites():
                if screen.get_rect().colliderect(item.rect):
                    screen.blit(item.image, item.rect.topleft)
        except AttributeError:
            pass
        
        
print(range(200,800, 80))
    
hp_cords = [(i, 20) for i in range(200, 200+80*20, 80)]
        
def draw_ui():
    write(screen, f"{round(clock.get_fps())}FPS", (10,970), color=(255,255,255), font=pygame.font.Font("Minecraft.ttf", 30))

    for i in range(plr.hp):
        screen.blit(IMAGES["ui"]["heart"], hp_cords[i])
        
    screen.blit(tools.rotate(-25,tools.get_bigger(plr.weapon.images["right"],2.5)), (860,5))
    if not plr.weapon.name == "fists":
        outline(tools.rotate(-25,tools.get_bigger(plr.weapon.images["right"],2.5)), (860,5), colour=plr.weapon.colour, )
        if plr.weapon.buff:
            outline(plr.weapon.image, plr.weapon.rect.topleft,colour=plr.weapon.colour, width=2)
            
    write(screen, f"{coins}", (660,27), color=(255, 248, 118),font=pygame.font.Font("Minecraft.ttf", 45))
    screen.blit(tools.get_bigger(IMAGES["loot"]["coin"],1.5), (600,20), )
    
    write(screen, f"{level_num}", (500,900), color=(255,255,255),font=pygame.font.Font("Minecraft.ttf", 80))
    
amplitude = 20
freq = 5

logo_img = IMAGES["mainmenu"]["logo"]
rect = logo_img.get_rect()

rect.x,rect.y = screen.get_width()//3.5, 100
start_time = time.time()

def render():
    global logo_y, logo_vel, ori, start_time
    
    current_time = time.time()
    
    screen.fill((34,3,38))
    
    if playing:
        room_group.update(cam, screen,plr)
        item_group.update(cam, dt)

        draw_around()
            
        if plr.outside and not plr.room_locked:
            cam.follow(plr, dt)
            
        for room in level_list:
            room.items_group.update(cam)
            room.items_group.draw(screen)
            try:
                room.enemies.update(cam, dt)
                room.enemies.draw(screen)
            except AttributeError:
                pass
            
            try:
                room.block.update(cam.scroll, screen)
            except AttributeError:
                pass

        
        player_group.update(dt,cam)
        player_group.draw(screen)
        
        plr.weapon.update(cam.scroll, screen)
        
        map.update(screen,cam.scroll)
        
        draw_ui()
    
    else:   
        
        rect.y = amplitude * math.sin(freq*(current_time )) + 100
        
        the_other = amplitude * math.sin(freq*(current_time )) + 500
        
        screen.blit(logo_img, rect)
        
        write(screen,f"Press 'Space' to play" ,(rect[0]-75, the_other), color = (255,255,255),font=pygame.font.Font("Minecraft.ttf", 60) )
        
def collisions():
    global coins, room_group, item_group, level_list, map, level_num
    
    keys = pygame.key.get_pressed()
    hit = pygame.sprite.spritecollide(plr, room_group, False)
    if not hit :
        if plr.last_room.locked:
            plr.velocity *= -2
            plr.room_locked = True

        plr.outside = False
        plr.room_locked = False
        
    if hit :
        plr.outside = True
        plr.last_room = hit[0]
        plr.room_locked = False
        
    hit = pygame.sprite.spritecollide(plr, item_group, False)
    if hit:
        if hit[0].vulnerable:
            hit[0].kill()
            if hit[0].coin_pickup:
                try:
                    plr.level_up(hit[0].stat,hit[0].increase)
                    print(plr.multis)
                except Exception:
                    print("idk wtf")
            else:
                try:
                    coins += hit[0].amount
                    print(coins)
                except Exception:
                    print("idk wtf")
                    
            print("miam")
            
    for room in level_list:
        hit = pygame.sprite.spritecollide(plr, room.items_group, False)
        
        
        if hit :
            if enter_key:
                hit[0].spawn_item(item_group)
        
        if room.use == "proceed":
            if room.block.rect.colliderect(plr.rect):
                room_group,level_list = gen_lvl(plr)
                map = minimap.Minimap(21.8, plr, level_list)
                plr.position = pygame.math.Vector2((600+1100,600+1300))
                item_group = pygame.sprite.Group()
                level_num += 1
            
        if room.use == "fight":
            hit = pygame.sprite.spritecollide(plr, room.enemies, False)
            if hit:
                
                for hits in hit:

                    if plr.weapon.attacking:                        
                        hits.hp -= plr.weapon.damage
                        hits.took_dmg = False
                        
                        if hits.hp < 1:
                            
                            item_group.add(loot.Pickup(hits.rect.center, randint(4,12), (uniform(-.04,.04), uniform(-.04,.04)), cam.scroll))
                            hits.kill()
                        
                        
                        if hits.position[0] < plr.position[0]:
                            hits.velocity = pygame.math.Vector2((uniform(-.5,-.8),uniform(-.5,.8)))
                        if hits.position[0] > plr.position[0]:
                            hits.velocity = pygame.math.Vector2((uniform(.5,.8),uniform(-.5,.8)))      
                            
                    else:
                        hits.holding += 1 * dt
                        print(hits.holding, end=", ")
                        if hits.can_dmg and plr.can_dmg:
                            plr.hp -= 1
                            print("Damaged")
                            hits.can_dmg = False
                            plr.can_dmg = False
            else:
                for enemy in room.enemies.sprites():
                    enemy.holding = 0                                                        

def get_dt():
    global last_time
    dt = 0
    time_now = pygame.time.get_ticks()
    dt = time_now - last_time
    last_time = time_now
    return dt

run = True 


frames = []

while 1:
    clock.tick_busy_loop(0)

    collisions()
    render()
    
    dt = get_dt()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False 
            
            print(f"Quit with {round(clock.get_fps(), 1)}FPS")
            print(f"Avg FPS -> {round(sum(frames)/len(frames),1)}FPS")
            
            quit()
            
        if event.type == KEYDOWN:
            if event.key == K_r:
                room_group,level_list = gen_lvl(plr)
                map = minimap.Minimap(21.8, plr, level_list)
                plr.position = pygame.math.Vector2((600+1100,600+1300))
                item_group = pygame.sprite.Group()
                
            if event.key == K_1:
                plr.set_weapon(weapons["fists"])
            if event.key == K_2:
                plr.set_weapon(weapons["sword"])
            if event.key == K_3:
                plr.set_weapon(weapons["axe"])
                
            if event.key == K_v:
                plr.weapon.buff = not plr.weapon.buff
                
            if event.key == K_SPACE:
                playing = True

                
                
        enter_key = event.type == KEYDOWN and event.key == K_RETURN
            
    #print(f"Running with {round(clock.get_fps(), 1)}FPS")
    frames.append(clock.get_fps())
    pygame.display.update()

