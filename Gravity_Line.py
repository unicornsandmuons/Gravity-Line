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

#define colors
red = (255,0,0)
green = (0,128,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)
yellow = (247,255,0)

MainColors = [red,green,blue,darkBlue,white,pink]

screen = pygame.display.set_mode((width,height))
screen.fill(black)
    
pygame.display.update()

#rocket and planet conditions
rocketMass = 100
rocketCoords = Vec2d(width/2,height-height/10)
rocketPath = [(rocketCoords[0],rocketCoords[1])]
rocketV = Vec2d(0,-0.2)

planetCoords = [Vec2d(530,300),Vec2d(300,500)]
planetMasses = [100,100]
planetColors = [pink,red]

winBox = (.8*width,0,.2*width,.2*height)


#randomly draws stars on screen in background
def drawStars(screen):
    for i in range(10):
        x = random.randint(0,width)
        y = random.randint(0,height)
        gfxdraw.pixel(screen, x, y, white)
        
#makes a planet but doesn't draw it on screen. Is added to the planets list
def makePlanet():
    mouse = pygame.mouse.get_pressed()
    x,y = pygame.mouse.get_pos()
    pos = Vec2d(x,y)       
    if (len(planetCoords) <= 10):
        planetCoords.append(pos)
        planetMasses.append(100)

#draws the rocket. Rocket is a triangle.
def drawRocket(screen,coords,color):
    width = 20
    height = 10
    vertices = [(coords[0]-10,coords[1]),(coords[0]+10,coords[1]),(coords[0],coords[1]-10)]
    pygame.draw.lines(screen, color, True, vertices, 1)

#draws the planets by looping through the planet list
def drawPlanets(screen,coords,colorlist):
    radius = 50
    counter = 0
    for element in planetCoords:
        pygame.draw.circle(screen,colorlist[counter%len(colorlist)],(element[0],element[1]),radius,radius)
        counter += 1

#generic button that can have text. Color changed to make "pressed" look
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

def text(text,x0,y0,w,h,color,size):
    textFont = pygame.font.SysFont("monospace", size)
    makeText = textFont.render(text, False, color)
    screen.blit(makeText,(x0+(w-textFont.size(text)[0])/2,y0+(h-textFont.size(text)[1])/2))

#Iterate rocket
def step(screen,pCoords,pMasses,rCoords,rMass,rV,rPath):
    force = gravity(pCoords,rCoords,pMasses,rMass)
    a = force/rMass
    rV += a*dt
    rCoords += rocketV*dt
    rPath.append((rCoords[0],rCoords[1]))

def passedLevel(rCoords,winarea):
    x0,y0,w,h = winarea[0],winarea[1],winarea[2],winarea[3]
    x,y = rCoords[0],rCoords[1]
    if (x>=x0 and x<=x0+w and y>=y0 and y<=y0+h):
        return True
    return False

def killme():
    x,y = pygame.mouse.get_pos()
    return (y>=.8*height or y<=.2*height)and (x<=.2*width or x>=.8*width)

dt = 5          #time step
run = False     #when simulation is running or not
level = 0       #what level the game is on. 0 is start screen
reset = False   #if simulation should be reset or not
resetRocket = False

while True:
    #Exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
        if (event.type == pygame.MOUSEBUTTONDOWN) and not run and not killme():
            makePlanet()
    
    screen.fill(black)
    drawStars(screen)
    
    #Start and About screen 
    if level==0:
        text("Gravity Lines",-100+width*.5,height*.1,white,30)
        drawPlanets(screen,planetCoords,planetColors)
        drawRocket(screen,rocketCoords,white)
        run = True
        if collision(planetCoords,rocketCoords,width,height):
            run = False
        if button("START GAME",red,width/3.0-100,height/5,200,75):
            level = -2
            reset = True
        if button("ABOUT",blue,2*width/3.0,height/5,200,75):
            level = -1
            reset = True
    if level == -1:
        text("This game is to learn about GRAVITY!",50,height*.1,white,30)
        if button("Back to Menu",blue,width/2.0,height/2,200,75):
            level = 0
    if level==-2:
        text("When two objects have mass they exert a force on each other that pulls them together",
             50,height*0.1,white,30)
        text("This force is called",50,height*0.1+35,white,30)
        text("GRAVITY",.5*width,height*0.1+65,red,50)
        if button("Play",blue,2*width/3.0,height/5,200,75):
            level = 2
            reset = True
        text("Watch the rocket as it goes to the red planet",50,height/2.0,white,30)
        text("You can even click to make new planets",50,height/2.0+40,white,30)
        text("Try to get it into the yellow box without crashing",50,height/2.0+70,white,30)
    if level == -3:
        text("How does gravity work though?",50,height*0.1,white,50)
        text("Isaac Newton was one of the first people to attempt to give a mathematical description of gravity",
             20,height*0.1+60,white,25)
        text("His work tells us that the force of gravity is an inverse square law",
             20,height*0.1+80,white,25)
        
    #Reset planets and rocket to initial positions

    if reset:             
        if level==2:
            rocketCoords = Vec2d(.2*width,.75*height)
            rocketV = Vec2d(.3,-.2)
            planetCoords = [Vec2d(width-50,50)]
            planetMasses = [100]
            rocketCoordsi = rocketCoords
        rocketPath=[(rocketCoords[0],rocketCoords[1])]
        reset = False
        run = False

    #Reset rocket to initial position, but keep all added planets
    if resetRocket:
        if level==2:
            rocketCoords = Vec2d(.2*width,.75*height)
            rocketV = Vec2d(.3,-.2)
        rocketPath=[(rocketCoords[0],rocketCoords[1])]
        resetRocket = False
        run = False

    #Gameplay events
    if level>0:
        drawPlanets(screen,planetCoords,MainColors)
        drawRocket(screen,rocketCoords,white)
        pygame.draw.rect(screen,yellow,(.8*width,0,.2*width,.2*height),2)
        if len(rocketPath)>1:
            pygame.draw.lines(screen,white,False,rocketPath,1)
        if button("Start",green,0,.8*height,.2*width,.2*height):
            run = True
        if passedLevel(rocketCoords,winBox):
            run = False
            if button("You Won! Next Level",yellow,width/2-100,height/2-30,200,60):
                level = -1*level-1
        if button("Reset All",red,.8*width,.8*height,.2*width,.2*height):
            reset = True
        if button("Reset Rocket",blue,0,0,0.2*width,0.2*height):
            resetRocket = True
        if collision(planetCoords,rocketCoords,width,height):
            run = False

    if run:
        step(screen,planetCoords,planetMasses,rocketCoords,rocketMass,rocketV,rocketPath)

    pygame.display.update()
    
