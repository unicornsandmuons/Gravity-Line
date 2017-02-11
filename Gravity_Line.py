import pygame
from pygame.locals import *
from pygame.color import *
import pymunk
import pymunk.pygame_util
from pymunk import Vec2d
import math, sys, random
from SciStuff import unitVec,mag,gravity,collision
from pygame import gfxdraw
import random

pygame.init()
pygame.font.init()

width = 1080
height = 600

red = (255,0,0)
green = (0,128,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)

MainColors = [red,green,blue,darkBlue,white,pink]

screen = pygame.display.set_mode((width,height))
screen.fill(black)
    
pygame.display.update()

rocketMass = 100
rocketCoords = Vec2d(width/2,height-height/10)
rocketPath = [(rocketCoords[0],rocketCoords[1])]
rocketV = Vec2d(0,-0.2)

planetCoords = [Vec2d(530,300),Vec2d(300,500)]
planetMasses = [100,100]
planetColors = [pink,red]


def drawStars(screen):
    for i in range(10):
        x = random.randint(0,width)
        y = random.randint(0,height)
        gfxdraw.pixel(screen, x, y, white)
        

def makePlanet():
    mouse = pygame.mouse.get_pressed()
    x,y = pygame.mouse.get_pos()
    pos = Vec2d(x,y)       
    if (len(planetCoords) <= 10):
        planetCoords.append(pos)
        planetMasses.append(100)
            
def drawRocket(screen,coords,color):
    width = 20
    height = 10
    vertices = [(coords[0]-10,coords[1]),(coords[0]+10,coords[1]),(coords[0],coords[1]-10)]
    pygame.draw.lines(screen, color, True, vertices, 1)

def drawPlanets(screen,coords,colorlist):
    radius = 50
    counter = 0
    for element in planetCoords:
        pygame.draw.circle(screen,colorlist[counter%len(colorlist)],(element[0],element[1]),radius,radius)
        counter += 1

def button(text,color,x0,y0,w,h):
    mouse = pygame.mouse.get_pressed()
    x,y = pygame.mouse.get_pos()
    if (x>=x0 and x<=x0+w and y>=y0 and y<=y0+h):
        newColor = (color[0]*0.5,color[1]*0.5,color[2]*0.5)
        pygame.draw.rect(screen,newColor,(x0,y0,w,h))
    else:
        pygame.draw.rect(screen,color,(x0,y0,w,h))
    buttonFont = pygame.font.SysFont("monospace", 25)
    buttonText = buttonFont.render(text, False, white)
    screen.blit(buttonText,(x0+(w-buttonFont.size(text)[0])/2,y0+(h-buttonFont.size(text)[1])/2))
    if mouse[0] == 1:
        if (x>=x0 and x<=x0+w and y>=y0 and y<=y0+h):
            return True
    else:
        return False

def step(screen,pCoords,pColors,pMasses,rCoords,rMass,rV,rPath):
    force = gravity(pCoords,rCoords,pMasses,rMass)
    a = force/rMass
    rV += a*dt
    rCoords += rocketV*dt
    rPath.append((rCoords[0],rCoords[1]))

dt = 5
run = False
level = 0
reset = False
butt = False

while True:

    screen.fill(black)
    drawStars(screen)

    if level==0:
        startFont = pygame.font.SysFont("monospace", 30)
        startText = startFont.render('Gravity Lines', False, white)
        screen.blit(startText,(-100+width/2,100+height/2))
        drawPlanets(screen,planetCoords,planetColors)
        drawRocket(screen,rocketCoords,white)
        run = True
        if collision(planetCoords,rocketCoords,width,height):
            run = False
        if button("START GAME",red,width/2-100,133+height/2,200,75):
            level +=1
            reset = True
    
    if reset:
        if level==1:
            #Reset to initial conditions
            rocketCoords = Vec2d(.8*width,height/2)
            rocketV = Vec2d(0,-.2)
            planetCoords = []
            planetMasses = []
            planetColors = [pink,red]
        elif level==2:
            rocketCoords = Vec2d(.2*width,*.75*height)
            rocketV = Vec2d(.3,-.2)
            planetCoords = []
            planetMasses = []
            planetColors = [pink,red]
        rocketPath=[(rocketCoords[0],rocketCoords[1])]
        reset = False
        run = False

    if level>0:
        drawPlanets(screen,planetCoords,MainColors)
        drawRocket(screen,rocketCoords,white)
        if len(rocketPath)>1:
            pygame.draw.lines(screen,white,False,rocketPath,1)
        if button("Start",green,0,.8*height,.2*width,.2*height):
            run = True
        else:
            for event in pygame.event.get():
                if (event.type == pygame.MOUSEBUTTONDOWN) and not run:
                    makePlanet()
        if button("Reset",red,.8*width,.8*height,.2*width,.2*height):
            reset = True
        if collision(planetCoords,rocketCoords,width,height):
            run = False

    if run:
        step(screen,planetCoords,planetColors,planetMasses,rocketCoords,rocketMass,rocketV,rocketPath)

    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
             pygame.quit(); sys.exit()
