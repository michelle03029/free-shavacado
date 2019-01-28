import pygame
from pygame.locals import *
import os
import sys
import math

class Chip(object):
    # CITATION: image from http://worldartsme.com/tortilla-chips-
    # clipart.html#gal_post_9088_tortilla-chips-clipart-1.jpg
    img = pygame.image.load(os.path.join("images", "chip.png"))
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitBox = (x, y, width, height)
        self.count = 0
        
    def draw(self, win):
        self.hitBox = (self.x, self.y + 6, self.width - 14, \
        self.height + 4)
        win.blit(pygame.transform.scale(self.img, (60, 60)), \
        (self.x, self.y))
        s = pygame.Surface((1000,750)) 
        s.set_alpha(128)               
        s.fill((255,255,255))      
        win.blit(s, (1000, 1000), self.hitBox)    
        
    def collide(self, rect):
        if rect[0] + rect[2] > self.hitBox[0] and rect[0] < \
        (self.hitBox[0] + self.hitBox[2]):
            if rect[1] + rect[3] > self.hitBox[1]: 
                return True
        return False