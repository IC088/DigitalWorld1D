import os
import sys
import random
import pygame
from pygame.locals import *
from time import sleep
from firebase import firebase
url = "https://dwfirebase.firebaseio.com" # URL to Firebase database
token = "DPY8XMO2SEGntN2kKInAlDmUNXww5L0qmwjXdYFW" # unique token used for authentication

firebase = firebase.FirebaseApplication(url, token)
up = 'up'
#creating player object in the game
class Player(object):
	def __init__(self):
		self.rect = pygame.Rect(32*5,32*7,32,32) #initialised as a square with length 32 and placed at coordinates(160,128)
	#giving method to move
	def move(self, dx,dy):
		if dx != 0:
			self.move_axis(dx,0)
		if dy != 0:
			self.move_axis(0,dy)
	#giving method to check for collision and make sure that it does not go through object
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
					self.rect.top = wall.rect.bottom # from for wall in walls checking for collision with wall (white border in the screen)
		for garbage in garbages:
			if self.rect.colliderect(garbage.rect):
				if dx > 0:
					garbage.rect.left += 32
				if dx < 0:
					garbage.rect.right -= 32
				if dy > 0:
					garbage.rect.top += 32
				if dy < 0:
					garbage.rect.bottom -= 32		#from for garbage in garbages checking for collision with trash (green object), this object is the wrong object to put in the hole, i.e. non-recyclables
		for recyclable in recyclables:
			if self.rect.colliderect(recyclable.rect):
				if dx > 0: 
					recyclable.rect.left += 32
				if dx < 0:
					recyclable.rect.right -= 32
				if dy > 0:
					recyclable.rect.top += 32
				if dy < 0:
					recyclable.rect.bottom -= 32	#from for recyclable in recyclables checking for collision with trash (green object), this object is the correct object to put in the hole, i.e. recyclables

class Trash(object):
	#initialise Non-recyclables
	def __init__(self, pos):
		garbages.append(self)
		self.rect = pygame.Rect(pos[0], pos[1], 32, 32)
class Recyclable(object):
	#initialise Recyclables
	def __init__(self, pos):
		recyclables.append(self)
		self.rect = pygame.Rect(pos[0], pos[1], 32, 32)


class Wall(object):
	#initialise Wall objects
	def __init__(self, pos):
		walls.append(self)
		self.rect = pygame.Rect(pos[0], pos[1], 32, 32)

class Exit(object):
	#initialise target hole
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
"WWWWWWWWWWW",
"WAAAAAAAAAW",
"WAAAAAAAGAW",
"WAAAAAAAAAW",
"WAAAAAAAAAW",
"WAAAAAAAAAW",
"WARAAAAAAAW",
"WAAAAAAAAAW",
"WAAAAAAAAAW",
"WWWWWWWWWWW"]
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
running = True					#defining variables for structure of map, bgm,position of non-recyclables and recyclables, and create window for the game itself.


#main loop for the game
def start():
	score = 0
	pygame.mixer.pre_init(44100,16,2,4096)
	pygame.init()
	pygame.font.init()

	running = True
	up,left,right,down = 'up','left','right','down'
	pygame.mixer.music.load(file)
	pygame.mixer.music.play(-1)
	myfont = pygame.font.SysFont('Impact', 20)
	img=pygame.image.load('Thymio.png')
	while running:
		clock.tick(60)
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				running = False
			if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
				running = False
		key = pygame.key.get_pressed()
		if key[pygame.K_a]: #event check
			player.move(-32, 0)
			firebase.put('/','movement', left) #upload for thymio use
		if key[pygame.K_d]:
			player.move(32, 0)
			firebase.put('/','movement', right) #upload for thymio use
		if key[pygame.K_w]:
			player.move(0, -32)
			firebase.put('/','movement', up) #upload for thymio use
		if key[pygame.K_s]:
			player.move(0, 32)
			firebase.put('/','movement', down)#upload for thymio use
		if key[pygame.K_j]:
			new_window()
    # Draw the scene
		screen.fill((0, 0, 0))
		for wall in walls:
			pygame.draw.rect(screen, (255, 255, 255), wall.rect) #drawing the walls for the game to limit the playing area to simulate real grids
		for garbage in garbages:
			pygame.draw.rect(screen, (0,255,0),garbage.rect)
			if garbage.rect.colliderect(ext.rect): 
				score = 100
				firebase.put('/Account/IC/Profile/','22',score)
				textsurface = myfont.render('You Are Correct! This is recyclable.', False, (255,255,255))
				textsurface2 = myfont.render("Press J to See your Score", False, (255,255,255))
				screen.blit(textsurface,(16,728))
				screen.blit(textsurface2,(16,760))
				#collision check between the non-recyclables and the target hole, pops out intended message on screen
		for recyclable in recyclables:
			pygame.draw.rect(screen, (0,255,0),recyclable.rect)
			if recyclable.rect.colliderect(ext.rect):
				score = 0 
				firebase.put('/Ivan/Profile/','Score',score)
				textsurface = myfont.render("I'm Sorry, But You Are Incorrect.", False, (255,255,255))
				textsurface2 = myfont.render("Press J to See your Score", False, (255,255,255))
				screen.blit(textsurface,(16,728))
				screen.blit(textsurface2,(16,760))
				#collision check between the recyclables and the target hole, pops out intended message on screen
		text_flavour  = "Hi there, Welcome to RON Control Center."
		text_flavour2 = "It's so nice to meet you."
		text_flavour3 = "We need your help in sorting out the trash."
		text_flavour4 = "As you see, there are 2 trashes one of which is recyclable."
		text_flavour5 = "we need you to push the one you think is recyclable to the hole."
		text_flavour6 = "Our friend, Thymio will be helping you do this, Good Luck!"
		text_flavour7 = "Use WASD to control Thymio."    # Game instructions string
		text1 = myfont.render(text_flavour,False, (255,255,255))
		text2 = myfont.render(text_flavour2,False, (255,255,255))
		text3 = myfont.render(text_flavour3,False, (255,255,255))
		text4 = myfont.render(text_flavour4,False, (255,255,255))
		text5 = myfont.render(text_flavour5,False, (255,255,255))
		text6 = myfont.render(text_flavour6,False, (255,255,255))
		text7 = myfont.render(text_flavour7,False, (255,255,255)) #render game instructions
		screen.blit(text1, (40,320))
		screen.blit(text2, (40,320+32))
		screen.blit(text3, (40,320+32*2))
		screen.blit(text4, (40,320+32*3))
		screen.blit(text5, (40,320+32*4))
		screen.blit(text6, (40,320+32*5))
		screen.blit(text7, (40,320+32*6)) #draws game instructions on screen
		screen.blit(img, (432,32))
		pygame.draw.rect(screen, (255,0,0),ext.rect) #draws target hole
		pygame.draw.rect(screen, (255, 200, 0), player.rect) #draws player
		pygame.display.flip() #update the screen

file_win = 'FF7.mp3' #load mp3 file
def new_window():
	pygame.mixer.pre_init(44100,16,2,4096)
	pygame.init()
	pygame.font.init() #initialise new window
	running = True
	pygame.mixer.music.load(file_win) #load music for playing
	pygame.mixer.music.play(-1) #play music
	myfont = pygame.font.SysFont('Impact', 50)
	hue = True
	while hue:
		screen.fill((255,255,255))
		texting = "Your Score is: 100!"
		text_test = myfont.render(texting,False, (0,0,0))
		screen.blit(text_test,(400,400))
		pygame.display.flip()
		key = pygame.key.get_pressed()
		if key[pygame.K_e]:
			hue = False
	pygame.display.quit()
	pygame.quit()
