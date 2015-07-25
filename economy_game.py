import pygame
import sys
import random
import time
pygame.init()
screen = pygame.display.set_mode((940, 680),0,32)
clock = pygame.time.Clock()

#globals
ocean = pygame.Rect((814,0),(126,680))
#classes
class Background:
    def __init__(self):
        self.ocean = pygame.Rect((814,0),(126,680))
    def draw(self):
        screen.fill((218,165,32))
        pygame.draw.rect(screen,(0,0,255),ocean)
    def click(self,x,y,click):
        return False
class Building:
    def __init__(self,posX,posY,color):
        self.hud = Hud(0,0)
        self.hud.sell_button.action = self.sell_button_action
        self.hud.buy_button.action = self.buy_button_action
        objects.append(self.hud)
        self.square = pygame.Rect((posX,posY),(64,64))
        self.posX = posX
        self.posY = posY
        self.color = color
        self.owned = False

    def buy_button_action(self):
        self.owned = True
        print "buy ran"
    def sell_button_action(self):
        self.owned = False
        print "sell ran"
    def draw(self):
        if self.owned:
            self.color = (255,0,0)
        if not self.owned:
            self.color = (139,69,19)
        if self.hud == Hud.current_hud:
            self.color = (255,255,255)
        pygame.draw.rect(screen,self.color,self.square)
    def click(self,x,y,mouse_button):
        if mouse_button == (1,0,0):
            if self.posX + 64 > x > self.posX and self.posY + 64 > y > self.posY:
                Hud.current_hud = self.hud
        return False
        
class Button:
    def __init__(self,posX,posY,width,length,color):
        self.width = width
        self.length = length
        self.posX = posX
        self.posY = posY
        self.color = color
        
        self.action = None
    def draw(self):
        self.square = pygame.Rect((self.posX,self.posY),(self.width,self.length))
        pygame.draw.rect(screen,self.color,self.square)
    def click(self,x,y,button):
        if button == (1,0,0):
            if self.posX + 64 > x > self.posX and self.posY + 64 > y > self.posY:
                if self.action:
                    self.action()
                return True
        return False

class Hud:
    current_hud = None
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.buy_button = Button(x,y,64,64,(0,0,0))
        self.sell_button = Button(x,y,64,64,(255,100,0))
    def draw(self):
        if Hud.current_hud == self:
            self.square = pygame.Rect((self.x,self.y),(440,400))
            pygame.draw.rect(screen,(255,255,255),self.square)
            
            self.buy_button.posX = self.x + 100
            self.buy_button.posY = self.y + 100

            self.sell_button.posX = self.x + 300
            self.sell_button.posY = self.y + 100
            if self.sell_button not in objects:
                objects.append(self.sell_button)
            if self.buy_button not in objects:
                objects.append(self.buy_button)                
    def click(self,x,y,mouse_button):
        pass
#object list
objects = []


#functions
def draw():
    for item in objects:
        item.draw()
    pygame.display.update()
    clock.tick(60)

def make_button(x,y,width,length,color):
    new_button = Button(x,y,width,length,color)
    objects.append(new_button)


def make_grid(num_horiz,num_vert,start, end, color):
    xGap = 0
    yGap = 0
    if num_horiz > 1:
        xGap = ((end[0]-start[0])-64*num_horiz)/(num_horiz-1)
    if num_vert > 1:
        yGap = ((end[1]-start[1])-64*num_vert)/(num_vert-1)
    for i in range(num_horiz):
        for j in range(num_vert):
            objects.append(Building(i*(64+xGap)+start[0], j*(64+yGap)+start[1], color))


#game loop 
def run():    
    objects.append(Background())
    make_grid(4, 4, start=(470,0), end=(879, 680), color=(139,69,19))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                cur = event.pos
                click = pygame.mouse.get_pressed()
                for i in objects[::-1]:
                    if i.click(cur[0],cur[1],click):
                        break
        draw()

run()    

    
