import pygame

print("Hello World")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 255, 0)
GREEN = (0, 0, 255)
WINX = 500
WINY = 480

jump_gravity = 5
jump_height = 30
jump_velocity = jump_height

class Player(object):
	def __init__(self, posx, posy, width, height, velocity):
		self.posx = posx
		self.posy = posy
		self.width = width
		self.height = height
		self.velocity = velocity
		self.isJump = False
		self.left = False
		self.right = False
		self.walkCount = 0

	def draw(self, win):
		if self.walkCount  + 1 >= 27:
			self.walkCount = 0
		if self.left:
			win.blit(walkLeft[self.walkCount//3], (self.posx, self.posy))
			self.walkCount += 1
		elif self.right:
			win.blit(walkRight[self.walkCount//3], (self.posx, self.posy))
			self.walkCount += 1
		else:
			win.blit(char, (self.posx, self.posy))

def redrawGameWindow():
	win.blit(bg, (0, 0))
	player1.draw(win)
	pygame.display.update()

if __name__ == '__main__':
	pygame.init()

	win = pygame.display.set_mode((WINX, WINY))
	pygame.display.set_caption(("First Game"))

	pil = pygame.image.load
	walkRight = [pil('R1.png'), pil('R2.png'), pil('R3.png'), pil('R4.png'), pil('R5.png'), pil('R6.png'), pil('R7.png'), pil('R8.png'), pil('R9.png')]
	walkLeft = [pil('L1.png'), pil('L2.png'), pil('L3.png'), pil('L4.png'), pil('L5.png'), pil('L6.png'), pil('L7.png'), pil('L8.png'), pil('L9.png')]
	bg = pil('bg.jpg')
	char = pil('standing.png')

	clock = pygame.time.Clock()

	player1 = Player(50, 400, 40, 60, 10)
	run = True
	while run:
		clock.tick(27)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		error_xplus = 10
		error_xminus = 0
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT] and player1.posx - player1.velocity + error_xminus >= 0:
			# print("REACHED")
			player1.posx -= player1.velocity
			player1.left = True
			player1.right = False
		elif keys[pygame.K_RIGHT] and player1.posx + player1.width + player1.velocity + error_xplus <= WINX:	
			# print("REACHED")
			player1.posx += player1.velocity
			player1.left = False
			player1.right = True
		else:
			# print("REACHED")
			player1.left = False
			player1.right = False
		if keys[pygame.K_SPACE]:
			# print("REACHED")
			player1.isJump = True
		if player1.isJump:
			player1.posy -= jump_velocity
			jump_velocity -= jump_gravity
			if jump_velocity < -jump_height:
				player1.isJump = False
				jump_velocity = jump_height
		else:
			pass
		redrawGameWindow()

	print("Good Bye!")

	pygame.quit()
