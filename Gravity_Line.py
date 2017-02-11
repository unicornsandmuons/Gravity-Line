import pygame
from pygame.locals import *
from pygame.color import *
import pymunk
import pymunk.pygame_util
from pymunk import Vec2d
import math, sys, random

pygame.init()

width = 1080
height = 600

red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)


screen = pygame.display.set_mode((width,height))
screen.fill(black)
    
pygame.display.update()

rocketCoords = Vec2d(width/2,height-height/10)
rocketMass = 100
rocketV = Vec2d(0,-0.2)

dt = 5

# planetCoords = [Vec2d(100,500),Vec2d(980,500)] #nice and periodic
planetCoords = [Vec2d(530,300),Vec2d(300,560)]
planetMasses = [100,100]
planetColors = [pink,red]

def drawRocket(screen,coords,color):
    width = 20
    height = 10
    vertices = [(coords[0]-10,coords[1]),(coords[0]+10,coords[1]),(coords[0],coords[1]-10)]
    pygame.draw.lines(screen, color, True, vertices, 1)

def drawPlanets(screen,coords,colorlist):
    radius = 50
    for i in range(len(coords)):
        pygame.draw.circle(screen, colorlist[i], (coords[i][0],coords[i][1]), radius, radius)

def mag(v):
    return math.sqrt((v[0])**2 + (v[1])**2)

def unitVec(v):
    result = v/(mag(v))
    return result

def gravity(planetList,rocket,massesList,rocketMass):
    G = 1
    result = Vec2d(0,0)
    for i in range(len(planetList)):
        rhat = unitVec(planetList[i]-rocket)
        r = mag(planetList[i]-rocket)
        magnitude = ((G*massesList[i]*rocketMass)/(r*r))
        grav = rhat*magnitude
        result += grav
    return result

def collision(planetList,rocket):
    for i in range(len(planetList)):
        if (mag(planetList[i]-rocket) < 50):
            return True
    if (rocket[0] < 0 or rocket[0]>width):
        return True
    elif (rocket[1] <0 or rocket[1] > height):
        return True
    else:
        return False
    
def step(screen,planetCoords,planetColors,planetMasses,rocketCoords,rocketMass,rocketV):
    rocket = drawRocket(screen,rocketCoords,white)
    drawPlanets(screen,planetCoords,planetColors)
    
    if (not collision(planetCoords,rocketCoords)):
        force = gravity(planetCoords,rocketCoords,planetMasses,rocketMass)
        a = force/rocketMass
        rocketV += a*dt
        rocketCoords += rocketV*dt
    else:
        pygame.quit(); sys.exit()
    
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
             pygame.quit(); sys.exit()
             
    screen.fill(black)
    step(screen,planetCoords,planetColors,planetMasses,rocketCoords,rocketMass,rocketV)
    pygame.display.update()
