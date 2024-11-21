# -*- coding: utf-8 -*-
"""
Created on Fri Jul  7 18:20:58 2023

@author: sabarinadh
"""

import pygame
from pygame.locals import *
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

screenw = 800
screenh = 801
flying = False
gameover = False
pipegap = 200
pipefrequency = 1500# millisec
lastpipe = pygame.time.get_ticks() - pipefrequency
score = 0 
passedpipe = False


screen = pygame.display.set_mode((screenw , screenh))

pygame.display.set_caption('FLAPPY BIRD')

#define font
font = pygame.font.SysFont("Bauhaus 93",60)

#define colour
white = (255,255,255)

groundscroll = 0
scrollspeed = 4


#load image
bg = pygame.image.load('image/bgimg.png')
gimg = pygame.image.load('image/ground.png')
button_img = pygame.image.load('image/restart.png')

def draw_text(text,font,textcol,x,y):
    img = font.render(text, True,textcol)
    screen.blit(img, (x,y))
    
def reset_game():
    pipegroup.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screenh / 2)
    score = 0
    return score
    



class Bird(pygame.sprite.Sprite):
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1,4):
            img = pygame.image.load(f'image/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.vel = 0
        self.clicked = False
        
        
    def update(self):
        if flying == True:
            
    #  handle the animation
            # gravity
            self.vel +=0.5
            if self.vel > 8:
                self.vel =8
            if self.rect.bottom < 700:
                self.rect.y += int(self.vel)
        if gameover == False:    
            #jump
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
                 
                
            #  handle the animation
            self.counter +=1
            falpcooldown = 5
            if self.counter > falpcooldown:
                self.counter = 0
                self.index +=1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]   
     #rotation   
            self.image = pygame.transform.rotate(self.images[self.index], self.vel *-2)
        else:  
            self.image = pygame.transform.rotate(self.images[self.index], -90)

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x,y,position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("image/pipe.png")
        self.rect = self.image.get_rect()
        #pos 1 = froom top , -1 from bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image,False,True)
            self.rect.bottomleft = [x,y - int(pipegap / 2)]
        if position == -1:    
            self.rect.topleft  = [x,y +int(pipegap / 2)  ]

    def update(self):
        self.rect.x -= scrollspeed
        if self.rect.right < 0:
            self.kill()
        
class Button():
	def __init__(self, x, y, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)

	def draw(self):

		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check if mouse is over the button
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1:
				action = True

		#draw button
		screen.blit(self.image, (self.rect.x, self.rect.y))

		return action
        
birdgroup = pygame.sprite.Group()
pipegroup = pygame.sprite.Group()


flappy = Bird(100, int(screenh /2))
birdgroup.add(flappy)







#load image
bg = pygame.image.load('image/bgimg.png')
gimg = pygame.image.load('image/ground.png')

# create restart button 
button = Button(screenw // 2 - 50, screenh // 2 - 100, button_img)
# quit button

run = True
while run:
    
    clock.tick (fps)
    # bg
    screen.blit(bg,(0,0))
    
    
    birdgroup.draw(screen)
    birdgroup.update()
    pipegroup.draw(screen)
        
    
    screen.blit(gimg,(groundscroll,700))
    
    #check score
    if len(pipegroup) > 0:
        if birdgroup.sprites()[0].rect.left >pipegroup.sprites()[0].rect.left\
            and birdgroup.sprites()[0].rect.right < pipegroup.sprites()[0].rect.right\
            and passedpipe == False:
            passedpipe = True
        if passedpipe == True:
            if birdgroup.sprites()[0].rect.left >pipegroup.sprites()[0].rect.right:
                score +=1
                passedpipe =False
                
    draw_text(str(score),font,white,int(screenw/2),20)

            
        
        
    
    #look for collision
    if pygame.sprite.groupcollide(birdgroup,pipegroup,False,False ) or flappy.rect.top < 0:
        gameover = True
        
        
    #check if bird hit the ground
    if flappy.rect.bottom >=700:
        gameover = True
        flying = False
    
    if gameover == False and flying == True:
        #genereate pipe
        timenow = pygame.time.get_ticks()
        if timenow - lastpipe > pipefrequency:
            pipeheight = random.randint(-100,100)
            btmpipe = Pipe(screenw, int(screenh / 2)+ pipeheight,-1)
            toppipe = Pipe(screenw, int(screenh / 2)+ pipeheight, 1)
            pipegroup.add(btmpipe)
            pipegroup.add(toppipe)
            lastpipe = timenow
            
        
    # draw and scroll
    
        groundscroll -= scrollspeed
        
        if abs(groundscroll) > 35:
            groundscroll = 0  
            
        pipegroup.update()
        
    #check  4 game over nd reset

    if gameover == True:
    	if button.draw() == True:
            gameover = False
            score = reset_game()
        
        
        
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and gameover == False:
            flying = True
            
    pygame.display.update()        
            
pygame.quit()            