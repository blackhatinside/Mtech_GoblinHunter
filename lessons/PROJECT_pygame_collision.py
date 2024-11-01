import pygame

print("Hello World")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WINX = 500
WINY = 480
pil = pygame.image.load

class Player(object):
	walkLeft = [pil(f'Assets/L{i}.png') for i in range(1, 10)]
	walkRight = [pil(f'Assets/R{i}.png') for i in range(1, 10)]
	def __init__(self, posx, posy, width, height, velocity):
		self.posx = posx
		self.posy = posy
		self.width = width
		self.height = height
		self.velocity = velocity

		self.isJump = False
		self.left = False
		self.right = False
		self.standing = True
		self.walkCount = 0
		self.hitbox = (self.posx + 20, self.posy + 12, 25, 50)

	def draw(self, win):
		if self.walkCount  + 1 >= 27:
			self.walkCount = 0
		if not self.standing:
			if self.left:
				win.blit(self.walkLeft[self.walkCount//3], (self.posx, self.posy))
				self.walkCount += 1
			elif self.right:
				win.blit(self.walkRight[self.walkCount//3], (self.posx, self.posy))
				self.walkCount += 1
		else:
			if self.left:
				win.blit(self.walkLeft[0], (self.posx, self.posy))
			elif self.right:
				win.blit(self.walkRight[0], (self.posx, self.posy))
		self.hitbox = (self.posx + 20, self.posy + 12, 25, 50)
		pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

class Enemy(object):
	walkLeft = [pil(f'Assets/L{i}E.png') for i in range(1, 12)]
	walkRight = [pil(f'Assets/R{i}E.png') for i in range(1, 12)]

	def __init__(self, posx, posy, width, height, end, velocity):
		self.posx = posx
		self.posy = posy
		self.width = width
		self.height = height
		self.end = end
		self.velocity = velocity

		self.path = [self.posx, self.end]
		self.walkCount = 0
		self.hitbox = (self.posx + 17, self.posy + 2, 40, 55)

	def draw(self, win):
		self.move()
		if self.walkCount + 1 >= 33:
			self.walkCount = 0
		if self.velocity > 0:
			win.blit(self.walkRight[self.walkCount//3], (self.posx, self.posy))
			self.walkCount += 1
		else:
			win.blit(self.walkLeft[self.walkCount//3], (self.posx, self.posy))
			self.walkCount += 1
		self.hitbox = (self.posx + 17, self.posy + 2, 40, 55)
		pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)


	def move(self):
		if self.velocity > 0:	# move right
			if self.posx + self.velocity < self.path[1]:
				self.posx += self.velocity
			else:	# turn left
				self.velocity = self.velocity * -1
				self.walkCount = 0
		else:	# move left
			if self.posx - self.velocity > self.path[0]:
				self.posx += self.velocity
			else:	# turn right
				self.velocity = self.velocity * -1
				self.WalkCount = 0
				
	def hit(self):
		print("Hit!")

class Projectile(object):
	def __init__(self, posx, posy, radius, facing, color, velocitymultiplier):
		self.posx = posx
		self.posy = posy
		self.radius = radius
		self.facing = facing
		self.color = color
		self.velocitymultiplier = velocitymultiplier

		self.velocity = velocitymultiplier * facing

	def draw(self, win):
		pygame.draw.circle(win, self.color, (self.posx, self.posy), self.radius)

def redrawGameWindow():
	bg = pil('Assets/bg.jpg')
	char = pil('Assets/standing.png')
	win.blit(bg, (0, 0))
	player1.draw(win)
	goblin.draw(win)
	for i in range(len(bullets)):
		bullets[i].draw(win)
	pygame.display.update()

if __name__ == '__main__':
	pygame.init()

	win = pygame.display.set_mode((WINX, WINY))
	pygame.display.set_caption(("First Game"))

	clock = pygame.time.Clock()

	player1 = Player(50, 400, 64, 64, 10)
	goblin = Enemy(100, 400, 64, 64, 300, 5)
	bullets = []
	jump_gravity = 5
	jump_height = 30
	jump_velocity = jump_height
	total_bullets = 8
	fireratecontroller = 0

	run = True
	while run:
		clock.tick(27)

		if fireratecontroller > 0:
			fireratecontroller += 1
		if fireratecontroller > 4:
			fireratecontroller = 0

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		for i, bullet in reversed(list(enumerate(bullets))):
			# is Top of Bullet inside Bottom Line of Goblin's Hitbox
			isBulletTopInside = bullet.posy - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3]
			# is Bottom of Bullet inside Top Line of Goblin's Hitbox
			isBulletBottomInside = bullet.posy + bullet.radius > goblin.hitbox[1]
			# is Left of Bullet inside Right Line of Goblin's Hitbox
			isBulletLeftInside = bullet.posx - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]
			# is Right of Bullet inside Left Line of Goblin's Hitbox
			isBulletRightInside = bullet.posx + bullet.radius > goblin.hitbox[0]
			if isBulletTopInside and isBulletBottomInside:
				if isBulletLeftInside and isBulletRightInside:
					goblin.hit()
					bullets.pop(i)
			if not 0 < bullet.posx < WINX:
				bullets.pop(i)
			else:
				bullet.posx += bullet.velocity

		error_xplus = 10
		error_xminus = 0
		keys = pygame.key.get_pressed()

		if keys[pygame.K_SPACE] and fireratecontroller == 0:
			if player1.left:
				facing = -1
			else:
				facing = 1
			if len(bullets) < total_bullets:
				bullet = Projectile(round(player1.posx + player1.width // 2), round(player1.posy + player1.height // 2), 6, facing, BLUE, 15)
				bullets.append(bullet)
			fireratecontroller += 1

		if keys[pygame.K_LEFT] and player1.posx - player1.velocity + error_xminus >= 0:
			# print("REACHED")
			player1.posx -= player1.velocity
			player1.left = True
			player1.right = False
			player1.standing = False
		elif keys[pygame.K_RIGHT] and player1.posx + player1.width + player1.velocity + error_xplus <= WINX:	
			# print("REACHED")
			player1.posx += player1.velocity
			player1.left = False
			player1.right = True
			player1.standing = False
		else:
			# print("REACHED")
			player1.standing = True
			player1.walkCount = 0
			pass

		if keys[pygame.K_UP]:
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
