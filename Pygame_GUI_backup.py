import os
import sys
import random
import pygame
from pygame.locals import *
from time import sleep
from firebase import firebase
import Kivy_Info_Screen
url = "https://dwfirebase.firebaseio.com" # URL to Firebase database
token = "DPY8XMO2SEGntN2kKInAlDmUNXww5L0qmwjXdYFW" # unique token used for authentication

firebase = firebase.FirebaseApplication(url, token)
up = 'up'
class Player(object):
	def __init__(self):
		self.rect = pygame.Rect(32*9,32*5,32,32)

	def move(self, dx,dy):
		if dx != 0:
			self.move_axis(dx,0)
			sleep(0.5)
		if dy != 0:
			self.move_axis(0,dy)
			sleep(0.5)
	def move_axis(self, dx, dy):
		self.rect.x += dx
		self.rect.y += dy

		for wall in walls:
			if self.rect.colliderect(wall.rect):
				if dx > 0: 
					self.rect.right = wall.rect.left
				if dx < 0:
					self.rect.left = wall.rect.right
				if dy > 0:
					self.rect.bottom = wall.rect.top
				if dy < 0:
					self.rect.top = wall.rect.bottom
		for garbage in garbages:
			if self.rect.colliderect(garbage.rect):
				if dx > 0: 
					self.rect.right = garbage.rect.left
					garbage.rect.left += 32
				if dx < 0:
					self.rect.left = garbage.rect.right
					garbage.rect.right -= 32
				if dy > 0:
					self.rect.bottom = garbage.rect.top
					garbage.rect.top += 32
				if dy < 0:
					self.rect.top = garbage.rect.bottom
					garbage.rect.bottom -= 32
		for recyclable in recyclables:
			if self.rect.colliderect(recyclable.rect):
				if dx > 0: 
					self.rect.right = recyclable.rect.left
					recyclable.rect.left += 32
				if dx < 0:
					self.rect.left = recyclable.rect.right
					recyclable.rect.right -= 32
				if dy > 0:
					self.rect.bottom = recyclable.rect.top
					recyclable.rect.top += 32
				if dy < 0:
					self.rect.top = recyclable.rect.bottom
					recyclable.rect.bottom -= 32

class Trash(object):
	def __init__(self, pos):
		garbages.append(self)
		self.rect = pygame.Rect(pos[0], pos[1], 32, 32)
class Recyclable(object):
	def __init__(self, pos):
		recyclables.append(self)
		self.rect = pygame.Rect(pos[0], pos[1], 32, 32)


class Wall(object):
	def __init__(self, pos):
		walls.append(self)
		self.rect = pygame.Rect(pos[0], pos[1], 32, 32)

class Exit(object):
	def __init__(self,pos):
		self.rect = pygame.Rect(pos[0], pos[1], 32, 32)

file = 'mario.mp3'

pygame.display.set_caption("1D GAME")

screen = pygame.display.set_mode((800,800))

clock = pygame.time.Clock()
walls = [] 
garbages = []
recyclables = []
player = Player()
ext = Exit([4*32,3*32])

level = [
"WWWWWWWW",
"WAAAAAAW",
"WAAAGAAW",
"WAAAAAAW",
"WARAAAAW",
"WAAAAAAW",
"WAAAAAAW",
"WWWWWWWW"]
x = y = 0
for row in level:
	for col in row:
		if col == "W":
			Wall((x, y))
		if col == "G":
			Trash((x,y))
		if col == "R":
			Recyclable((x,y))
		x += 32
	y += 32
	x = 0
running = True
black = (0,0,0)

def over():
	paused = True
	while paused:
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				paused = False
			if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
				paused = False
def start():

	pygame.mixer.pre_init(44100,16,2,4096)
	pygame.init()
	pygame.font.init()

	running = True
	up,left,right,down = 'up','left','right','down'
	pygame.mixer.music.load(file)
	pygame.mixer.music.play(-1)


	while running:
		clock.tick(60)
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				running = False
			if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
				running = False
		key = pygame.key.get_pressed()
		if key[pygame.K_a]:
			player.move(-32, 0)
			firebase.put('/','movement', left)
		if key[pygame.K_d]:
			player.move(32, 0)
			firebase.put('/','movement', right)
		if key[pygame.K_w]:
			player.move(0, -32)
			firebase.put('/','movement', up)
		if key[pygame.K_s]:
			player.move(0, 32)
			firebase.put('/','movement', down)
    # Draw the scene
		screen.fill((0, 0, 0))
		for wall in walls:
			pygame.draw.rect(screen, (255, 255, 255), wall.rect)
		for garbage in garbages:
			pygame.draw.rect(screen, (255,0,255),garbage.rect)
			if garbage.rect.colliderect(ext.rect): # you have to call this at the start, 
			# if you want to use this module.
				myfont = pygame.font.SysFont('Arial', 50)
				textsurface = myfont.render('You Win', False, (255,255,255))
				screen.blit(textsurface,(600,500))

		for recyclable in recyclables:
			pygame.draw.rect(screen, (255,255,0),recyclable.rect)
			if recyclable.rect.colliderect(ext.rect):
				myfont = pygame.font.SysFont('Arial', 50)
				textsurface = myfont.render('You Lost', False, (255,255,255))
				screen.blit(textsurface,(600,500))

		text_flavour  = "Hi there, Welcome to RON Control Center.\n It's so nice to meet you\n We need your help in sorting out the trash\n As you can see in the screen, there are 2 green squares which represent the trash that we need to take out in the real world.\n We need you to push one of the green blocks to the hole, represented by the red block\nOur friend, Thymio will be helping you do this, Good Luck!"
		screen.blit(text_flavour, (480,16))
		pygame.draw.rect(screen, (255,0,0),ext.rect)
		pygame.draw.rect(screen, (0, 255, 0), player.rect)
		pygame.display.flip()
start()