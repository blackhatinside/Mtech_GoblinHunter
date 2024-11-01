import pygame

print("Hello World")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

winx = 500
winy = 480
posx = 50
posy = 400
width = 40
height = 60
vel = 10
# jumpCount = 10
isJump = False
left = False
right = False
walkCount = 0
jump_gravity = 5
jump_height = 30
jump_velocity = jump_height

pygame.init()

win = pygame.display.set_mode((winx, winy))
pygame.display.set_caption(("First Game"))

pil = pygame.image.load
walkRight = [pil('R1.png'), pil('R2.png'), pil('R3.png'), pil('R4.png'), pil('R5.png'), pil('R6.png'), pil('R7.png'), pil('R8.png'), pil('R9.png')]
walkLeft = [pil('L1.png'), pil('L2.png'), pil('L3.png'), pil('L4.png'), pil('L5.png'), pil('L6.png'), pil('L7.png'), pil('L8.png'), pil('L9.png')]
bg = pil('bg.jpg')
char = pil('standing.png')

clock = pygame.time.Clock()

def redrawGameWindow():
	global walkCount
	# win.fill(BLACK)
	win.blit(bg, (0, 0))
	# pygame.draw.rect(win, RED, (posx, posy, width, height))
	if walkCount  + 1 >= 27:
		walkCount = 0
	if left:
		win.blit(walkLeft[walkCount//3], (posx, posy))
		walkCount += 1
	elif right:
		win.blit(walkRight[walkCount//3], (posx, posy))
		walkCount += 1
	else:
		win.blit(char, (posx, posy))
		walkCount = 0

	pygame.display.update()

run = True
while run:
	clock.tick(27)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	error_xplus = 10
	error_xminus = 0
	keys = pygame.key.get_pressed()
	if keys[pygame.K_LEFT] and posx - vel + error_xminus >= 0:
		# print("REACHED")
		posx -= vel
		left = True
		right = False
	elif keys[pygame.K_RIGHT] and posx + width + vel + error_xplus <= winx:	
		# print("REACHED")
		posx += vel
		left = False
		right = True
	else:
		# print("REACHED")
		left = False
		right = False
		# walkCount = 0
	# if keys[pygame.K_UP] and posy - vel >= 0:
	# 	posy -= vel
	# if keys[pygame.K_DOWN] and posy + height + vel <= winy:
	# 	posy += vel
	if keys[pygame.K_SPACE]:
		# print("REACHED")
		isJump = True
	if isJump:
		# print(f"posy: 	{posy} \t jump_velocity: {jump_velocity} \n")
		posy -= jump_velocity
		jump_velocity -= jump_gravity
		if jump_velocity < -jump_height:
			isJump = False
			jump_velocity = jump_height
	else:
		# print("REACHED")
		# left = False
		# right = False
		# walkCount = 0
		pass
	# print(f"left: {left} \t right: {right} \n")
	redrawGameWindow()


print("Good Bye!")

pygame.quit()
