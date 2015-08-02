import pygame
import time
import sys
import math
import random
pygame.init()
clock = pygame.time.Clock()


#####################    global variables     ###################
objects = []
zoom = 1
grid_tile_size = 50
number_of_linesx = 20
number_of_linesy = 20
window_width = 1240
window_height = 600

screen_width = window_width
screen_height = window_height

screen2_width = window_width/2
screen2_height = window_height

offsetx = 0
offsety = 0



window = pygame.display.set_mode((window_width, window_height),0,32)
screen = pygame.Surface((screen_width,screen_height))
#screen2 = pygame.Surface((screen2_width,screen2_height))
######################    global constants    ##########################
grid_lengthx = grid_tile_size * number_of_linesx
grid_lengthy = grid_tile_size * number_of_linesy
tile_count = number_of_linesx * number_of_linesy
#######################      classes          #######################
class Background:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.exists = True
        self.name = "background"
        self.rect = None
        self.width = None
        self.height = None
    def draw(self):
        screen.fill((255,255,255))
        #screen2.fill((255,255,255))
        make_grid(number_of_linesx,number_of_linesy,grid_tile_size,self.x + offsetx,self.y + offsety)

class Player:
    def __init__(self,x,y,width,height):
        self.exists = True
        self.name = "player"
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 10
        self.rect = None
    def move(self,speedx,speedy):    
        self.x += (speedx * self.speed)
        self.y += (speedy * self.speed)
        collide = check_player_collision()
        if collide != None:
            self.x -= (speedx * self.speed)
            self.y -= (speedy * self.speed)
        #print coords_to_tile(self.x,self.y)
    def laser_sight(self,mouse_pos):
        centerx = (self.x + self.width/2)
        centery = (self.y + self.height/2)            
        #laser_sight = pygame.draw.line(screen, (255,0,0), (centerx,centery),mouse_pos)
    def draw(self):
        self.rect = pygame.Rect((self.x + offsetx,self.y + offsety),(self.width,self.height))
        #self.rect2 = pygame.Rect((self.x,self.y),(self.width,self.height))
        pygame.draw.rect(screen,(0,0,0),self.rect)
        #pygame.draw.rect(screen2,(0,0,0),self.rect2)

class Bullet:
    def __init__(self,mouse,player):
        self.exists = True
        centerx = (player.x + player.width/2)
        centery = (player.y + player.height/2)
        self.x = centerx
        self.y = centery
        self.launch_point = (self.x,self.y)
        self.width = 20
        self.height = 20
        self.name = "bullet"
        self.speed = 5
        self.rect = None
        self.mouse = mouse
        self.dx,self.dy = self.mouse
        
        distance = [self.dx - self.x, self.dy - self.y]
        norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
        direction = [distance[0] / norm, distance[1] / norm]
        self.bullet_vector = [direction[0] * self.speed, direction[1] * self.speed]

    def move(self):
        self.x += self.bullet_vector[0]
        self.y += self.bullet_vector[1]

    def draw(self):
        make_bullet_trail(self,self.launch_point)
        self.rect = pygame.Rect((self.x + offsetx,self.y + offsety),(self.width,self.height))
        pygame.draw.rect(screen,(255,0,40),self.rect)
        #pygame.draw.rect(screen2,(255,0,40),self.rect)
        
class Asteroid:
    def __init__(self,x,y,width,height):
        self.exists = True
        self.name = "asteroid"
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = None
    def draw(self):
        self.rect = pygame.Rect((self.x + offsetx,self.y + offsety),(self.width,self.height))
        pygame.draw.rect(screen,(100,100,100),self.rect)
        #pygame.draw.rect(screen2,(100,100,100),self.rect)
#####################          functions           #######################
def make_bullet_trail(bullet,launch_point):
    x1 = bullet.x + offsetx
    y1 = bullet.y + offsety
    x2,y2 = launch_point 
    x2 += offsetx
    y2 += offsety
    start_len = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    final_len = min(start_len, 600)
    ratio = 1.0 * final_len / start_len
    x2 = x1 + (x2 - x1) * ratio
    y2 = y1 + (y2 - y1) * ratio
    
    pygame.draw.line(screen,(0,0,0),(x1,y1),(x2,y2))
def coords_to_tile(x,y):
    index = 0
    tilex = 0 
    while index < x:
        tilex += 1
        index += grid_tile_size
    index = 0
    tiley = 0 
    while index < y:
        tiley += 1
        index += grid_tile_size    
    return tilex,tiley

def tile_to_coords(tilex,tiley):
    x = (tilex * grid_tile_size * zoom) - grid_tile_size
    y = (tiley * grid_tile_size * zoom) - grid_tile_size
    return x,y

def collect_trash():
    for i in objects:
        if i.exists == False:
            objects.remove(i)

def generate_asteroids():
    grid_array = []
    index1 = 0
    index2 = 0
    x = 1
    y = 1
    while index1 < number_of_linesx:
        grid_array.append((x,y))
        while index2 < number_of_linesy:
            grid_array.append((x,y))
            y += 1
            index2 += 1
        x += 1
        index1 += 1
        index2 = 0
        y = 1

    for i in grid_array:
        number = random.randint(1,8)
        if number == 1:
            a,b = i
            x,y = tile_to_coords(a,b)
            asteroid = Asteroid(x,y,grid_tile_size,grid_tile_size)
            objects.append(asteroid)
            
def make_grid(number_of_linesx,number_of_linesy,tile_size,x,y):
    index = 0
    while index < number_of_linesy:
        pygame.draw.line(screen,(0,0,0),(x,y),(x + grid_lengthx, y),1)
        #pygame.draw.line(screen2,(0,0,0),(x,y),(x + grid_lengthx, y),1)
        y += tile_size
        index += 1
    index = 0
    x = 0 + offsetx
    y = 0 + offsety
    while index < number_of_linesx:
        pygame.draw.line(screen,(0,0,0),(x,y),(x, y + grid_lengthy),1)
        #pygame.draw.line(screen2,(0,0,0),(x,y),(x, y + grid_lengthy),1)
        x += tile_size
        index += 1

def check_player_collision():
    for i in objects:
        if i.name == "player":
            if i.rect != None:
                for j in objects:
                    if j.rect != None and j.rect != i.rect:
                        if i.rect.colliderect(j.rect):
                            return j.name
def check_bullet_collision():
    for i in objects:
        if i.name == "bullet":
            if i.rect != None:
                for j in objects:
                    if j.rect != None and j.rect != i.rect and j.name != "player" and j.name != "bullet":
                        if i.rect.colliderect(j.rect):
                            j.exists = False
                            i.exists = False
                    

def scroll(player):
    global offsetx
    global offsety
    if (player.x + offsetx) > (screen_width - 400):
        qty = (player.speed)
        offsetx -= qty
    if player.x + offsetx < 400:
        qty = (player.speed)
        offsetx += qty           
    if (player.y + offsety) > (screen_height - 400):
        qty = (player.speed)
        offsety -= qty
    if player.y + offsety < 400:
        qty = (player.speed)
        offsety += qty

def handle_events():
    for i in objects:
        if i.name == "player":
            player = i
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
 
        elif event.type == pygame.MOUSEBUTTONDOWN:
            cur = event.pos
            click = pygame.mouse.get_pressed()
            if click == (1,0,0):
                print cur
                print cur[0] + offsetx, cur[1] + offsety
                bullet = Bullet(cur,player)
                objects.append(bullet)



    keys_pressed = pygame.key.get_pressed()
  
    if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
        player.move(-1,0)
    if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
        player.move(1,0)
    if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:
        player.move(0,-1)
    if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
       player.move(0,1)


def draw(): 
    for item in objects:
        if item.name == "player":
            player = item
            scroll(player)
            mouse_pos = pygame.mouse.get_pos()
            player.laser_sight(mouse_pos)
    
        item.draw()
    pygame.display.update()
    clock.tick(60)

def move_objects():
    for i in objects:
        if i.name == "bullet":
            i.move()
def run():    
    objects.append(Background(0,0))
    generate_asteroids()
    player1 = Player(500,300,32,32)
    player2 = Player(600,500,32,32)
    if player1 not in objects:
        objects.append(player1)
    #if player2 not in objects:
        #objects.append(player2)

    while True:
        check_bullet_collision()
        collect_trash()
        handle_events()
        move_objects()
        draw()
        window.blit(screen,(0,0))
        #window.blit(screen2,(screen_width,0))
run()    
