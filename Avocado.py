import pygame
from pygame.locals import *
import os
import sys
import math

# CITATION: basic template to set up player class from: 
# https://github.com/techwithtim/side_scroller/blob/master/
# starterFile.py

class Player(object):
    # CITATION: avocado image from: https://www.behance.net/
    # gallery/46446607/Why-run-when-you-can-Guac
    # animated running avocado was edited by me
    run = [pygame.image.load(os.path.join('images', str(x) + \
    '.png')) for x in range(8,16)]
    jump = [pygame.image.load(os.path.join('images', str(x) + \
    '.png')) for x in range(1,8)]
    slide = [pygame.image.load(os.path.join('images', 'S1.png')),\
    pygame.image.load(os.path.join('images', 'S2.png')),\
    pygame.image.load(os.path.join('images', 'S2.png')),\
    pygame.image.load(os.path.join('images', 'S2.png')), \
    pygame.image.load(os.path.join('images', 'S2.png')),\
    pygame.image.load(os.path.join('images', 'S2.png')), \
    pygame.image.load(os.path.join('images', 'S2.png')), \
    pygame.image.load(os.path.join('images', 'S2.png')), \
    pygame.image.load(os.path.join('images', 'S3.png')), \
    pygame.image.load(os.path.join('images', 'S4.png')), \
    pygame.image.load(os.path.join('images', 'S5.png'))]
    fall = pygame.image.load(os.path.join('images', '0.png'))
    # character jumping
    jumpList = [1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,\
    3,3,3,3,3,3,3,3,3,3,3,3,4,4,\
    4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,\
    0,0,0,-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-3,\
    -3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-4,-4,-4,-4,-4,-4,-4,\
    -4,-4,-4,-4,-4]
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.sliding = False
        self.slideCount = 0
        self.jumpCount = 0
        self.runCount = 0
        self.slideUp = False
        self.falling = False

    def draw(self, win):
        if self.falling: 
            win.blit(pygame.transform.scale(self.fall, (135, 135)),\
             (self.x, self.y + 30))
        # multiple jump by factor to control height of jump
        # position will decrease back down when max height is reached
        elif self.jumping:
            self.y -= self.jumpList[self.jumpCount] * 2
            win.blit(pygame.transform.scale(self.jump\
            [self.jumpCount//18], (135, 135)), (self.x,self.y))
            self.jumpCount += 1
            if self.jumpCount > 108:
                self.jumpCount = 0
                self.jumping = False
                self.runCount = 0
            self.hitBox = (self.x + 4, self.y, self.width - 24,\
             self.height - 10)
        elif self.sliding or self.slideUp:
            if self.slideCount < 20:
                self.y += 1
            elif self.slideCount == 80:
                self.y -= 19
                self.sliding = False
                self.slideUp = True
            elif self.slideCount > 20 and self.slideCount < 80:
                self.hitBox = (self.x, self.y + 20, self.width - 8, \
                self.height - 10)
            if self.slideCount >= 110:
                self.slideCount = 0
                self.slideUp = False
                self.runCount = 0
                self.hitBox = (self.x + 4, self.y + 20, \
                self.width - 24, self.height - 10)
            win.blit(pygame.transform.scale(\
            self.slide[self.slideCount//10], (135, 135)), \
            (self.x,self.y))
            self.slideCount += 1
        else:
            if self.runCount > 42:
                self.runCount = 0
            win.blit(pygame.transform.scale(\
            self.run[self.runCount//6], (135, 135)), (self.x,self.y))
            self.runCount += 1
            self.hitBox = (self.x + 5, self.y + 6, self.width - 35, \
            self.height - 12)
        s = pygame.Surface((1000,750)) 
        s.set_alpha(128)                
        s.fill((255,255,255))           
        win.blit(s, (1000, 1000), self.hitBox)    
    