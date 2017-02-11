import pygame
from pygame.locals import *
from pygame.color import *
import pymunk
import pymunk.pygame_util
from pymunk import Vec2d
import math, sys, random

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

def collision(planetList,rocket,w,h):
    for i in range(len(planetList)):
        if (mag(planetList[i]-rocket) < 50):
            return True
    return rocket[0]<0 or rocket[0]>w or rocket[1]<0 or rocket[1]>h

def collisionRect(rocket,x0,y0,w,h):
    return rocket[0]>=x0 and rocket[0]<=x0+w and rocket[1]>=y0 and rocket[1]<=y0+h
