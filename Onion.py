import pygame
from pygame.locals import *
import os
import sys
import math
from Chip import Chip

class Onion(Chip):
    # CITATION: image from 
    # https://www.pinterest.com/pin/432204895481246458/?lp=true
    img = pygame.image.load(os.path.join("images", "onion.png"))
    def draw(self, win):
        self.hitBox = (self.x + 12, self.y +10, self.width + 61, \
        self.y + 284)
        win.blit(pygame.transform.scale(self.img, (140, 310)), \
        (self.x, self.y))
        s = pygame.Surface((1000,750))  
        s.set_alpha(128)                
        s.fill((255,255,255))          
        win.blit(s, (1000, 1000), self.hitBox)   
        
    def collide(self, rect):
        if rect[0] + rect[2] > self.hitBox[0] and rect[0] < \
        (self.hitBox[0] + self.hitBox[2]):
            if rect[1] < self.hitBox[3]: 
                return True
        return False