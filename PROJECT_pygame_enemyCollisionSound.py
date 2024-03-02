import pygame

print("Hello World")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 128, 0)
BLUE = (0, 0, 255)
WINX = 500
WINY = 480
pil = pygame.image.load

class Player(object):
	walkLeft = [pil(f'Assets/L{i}.png') for i in range(1, 10)]
	walkRight = [pil(f'Assets/R{i}.png') for i in range(1, 10)]
	standStill = pil('Assets/standing.png')

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
		coordinate_player = (self.posx, self.posy)
		if self.walkCount  + 1 >= 27:
			self.walkCount = 0
		if not self.standing:
			if self.left:
				win.blit(self.walkLeft[self.walkCount//3], coordinate_player)
				self.walkCount += 1
			elif self.right:
				win.blit(self.walkRight[self.walkCount//3], coordinate_player)
				self.walkCount += 1
			# else:
			# 	win.blit(self.standStill, coordinate_player)
			# 	walkCount = 0
		else:
			if self.left:
				win.blit(self.walkLeft[0], coordinate_player)
			elif self.right:
				win.blit(self.walkRight[0], coordinate_player)
			else:
				win.blit(self.standStill, coordinate_player)
				walkCount = 0

		self.hitbox = (self.posx + 20, self.posy + 12, 25, 50)
		# pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

	def hit(self, damage):		# when player gets hit
		self.x = 50
		self.y = 400
		self.walkCount = 0
		font = pygame.font.SysFont('comicsans', 100)
		text = font.render(str(-damage), 1, RED)
		win.blit(text, (WINX//2 - (text.get_width()//2), WINY))
		pygame.display.update()
		try:
			i = 0
			while i < 500:
				pygame.time.delay(10)
				i += 1
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						i = 201
						pygame.quit()
		except Exception as e:
			print("Error: ", e)
		finally:
			print("Goblin caught you, wait 5s")

class Enemy(object):
	walkLeft = [pil(f'Assets/L{i}E.png') for i in range(1, 12)]
	walkRight = [pil(f'Assets/R{i}E.png') for i in range(1, 12)]

	def __init__(self, posx, posy, width, height, end, velocity, health, damage):
		self.posx = posx
		self.posy = posy
		self.width = width
		self.height = height
		self.end = end
		self.velocity = velocity
		self.health = health
		self.damage = damage

		self.path = [self.posx, self.end]
		self.walkCount = 0
		self.hitbox = (self.posx + 17, self.posy + 2, 40, 55)
		self.visible = True

	def draw(self, win):
		self.move()
		coordinate_enemy = (self.posx, self.posy)
		if self.visible:
			if self.walkCount + 1 >= 33:
				self.walkCount = 0
			if self.velocity > 0:
				win.blit(self.walkRight[self.walkCount//3], coordinate_enemy)
				self.walkCount += 1
			else:
				win.blit(self.walkLeft[self.walkCount//3], coordinate_enemy)
				self.walkCount += 1
			pygame.draw.rect(win, RED, (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
			pygame.draw.rect(win, DARKGREEN, (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
			self.hitbox = (self.posx + 17, self.posy + 2, 40, 55)
		# pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)


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
				
	def hit(self, damage):		# when goblin gets hit
		if self.health - damage > 0:
			self.health -= damage
		else:
			self.visible = False
		print("Hit!")

class Projectile(object):
	def __init__(self, posx, posy, radius, facing, color, velocitymultiplier, damage):
		self.posx = posx
		self.posy = posy
		self.radius = radius
		self.facing = facing
		self.color = color
		self.velocitymultiplier = velocitymultiplier
		self.damage = damage

		self.velocity = velocitymultiplier * facing

	def draw(self, win):
		coordinate_projectile = (self.posx, self.posy)
		pygame.draw.circle(win, self.color, coordinate_projectile, self.radius)

def redrawGameWindow():
	coordinate_bg = (0, 0)
	coordinate_score = (300, 10)
	bg = pil('Assets/bg.jpg')
	text = font.render(f'Score: {score}', 1, BLACK)
	win.blit(bg, coordinate_bg)
	player1.draw(win)
	goblin.draw(win)
	win.blit(text, coordinate_score)
	for i in range(len(bullets)):
		bullets[i].draw(win)
	pygame.display.update()

if __name__ == '__main__':
	pygame.init()

	win = pygame.display.set_mode((WINX, WINY))
	pygame.display.set_caption(("First Game"))
	bulletSound = pygame.mixer.Sound('Assets/bullet.mp3')
	hitSound = pygame.mixer.Sound('Assets/hit.mp3')
	pygame.mixer.music.load('Assets/bgm.mp3')
	pygame.mixer.music.play(-1)		# -1 for looping song

	clock = pygame.time.Clock()

	font = pygame.font.SysFont('comicsans', 32, True)	# font-name, font-size, isBold?
	player1 = Player(50, 400, 64, 64, 10)
	goblin = Enemy(100, 400, 64, 64, 300, 5, 10, 5)
	bullets = []
	jump_gravity = 5
	jump_height = 30
	jump_velocity = jump_height
	total_bullets = 8
	fireratecontroller = 0
	score = 0

	run = True
	while run:
		clock.tick(27)

		# is Top of Player inside Bottom Line of Goblin's Hitbox
		isPlayerTopInside = player1.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3]
		# is Bottom of Player inside Top Line of Goblin's Hitbox
		isPlayerBottomInside = player1.hitbox[1] + player1.hitbox[3] > goblin.hitbox[1]
		# is Left of Player inside Right Line of Goblin's Hitbox
		isPlayerLeftInside = player1.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]
		# is Right of Player inside Left Line of Goblin's Hitbox
		isPlayerRightInside = player1.hitbox[0] + player1.hitbox[2] > goblin.hitbox[0]
		if isPlayerTopInside and isPlayerBottomInside:
			if isPlayerLeftInside and isPlayerRightInside:
				player1.hit(goblin.damage)
				score -= goblin.damage

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
					hitSound.play()
					goblin.hit(bullet.damage)
					score += 1
					bullets.pop(i)
			if not 0 < bullet.posx < WINX:
				bullets.pop(i)
			else:
				bullet.posx += bullet.velocity

		error_xplus = 10
		error_xminus = 0
		keys = pygame.key.get_pressed()

		if keys[pygame.K_SPACE] and fireratecontroller == 0:
			bulletSound.play()
			if player1.left:
				facing = -1
			else:
				facing = 1
			if len(bullets) < total_bullets:
				bullet = Projectile(round(player1.posx + player1.width // 2), round(player1.posy + player1.height // 2), 6, facing, BLUE, 15, 1)
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
