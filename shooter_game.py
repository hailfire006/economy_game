import pygame
import time
import sys
import math
pygame.init()
screen = pygame.display.set_mode((940, 680),0,32)
clock = pygame.time.Clock()



objects = []
class Background:
    def __init__(self):
        self.name = "background"
    def draw(self):
        screen.fill((255,255,255))


class Player:
    def __init__(self,x,y):
        self.name = "player"
        self.x = x
        self.y = y
        self.speed = 10
    def move(self,speedx,speedy):    
        self.x += (speedx * self.speed)
        self.y += (speedy * self.speed)
    def draw(self):
        square = pygame.Rect((self.x,self.y),(64,64))
        pygame.draw.rect(screen,(0,0,0),square)

class Bullet:
    def __init__(self,mouse,player):
        self.x = player.x
        self.y = player.y
        self.name = "bullet"
        self.speed = 13
        self.mouse = mouse
        self.dx,self.dy = self.mouse
    def move(self):
        distance = [self.dx - self.x, self.dy - self.y]
        norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
        direction = [distance[0] / norm, distance[1] / norm]
        bullet_vector = [direction[0] * self.speed, direction[1] * self.speed]

        self.x -= bullet_vector[0]
        self.y -= bullet_vector[1]

    def draw(self):
        square = pygame.Rect((self.x,self.y),(20,20))
        pygame.draw.rect(screen,(200,100,40),square)
        
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
            if click:
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
        item.draw()
        if item.name == "player":
            player = item
            mouse_pos = pygame.mouse.get_pos()
            laser_sight = pygame.draw.line(screen, (255,0,0), (player.x,player.y),mouse_pos)
    pygame.display.update()
    clock.tick(60)

def move_objects():
    for i in objects:
        if i.name == "bullet":
            i.move()

def run():    
    objects.append(Background())
    player = Player(500,500)
    if player not in objects:
        objects.append(player)
    while True:
        handle_events()
        move_objects()
        draw()
run()    
