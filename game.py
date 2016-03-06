import pygame
import time
import sys
import math
import random
import pickle
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
screen_width = 750
screen_height = 500
screen = pygame.display.set_mode((screen_width,screen_height),pygame.FULLSCREEN)
objects = []
start = time.time()
offsetx = 0
offsety = 0
game_over = False

######################   TODO:
######################           get background to move slower than foreground
######################           projectile functionality                           (easy)
######################           space station sprites                              (easy)
######################           npc ship AI                                        (HARD)
######################           minimap functionality                              (easy)
######################           add jetstream trails                               (easy)
######################           get framerate up                                   (HARD)

def load_sprite(imgName,scale):
    img = pygame.image.load(imgName).convert()
    if scale != None:
        img = pygame.transform.smoothscale(img,scale)
    transColor = img.get_at((0,0))
    img.set_colorkey(transColor)
    return img

background_sprite = pygame.image.load("background.jpg").convert()
background_sprite = pygame.transform.smoothscale(background_sprite,(2000,2000))

triangle_sprite = load_sprite("triangle.png",(20,20))
spaceship_still_sprite = load_sprite("SpaceShipStill.png",None)
spaceship_damage_readout_sprite = load_sprite("SpaceShipDamageReadout.png",(200,200))
damaged_left_sprite = load_sprite("DamagedLeft.png",(200,200))
#asteroid_sprite = load_sprite("asteroid.jpg",(150,150))
#trail_sprite = load_sprite("trail.jpg",None)
laser_sprite = load_sprite("green_laser.jpg",(50,50))
space_station_sprite = load_sprite("space_station.jpg",(1000,1000))


class Player:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.sprite = pygame.sprite.Sprite()
        self.name = "player"
        self.rect = None
        self.speed = 1
        self.width = 10
        self.height = 10
        self.image = spaceship_still_sprite
        self.angle = 0
    def draw(self):
        self.image = spaceship_still_sprite
        self.image = rot_center(self.image,self.angle)
        self.rect = pygame.Rect((self.x,self.y),(self.width,self.height))
        self.sprite.rect = self.rect        
        screen.blit(self.image, self.sprite.rect)
        pygame.draw.rect(screen,(144,122,0),((self.x,self.y),(20,20)))
        


class Game_state:
    def __init__(self):
        self.blink_timer = None
        fps_timer = time.time()
        
class Background:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.sprite = pygame.sprite.Sprite()
        self.name = "background"
        self.rect = None
        self.width = 10
        self.height = 10
        self.image = background_sprite
        self.angle = 0
    def draw(self):
        self.image = background_sprite
        #self.image = rot_center(self.image,self.angle)
        self.rect = pygame.Rect((self.x,self.y),(self.width,self.height))
        self.sprite.rect = self.rect        
        screen.blit(self.image, self.sprite.rect)

class Npc:
    def __init__(self,x,y,img,dx,dy):
        self.x = x
        self.y = y
        self.sprite = pygame.sprite.Sprite()
        self.name = "Npc"
        self.rect = None
        self.speed = 1
        self.width = 10
        self.height = 10
        self.original_image = img
        self.image = None
        self.friendly = True
        self.dx = dx
        self.dy = dy

        if self.dx != None and self.dy != None:
            self.angle = math.degrees(math.atan2(self.x - self.dx, self.y - self.dy)) + 316
            distance = [self.dx - self.x, self.dy - self.y]
            norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
            direction = [distance[0] / norm, distance[1] / norm]
            self.vector = [direction[0] * self.speed, direction[1] * self.speed]

    def draw(self):
        self.image = self.original_image
        self.rect = pygame.Rect((self.x + offsetx,self.y + offsety),(self.width,self.height))
        self.sprite.rect = self.rect
        if self.dx != None and self.dy != None:
            angle = math.degrees(math.atan2(self.x - self.dx, self.y - self.dy)) + 316
            self.image = rot_center(self.image,self.angle)
            self.move()
        screen.blit(self.image, self.sprite.rect)
    def move(self):
        self.x += self.vector[0]
        self.y += self.vector[1]

class Projectile:
    def __init__(self,x,y,angle):
        self.initialx = x
        self.initialy = y
        self.x = x
        self.y = y
        self.sprite = pygame.sprite.Sprite()
        self.name = "projectile"
        self.rect = None
        self.speed = .5
        self.width = 4
        self.height = 4
        self.image = laser_sprite
        self.angle = angle

    def draw(self):
        self.image = laser_sprite
        self.image = pygame.transform.rotate(self.image,self.angle)
        self.rect = pygame.Rect((self.x + offsetx,self.y + offsety),(self.width,self.height))
        self.sprite.rect = self.rect
        screen.blit(self.image, self.sprite.rect)
        self.move()
    def move(self):
        self.x -= math.cos(math.radians(self.angle)) * (self.speed)
        self.y += math.sin(math.radians(self.angle)) * (self.speed)

class Asteroid:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.sprite = pygame.sprite.Sprite()
        self.name = "Npc"
        self.rect = None
        self.width = 10
        self.height = 10
        self.image = space_station_sprite
    def draw(self):
        self.rect = pygame.Rect((self.x + offsetx,self.y + offsety),(self.width,self.height))
        self.sprite.rect = self.rect
        screen.blit(self.image, self.sprite.rect)

def rot_center(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


def handle_keys():
    keys_pressed = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_p:
                display_menu()

    for i in objects:
        if i.name == "player":
            global offsetx
            global offsety
            if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s] :
                for j in objects:
                    if j.name == "background":
                        j.x += math.cos(math.radians(i.angle)) * (i.speed)
                        j.y -= math.sin(math.radians(i.angle)) * (i.speed)
                        global offsetx
                        global offsety
                        offsetx += math.cos(math.radians(i.angle))
                        offsety -= math.sin(math.radians(i.angle))
            elif keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:
                for j in objects:
                    if j.name == "background":    
                        j.x -= math.cos(math.radians(i.angle)) * (i.speed)
                        j.y += math.sin(math.radians(i.angle)) * (i.speed)
                        global offsetx
                        global offsety
                        offsetx -= math.cos(math.radians(i.angle))
                        offsety += math.sin(math.radians(i.angle))
            
            if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
                i.angle += .4
            elif keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
                i.angle -= .4
            if keys_pressed[pygame.K_SPACE]:
                #projectile = Projectile(i.x + offsetx,i.y + offsety,i.angle)
                #objects.append(projectile)
                pass
def display_menu():
    pass

def move():
    pass
        
def check_collision():
    pass

def collect_trash():
    pass

def draw_hud(game_state):
    pygame.draw.rect(screen, (20,255,50),((15,screen_height - 185),(170,170)),1)
    pygame.draw.circle(screen, (20,255,50),(100,screen_height - 100),80,1)
    pygame.draw.circle(screen, (20,255,50),(100,screen_height - 100),65,1)
    pygame.draw.circle(screen, (20,255,50),(100,screen_height - 100),50,1)
    pygame.draw.circle(screen, (20,255,50),(100,screen_height - 100),35,1)
    pygame.draw.circle(screen, (20,255,50),(100,screen_height - 100),20,1)
    pygame.draw.circle(screen, (20,255,50),(100,screen_height - 100),7,1)
    for i in objects:
        if i.name == "player":
            angle = i.angle
    temp_sprite = rot_center(triangle_sprite,angle - 90)
    screen.blit(temp_sprite,((90,screen_height - 110),(10,10)))    
    #screen.blit(spaceship_damage_readout_sprite,((screen_width - 200,screen_height - 200),(5,5)))
    screen.blit(damaged_left_sprite,((screen_width - 200,screen_height - 200),(5,5)))    

    font = pygame.font.Font(None,30)
    fps = font.render(str(int(clock.get_fps()/10)),1,(255,255,255))
    screen.blit(fps,(100,100))
    
    return game_state

def draw(game_state):
    #screen.fill((255,255,255))
    for i in objects:
        if i.name == "background":
            i.draw()    
    for i in objects:
        if i.name != "background" and i.name != "player":
            i.draw()
    for i in objects:
        if i.name == "player":
            i.draw()
    game_state = draw_hud(game_state)
    pygame.display.update()
    clock.tick()

def run():
    background = Background(offsetx,offsety)
    player = Player(screen_width/2 - 50,screen_height/2)
    npc = Npc(screen_width/2,screen_height/2,spaceship_still_sprite,None,None)
    asteroid = Asteroid(500,500)
    
    objects.append(background)
    objects.append(player)
    objects.append(npc)
    objects.append(asteroid)
    
    
    game_state = Game_state()
    while game_over == False:
        handle_keys()
        move()
        check_collision()
        collect_trash()
        draw(game_state)

run()


        
