import pygame 
from pygame.locals import *

class Image_tools:
    def __init__(self):
        print("Thanks for using image tools")

    def get_sprites(self,sheet, images, save = False, name="autoname_"):
        
        apart = sheet.get_width() / images
        width = apart
        height = sheet.get_height()
        x = 0
        sprites = []
        
        for i in range(images):
            img = sheet.subsurface(pygame.Rect(x,0,width, height))
            sprites.append(img)
            if save:
                pygame.image.save(img, f"{name}{i}.png")
                
            x += apart
            
        return sprites
    
    def get_bigger(self,image, times_bigger):
        now_x = image.get_width()
        now_y = image.get_height()
        
        return pygame.transform.scale(image, (now_x * times_bigger, now_y*times_bigger))
    
    def get_smaller(self, image, times_smaller):
        now_x = image.get_width()
        now_y = image.get_height()
        
        return pygame.transform.scale(image, (now_x / times_smaller, now_y / times_smaller))
    
    def flip_x(self,image):
        return pygame.transform.flip(image, True, False)
    
    def flip_y(self,image):
        return pygame.transform.flip(image, False, True)
    
    def rotate(self, degrees, image):
        return pygame.transform.rotate(image, degrees)
    
def default_event_list():
    global RUN
    for event in pygame.event.get():
        if event.type == QUIT:
            quit()
            pygame.quit()
    
class Game:
    def __init__(self,screen_res, win_title="SET win_title to your game name!", color=(255,255,255), target_fps=0):
        print(" \nThank you for using my Pygame Template. \nWatch how it was made at https://www.youtube.com/channel/UCTHtClpiTYWKtBSkHi_q14w \n")
        
        self.screen_width, self.screen_height = screen_res
        self.screen = pygame.display.set_mode(screen_res)
        pygame.display.set_caption(win_title)
        self.clock = pygame.time.Clock()
        self.target_fps = target_fps 
        self.has_background = False
        
        self.color = color
        
        self.has_render_function = False
        self.has_spawn_function = False
        self.has_collisions_function = False
        self.has_custom_events = True
        
        self.background_fits = False

        self.pause = False
        
        self.last_time = pygame.time.get_ticks()
        
        self.player_group = pygame.sprite.Group()
        
        self.holding = False
        
        self.IMAGES = {}
        
    def set_background(self, bcg_image): 
        self.has_background = True
        self.bcg_image = bcg_image
        if bcg_image.get_width() < self.screen_width or bcg_image.get_height() < self.screen_height or bcg_image.get_width() > self.screen_width or bcg_image.get_height() > self.screen_height:
            print("The image you selected for background does not fit the screen resolution. If that is a problem please change it")
            
    def create_render_function(self, draw_function, update_function):
        self.update = update_function
        self.render = draw_function
        self.has_render_function = True
        
    def create_collision_function(self, collision_function):
        self.collisions = render_function
        self.has_collisions_function = True
        
    def create_spawn_function(self, spawn):
        self.spawn = spawn_function
        self.has_spawn_function = True
        
    def dt(self):
        global last_time
        dt = 0
        time_now = pygame.time.get_ticks()  # milliseconds since game start
        dt = time_now - self.last_time
        self.last_time = time_now
        return dt
        
    def update_game(self):
        self.clock.tick(self.target_fps)
        
        if self.has_background:
            if not self.background_fits:
                self.screen.fill(self.color)
            self.screen.blit(self.bcg_image, (0,0))
        else:
            self.screen.fill(self.color)
            
        if self.has_spawn_function and not self.pause and self.has_render_function:
            self.spawn()
        self.update()
            
        if self.has_collisions_function:
            self.collisions()   
            
        if self.has_render_function:
            self.render()
            
        pygame.display.update()
        
    def game_images(self, images):
        self.IMAGES = images
        for key in self.IMAGES:
            if isinstance(self.IMAGES[key], list):
                for image in self.IMAGES[key]:
                    image.convert()
            else:    
                self.IMAGES[key] = self.IMAGES[key].convert()
        
class GameObject(pygame.sprite.Sprite):
    def __init__(self, pos, speed,animated, anim_cooldown=200, move_type="hardcode"):
        pygame.sprite.Sprite.__init__(self)
        
        self.start_pos = pos
        self.speed = speed 
        self.animated = animated
        
        self.jumped = False
        
        self.touching_ground = False
        
        self.gravity_in_script = False
        
        self.move_type = move_type
        
        self.ANGLE = 0
        
        if move_type == "velocity":
            self.vel_y = 0 
            self.vel_x = 0
        elif move_type == "hardcode":
            print("Selected Hardcoded movement. Cannot use 'vel_x' and 'vel_y' variables, gravity and friction functions")
        
        self.gravity_force = 0.5
        self.gravity_max = 8   
        
        self.custom_keybinds = False
        
        if animated:
            self.animations = {}
            self.state = "idle"
            self.max_index = 0
            self.index = 0 
            self.rate = anim_cooldown
            self.next_anim = pygame.time.get_ticks() + self.rate
            
    def set_key_binds(self, left=K_a, right=K_d, up=K_w, down=K_s, jump=K_SPACE, attack=K_r, sprint=K_LSHIFT):
        
        self.move_left = left 
        self.move_right = right 
        self.move_up = up
        self.move_down = down 
        self.jump = jump 
        self.attack = attack 
        self.sprint = sprint
            
    def define_jump(self, jump_speed, hold_time):
        self.jump_strenght = jump_speed
        self.jump_hold_time = hold_time
        self.jump_held = 0
        self.got_jump = True
        self.holding = False
        
    def set_idle_image(self, image): 
        self.image = image 
        self.rect = self.image.get_rect(center=self.start_pos)
        
    def set_animations(self, idle_anim, run_anim="no", attack_anim="no"):
        if self.animated:
            self.animations["idle"] = idle_anim
            if not run_anim == "no":
                self.animations["run"] = run_anim
            if not attack_anim == "no":
                self.animations["attack"] = attack_anim
                
            self.set_animation("idle")
        else:
            print("This object is not animated. Please set 'animated' to True at instantiation")
            
    def add_new_animation(self, anim_name, animation):
        if self.animated:
            self.animations[anim_name] = animation
        else:
            print("This object is not animated. Please set 'animated' to True at instantiation")
            
    def set_animation(self, state):
        self.state = state
        self.current_anim = self.animations[self.state]
        self.index_max = len(self.current_anim)-1
        self.image = self.current_anim[0]
        
    def animate(self):
        time_now = pygame.time.get_ticks()
        if time_now > self.next_anim:
            self.index += 1
            if self.index >= self.index_max+ 1: 
                self.index = 0
            self.next_anim = time_now + self.rate
        self.image = self.current_anim[self.index]
        
    def gravity(self,grav_force, jump=False):
        self.gravity_in_script = True
        self.grav_force = grav_force
        
        if self.move_type == "velocity":
            self.vel_y += grav_force
            # if self.vel_y > self.y_vel_cap:
            #     self.vel_y = self.y_vel_cap              
            
        elif self.move_type == "hardcode":
            self.rect.y += grav_force
            
    def jump(self, touch_ground=True):
        try:
            
            self.pressed_jump = pygame.key.get_pressed()[K_SPACE] 
            
            
            if not self.jumped:
                if self.pressed_jump:
                    if self.touching_ground or touch_ground:
                        self.vel_y = self.jump_strenght * -1
                        self.jumped = True
                        self.holding = True
                        self.touching_ground = False
            
            if self.holding:
                self.jump_held += 1 
                #self.y_vel_cap += 2
                self.vel_y = self.jump_strenght * -1

                if self.jump_held >= self.jump_hold_time:
                    self.jump_held = 0 
                    self.holding = False

            if self.touching_ground:
                self.jumped = False
            
            if self.touching_ground and self.jumped and touch_ground:
                self.jumped = False
                self.jump_held = 0
            if touch_ground:
                self.jumped = False
            
        except AttributeError:
            raise Exception('Please use define_jump() after instantiating the object')
        
    def move_character(self):
        keypr = pygame.key.get_pressed()
        self.vel_x += (keypr[K_RIGHT] - keypr[K_LEFT]) * self.speed
        if not self.gravity_in_script:
            self.vel_y += (keypr[K_DOWN] - keypr[K_UP]) * self.speed
            
    def friction(self, friction_force):
        
        if self.move_type == "velocity":
            
            self.fric = friction_force
            
            fr_x = friction_force
            fr_y = friction_force
            
            if int(fr_x * 10) & int(self.vel_x * 10) != 0 :
                fr_x -= 0.01
                
            if int(fr_y*10) & int(self.vel_y * 10) != 0 :
                fr_y -= 0.01
                
            if self.vel_x > 0:
                self.vel_x -= fr_x
            if self.vel_x < 0:
                self.vel_x += fr_x
                
            if not self.gravity_in_script:
                if self.vel_y > 0:
                    self.vel_y -= fr_y
                if self.vel_y < 0:
                    self.vel_y += fr_y
                
            if self.vel_y == 0:
                fr_y = self.fric
            if self.vel_x == 0:
                fr_x = self.fric
                
            self.vel_x = round(self.vel_x, 1)   
            self.vel_y = round(self.vel_y, 1)   

    def bottom_border(self, margin, bouncy=False):
        if self.rect.y > margin:
            self.touching_ground = True
            if self.move_type == "velocity":
                if bouncy:
                    self.vel_y *= -1
                else:
                    self.vel_y = self.grav_force * -2
            elif self.move_type == "hardcode":
                self.rect.y -= self.speed
                
    def top_border(self, margin, bouncy=False):
        if self.rect.y < margin:
            if self.move_type == "velocity":
                if bouncy:
                    self.vel_y *= -1
                else:
                    self.vel_y =1
            elif self.move_type == "hardcode":
                self.rect.y += self.speed
                
    def side_borders(self, left_margin, right_margin, bouncy):
        if self.rect.x < left_margin:
            if self.move_type == "velocity":
                if bouncy:
                    self.vel_x *= -1
                else:
                    self.vel_x = 2
            elif self.move_type == "hardcode":
                self.rect.x += self.speed 

        if self.rect.x > right_margin - self.image.get_width():
            if self.move_type == "velocity":
                if bouncy:
                    self.vel_x *= -1
                else:
                    self.vel_x = -2
            elif self.move_type == "hardcode":
                self.rect.x -= self.speed 
    
    def set_vel_cap(self, vel_x, vel_y, vel_xv=4, vel_yv=4):
        self.cap_x = vel_x
        self.cap_y = vel_y
        
        if vel_x:
            self.x_vel_cap=vel_xv
        if vel_y:
            self.y_vel_cap=vel_yv
            
    def cap_velocity(self, x, y):
        if x : 
            if self.vel_x > self.x_vel_cap:
                self.vel_x = self.x_vel_cap 
            if self.vel_x < self.x_vel_cap * -1:
                self.vel_x = self.x_vel_cap * -1
            
        if y: 
            if self.vel_y > self.y_vel_cap:
                self.vel_y = self.y_vel_cap 
            if self.vel_y < self.y_vel_cap * -1:
                self.vel_y = self.y_vel_cap * -1

            
if __name__ == '__main__':
    pass