import os
import random
import pygame

class Player(object):
	def __init__(self):
		self.rect = pygame.Rect(32,120,16,16)

	def move(self, dx, dy):
		if dx != 0:
			self.move_axis(dx,0)
		if dy != 0:
			self.move_axis(0,dy)

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
class Wall(object):
	def __init__(self, pos):
		walls.append(self)
		self.rect = pygame.Rect(pos[0], pos[1], 16, 16)


pygame.init()

pygame.display.set_caption("ROBOT SIMULATION TEST")

screen = pygame.display.set_mode((320,240))

clock = pygame.time.Clock()
walls = [] 
player = Player()
level = ["WWWWWWWWWWWWWWWWWWWWW","WAAAAAAAAAAAAAAAAAAW","WWWWWWWWAAAAAAAAAAWWWWWWW","WAAAAAAAAAAAAAAAAWWWWWWWWW","WAAAAAAAAAAAAAAAAAAAAAAWW","W","W","W","W","W","W","W","W","W","WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW"]
x = y = 0
for row in level:
	for col in row:
		if col == "W":
			Wall((x, y))
		x += 16
	y += 16
	x = 0

running = True
while running:
	clock.tick(60)
	for e in pygame.event.get():
		if e.type == pygame.QUIT:
			running = False
		if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
			running = False
	key = pygame.key.get_pressed()
	if key[pygame.K_a]:
		player.move(-2, 0)
	if key[pygame.K_d]:
		player.move(2, 0)
	if key[pygame.K_w]:
		player.move(0, -2)
	if key[pygame.K_s]:
		player.move(0, 2)
    
    # Draw the scene
	screen.fill((0, 0, 0))
	for wall in walls:
		pygame.draw.rect(screen, (255, 255, 255), wall.rect)
	pygame.draw.rect(screen, (255, 200, 0), player.rect)
	pygame.display.flip()
