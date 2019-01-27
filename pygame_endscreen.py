import os
import sys
import random
import pygame
from pygame.locals import *
from time import sleep


screen = pygame.display.set_mode((800,800))
pygame.display.set_caption("1D GAME")
pygame.display.init()

def start_end_screen():
	textsurface = myfont.render('You Lost', False, (255,255,255))
	
	pygame.display.update()