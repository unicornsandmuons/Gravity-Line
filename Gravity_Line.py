import pygame
from pygame.locals import *
from pygame.color import *
import pymunk
import pymunk.pygame_util
from pymunk import Vec2d
import math, sys, random
from SciStuff import unitVec,mag,gravity,collision

pygame.init()

width = 1080
height = 600

dt = 5

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

planetCoords = [Vec2d(530,300),Vec2d(300,500)]
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
    
def step(screen,planetCoords,planetColors,planetMasses,rocketCoords,rocketMass,rocketV):
    rocket = drawRocket(screen,rocketCoords,white)
    drawPlanets(screen,planetCoords,planetColors)
    pygame.draw.rect(screen, green,(0,height-height/20,100,height/20))
    mouse = pygame.mouse.get_pressed()
    if mouse[0] == 1:
        x,y = pygame.mouse.get_pos()
        if (x>= 0 and x <= 100):
            if (y >= height-height/20 and y<= height):
                print("pressed fr")
    
    if (not collision(planetCoords,rocketCoords,width,height)):
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
