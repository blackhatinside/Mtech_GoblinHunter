import pygame
from enum import Enum

print("Hello World")

class Color(Enum):
	BLACK = (0, 0, 0)
	WHITE = (255, 255, 255)
	RED = (255, 0, 0)
	BLUE = (0, 255, 0)
	GREEN = (0, 0, 255)

class Direction(Enum):	#Direction.LEFT, Direction.STANDING, Direction.RIGHT
	LEFT = 0
	STANDING = 1
	RIGHT = 2

class Player(object):
	def __init__(self, posx, posy, width, height, velocity):
		self.posx = posx
		self.posy = posy
		self.width = width
		self.height = height
		self.velocity = velocity

		self.isJump = False
		self.direction = [0, 1, 0]
		self.walkCount = 0

	def draw(self, win):
		coordinate = (self.posx, self.posy)
		if self.walkCount  + 1 >= 27:
			self.walkCount = 0
		if not self.direction[1]:
			if self.direction[0]:
				win.blit(walkLeft[self.walkCount//3], coordinate)
				self.walkCount += 1
			elif self.direction[2]:
				win.blit(walkRight[self.walkCount//3], coordinate)
				self.walkCount += 1
		else:
			if self.direction[0]:
				win.blit(walkLeft[0], coordinate)
			elif self.direction[2]:
				win.blit(walkRight[0], coordinate)

class Projectile(object):
	def __init__(self, posx, posy, radius, facing, color):
		self.posx = posx
		self.posy = posy
		self.radius = radius
		self.facing = facing
		self.color = color

		self.velocity = 15 * facing

	def draw(self, win):
		coordinate = (self.posx, self.posy)	
		pygame.draw.circle(win, self.color, coordinate, self.radius)

def redrawGameWindow():
	win.blit(bg, (0, 0))
	player1.draw(win)
	for i in range(len(bullets)):
		bullets[i].draw(win)
	pygame.display.update()

if __name__ == '__main__':
	pygame.init()

	pil = pygame.image.load
	try:
		walkRight = [pil(f'R{i}.png') for i in range(1, 10)]
		walkLeft = [pil(f'L{i}.png') for i in range(1, 10)]
		bg = pil('bg.jpg')
		char = pil('standing.png')
	except Exception as e:
		print("Error while loading images: ", e)

	clock = pygame.time.Clock()

	winx = 500
	winy = 480
	player1 = Player(50, 400, 40, 60, 10)
	bullets = []
	jump_gravity = 5
	jump_height = 30
	jump_velocity = jump_height
	total_bullets = 8
	frame_rate = 27

	win = pygame.display.set_mode((winx, winy))
	pygame.display.set_caption(("First Game"))

	run = True
	while run:
		clock.tick(frame_rate)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		for i, bullet in reversed(list(enumerate(bullets))):
			if not (0 < bullet.posx < winx):
				bullets.pop(i)
			else:
				bullet.posx += bullet.velocity

		error_xplus = 10
		error_xminus = 0
		keys = pygame.key.get_pressed()

		if keys[pygame.K_SPACE]:
			if player1.direction[0]:
				facing = -1
			else:
				facing = 1
			if len(bullets) < total_bullets:
				bullet = Projectile(
					player1.posx + player1.width // 2, 
					player1.posy + player1.height // 2, 
					6, facing, Color.RED.value)
				bullets.append(bullet)

		if keys[pygame.K_LEFT] and player1.posx - player1.velocity + error_xminus >= 0:
			player1.posx -= player1.velocity
			player1.direction = [1, 0, 0]
		elif keys[pygame.K_RIGHT] and player1.posx + player1.width + player1.velocity + error_xplus <= winx:	
			player1.posx += player1.velocity
			player1.direction = [0, 0, 1]
		else:
			player1.direction[1] = True
			player1.walkCount = 0
			pass

		if keys[pygame.K_UP]:
			player1.isJump = True
		if player1.isJump:
			player1.posy -= jump_velocity
			jump_velocity -= jump_gravity
			if jump_velocity < -jump_height:
				player1.isJump = False
				jump_velocity = jump_height

		redrawGameWindow()

	print("Good Bye!")

	pygame.quit()
