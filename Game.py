import pygame
from pygame.locals import *
import os
import sys
import math
import random
from Avocado import Player
from Chip import Chip
from Onion import Onion
from Star import Star
import copy
#from Button import Button

# CITATION: basic template to set up game from: 
# https://github.com/techwithtim/side_scroller/blob/master/
# starterFile.py

pygame.init()

W, H = 810, 447
win = pygame.display.set_mode((W,H))

# CITATION: background from: https://www.pinterest.com/
# pin/631137335248955157/?lp=true
bkg = pygame.image.load(os.path.join('images','bg.png')).convert()
bkgX = 0
bkgX2 = bkg.get_width()
# increase speed of game with FPS
clock = pygame.time.Clock()

# play background music
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play()

def button(text, x, y, width, height, inactive_color, active_color, action = "None"):
    global clicked
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width > cur[0] > x and y + height > cur[1] > y:
        pygame.draw.rect(bkg, active_color, (x, y, width, height))
        if click[0] == 1 and action != "None":
            if action == "quit":
                pygame.quit()
                quit()
            if action == "level1":
                playGame()
            if action == "level2":
                playMediumGame()
            if action == "level3":
                playHardGame()
            if action == "AIMode":
                selfMode()
    else: 
        pygame.draw.rect(bkg, inactive_color, (x, y, width, height)) 

def startScreen():
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                playGame()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                playMediumGame()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                playHardGame()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                selfMode()
        win.blit(bkg, (0, 0))
        fontType = pygame.font.SysFont("helvetica", 40)
        fontType2 = pygame.font.SysFont("helvetica bold", 30)
        message1 = fontType.render("Press 1 to play easy level", 1, \
        (0, 0, 0))
        message2 = fontType.render("Press 2 to play medium level", 1,\
        (0, 0, 0))
        message3 = fontType.render("Press 3 to play hard level", 1,\
        (0, 0, 0))
        message4 = fontType.render("Press space to view AI mode", 1, \
        (0, 0, 0))
        message5 = fontType2.render("Instructions: Press up to jump"+\
        " over chips and down to duck under onions."\
        , 1, (0, 0, 0))
        message6 = fontType2.render("Collect stars to earn points!" \
        , 1, (0, 0, 0))
        win.blit(message1,(W/2-message1.get_width()//2, 100))
        win.blit(message2,(W/2-message2.get_width()//2, 150))
        win.blit(message3,(W/2-message3.get_width()//2, 200))
        win.blit(message4,(W/2-message4.get_width()//2, 250))
        win.blit(message5,(W/2-message5.get_width()//2, 50))
        win.blit(message6,(W/2-message6.get_width()//2, 70))
        
        # create buttons
        # button("level 1", 50, 300, 100, 50, (0, 153, 76), (0,255,0), action = "level1")
        # button("level 2", 200, 300, 100, 50, (0, 153, 76), (0,255,0), action = "level2")
        # button("level 3", 350, 300, 100, 50, (0, 153, 76), (0,255,0), action = "level3")
        # button("AI Mode", 500, 300, 100, 50, (0, 153, 76), (0,255,0), action = "AIMode")
        # button("quit", 650, 300, 100, 50, (0, 153, 76), (0,255,0), action = "quit")

        pygame.display.update()
    
def gameOverScreen():
    global pauseCounter, objects, speed, score
    pauseCounter = 0
    objects = []
    speed = 30
    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                startScreen()
        win.blit(bkg, (0, 0))
        fontType = pygame.font.SysFont("helvetica", 80)
        highestScore = fontType.render("Highest Score: " + \
        str(updateFile()), 1, 
        (0, 0, 0))
        win.blit(highestScore,(W/2-highestScore.get_width()/2, 150))
        newScore = fontType.render("Score: " + str(score), 1, \
        (0, 0, 0))
        win.blit(newScore, (W/2 - newScore.get_width()/2, 250))
        # pygame.display.update()
        fontType = pygame.font.SysFont("helvetica", 40)
        message3 = fontType.render("Press space to go back to the start screen!", 1,\
        (0, 0, 0))
        win.blit(message3,(W/2-message3.get_width()//2, 100))
        pygame.display.update()
    # reset the score
    score = 0
    avocado.falling = False
    
# variables 
avocado = Player(120, 260, 140, 140)
# every half second, increase speed if score reaches multiple of 10
pygame.time.set_timer(USEREVENT+1, 500) 
# pygame.time.set_timer(USEREVENT+1, random.randrange(1000,1500))
# random object generation between 5 sec and 6.5 sec
pygame.time.set_timer(USEREVENT+2, random.randrange(5000, 6500)) 
speed = 30
run = True
pauseCounter = 0
fallSpeed = 0
objects = []
score = 0

def playGame():
    global pauseCounter, objects, speed, score, bkgX, bkgX2 
    global fallSpeed, event, powerups
    run = True
    avocado.falling = False
    score = 0
    while run: 
        if pauseCounter > 0:
            pauseCounter += 1
            # delay before showing end screen
            if pauseCounter * 40 > fallSpeed:
                gameOverScreen()
                
        newList = copy.copy(objects)
        for item in objects:
            # if instance of star, remove star from screen
            if item.collide(avocado.hitBox):
                if isinstance(item, Star):
                    newList.pop(objects.index(item))
                    score += 1
                else: 
                    avocado.falling = True
                    if pauseCounter == 0:
                        fallSpeed = speed
                        pauseCounter = 1
            item.x -= 1.4
            # off the screen, get rid of the object
            if item.x < item.width * -3:
                newList.pop(newList.index(item))
        objects = newList
                
        # move background back leftwards 
        bkgX -= 1.4
        # move background at different position
        bkgX2 -= 1.4
        # first background starts until the negative 
        # width of the background
        if bkgX < bkg.get_width() * -1:
            bkgX = bkg.get_width()
        if bkgX2 < bkg.get_width() * -1:
            bkgX2 = bkg.get_width()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == USEREVENT+1: 
                speed += 20
            if event.type == USEREVENT+2:
                # every second, add star to screen
                rand = random.randrange(0, 3)
                if rand == 0:
                    objects.append(Chip(810, 340, 64, 64))
                elif rand == 1:
                    objects.append(Star(810, 340, 64, 64))
                else: 
                    objects.append(Onion(810, -0.5, 48, 320))
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP]:
            if not (avocado.jumping):
                avocado.jumping = True
                
        if keys[pygame.K_DOWN]:
            if not (avocado.sliding):
                avocado.sliding = True
        
        clock.tick(speed)
        redrawWindow()

# set variable, background speed item.x - backroundSpeed        
def selfMode():
    global pauseCounter, objects, speed, score, bkgX, bkgX2 
    global fallSpeed, event, powerups
    run = True
    avocado.falling = False
    score = 0
    while run: 
        if pauseCounter > 0:
            pauseCounter += 1
            # delay before showing game over
            if pauseCounter * 40 > fallSpeed:
                gameOverScreen()
        
        newList = copy.copy(objects)
        for item in objects:
            # if instance of star, remove star from screen
            if item.collide(avocado.hitBox):
                if isinstance(item, Star):
                    newList.pop(objects.index(item))
                    score += 1
                elif isinstance(item, Chip):
                    avocado.jumping = True
                else: 
                    avocado.sliding = True
            item.x -= 3
            # off the screen, get rid of the object
            if item.x < item.width * -3:
                newList.pop(newList.index(item))
        objects = newList
        # move background back leftwards 
        bkgX -= 3
        # move background at different position
        bkgX2 -= 3
        # first background starts until the negative 
        # width of the background
        if bkgX < bkg.get_width() * -1:
            bkgX = bkg.get_width()
        if bkgX2 < bkg.get_width() * -1:
            bkgX2 = bkg.get_width()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == USEREVENT+1: 
                speed += 20
            if event.type == USEREVENT+2:
                # every second, add star to screen
                rand = random.randrange(0, 2)
                if rand == 0:
                    objects.append(Chip(810, 340, 64, 64))
                else:
                    objects.append(Star(810, 340, 64, 64))

        clock.tick(speed)
        redrawWindow()
        
pygame.time.set_timer(USEREVENT+3, 500) 
pygame.time.set_timer(USEREVENT+4, random.randrange(3000, 4500))         
def playMediumGame():
    global pauseCounter, objects, speed, score, bkgX, bkgX2 
    global fallSpeed, event, powerups
    run = True
    avocado.falling = False
    score = 0
    while run: 
        if pauseCounter > 0:
            pauseCounter += 1
            # delay 
            if pauseCounter * 40 > fallSpeed:
                gameOverScreen()
        
        newList = copy.copy(objects)
        for item in objects:
            # if instance of star, remove star from screen
            if item.collide(avocado.hitBox):
                if isinstance(item, Star):
                    newList.pop(objects.index(item))
                    score += 1
                else: 
                    avocado.falling = True
                    if pauseCounter == 0:
                        fallSpeed = speed
                        pauseCounter = 1
            item.x -= 3
            # off the screen, get rid of the object
            if item.x < item.width * -3:
                newList.pop(newList.index(item))
        objects = newList
                
        # move background back leftwards 
        bkgX -= 3
        # move background at different position
        bkgX2 -= 3
        # first background starts until the negative 
        # width of the background
        if bkgX < bkg.get_width() * -1:
            bkgX = bkg.get_width()
        if bkgX2 < bkg.get_width() * -1:
            bkgX2 = bkg.get_width()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == USEREVENT+3: 
                speed += 60
            if event.type == USEREVENT+4:
                # every second, add star to screen
                rand = random.randrange(0, 3)
                if rand == 0:
                    objects.append(Chip(810, 340, 64, 64))
                elif rand == 1:
                    objects.append(Star(810, 340, 64, 64))
                else: 
                    objects.append(Onion(810, -0.5, 48, 320))
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP]:
            if not (avocado.jumping):
                avocado.jumping = True
                
        if keys[pygame.K_DOWN]:
            if not (avocado.sliding):
                avocado.sliding = True
        
        clock.tick(speed)
        redrawWindow()

pygame.time.set_timer(USEREVENT+5, 500) 
pygame.time.set_timer(USEREVENT+6, random.randrange(3000, 4500))         
def playHardGame():
    global pauseCounter, objects, speed, score, bkgX, bkgX2 
    global fallSpeed, event, powerups
    run = True
    avocado.falling = False
    score = 0
    while run: 
        if pauseCounter > 0:
            pauseCounter += 1
            # delay gives about 2 seconds
            if pauseCounter * 40 > fallSpeed:
                gameOverScreen()
        
        newList = copy.copy(objects)
        for item in objects:
            # if instance of star, remove star from screen
            if item.collide(avocado.hitBox):
                if isinstance(item, Star):
                    newList.pop(objects.index(item))
                    score += 1
                else: 
                    avocado.falling = True
                    if pauseCounter == 0:
                        fallSpeed = speed
                        pauseCounter = 1
            item.x -= 7
            # off the screen, get rid of the object
            if item.x < item.width * -3:
                newList.pop(newList.index(item))
        objects = newList
                
        # move background back leftwards 
        bkgX -= 7
        # move background at different position
        bkgX2 -= 7
        # first background starts until the negative 
        # width of the background
        if bkgX < bkg.get_width() * -1:
            bkgX = bkg.get_width()
        if bkgX2 < bkg.get_width() * -1:
            bkgX2 = bkg.get_width()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == USEREVENT+5: 
                speed += 60
            if event.type == USEREVENT+6:
                # every second, add star to screen
                rand = random.randrange(0, 3)
                if rand == 0:
                    objects.append(Chip(810, 340, 64, 64))
                elif rand == 1:
                    objects.append(Star(810, 340, 64, 64))
                else: 
                    objects.append(Onion(810, -0.5, 48, 320))
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP]:
            if not (avocado.jumping):
                avocado.jumping = True
                
        if keys[pygame.K_DOWN]:
            if not (avocado.sliding):
                avocado.sliding = True
        
        clock.tick(speed)
        redrawWindow()

def updateFile():
    # open and save files, r is reading in the file
    f = open("scores.txt", "r")
    file = f.readlines()
    # only line used in the file
    last = int(file[0])
    # if last score is less than our score, reopen the file and
    # replace the content, higher score is updated in file
    if last < int(score):
        f.close()
        file = open("scores.txt", "w")
        file.write(str(score))
        file.close()
        return score
    return last
    
def redrawWindow(): 
    win.blit(bkg, (bkgX, 0))
    win.blit(bkg, (bkgX2, 0))
    avocado.draw(win)
    for item in objects: 
        item.draw(win)
    font = pygame.font.SysFont("helvetica", 30)
    text = font.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (650, 20))
    pygame.display.update()
    
startScreen()