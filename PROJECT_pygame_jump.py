import pygame

print("Hello World")

WINX = 500
WINY = 500
POSX = 50
POSY = 50
WIDTH = 40
HEIGHT = 60
VEL = 10
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
# jumpCount = 10
isJump = False
JUMP_GRAVITY = 5
JUMP_HEIGHT = 30
JUMP_VELOCITY = JUMP_HEIGHT

pygame.init()

win = pygame.display.set_mode((WINX, WINY))
pygame.display.set_caption(("First Game"))

run = True
while run:
	pygame.time.delay(100)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	keys = pygame.key.get_pressed()
	if keys[pygame.K_LEFT] and POSX - VEL >= 0:
		POSX -= VEL
	if keys[pygame.K_RIGHT] and POSX + WIDTH + VEL <= WINX:
		POSX += VEL
	if keys[pygame.K_UP] and POSY - VEL >= 0:
		POSY -= VEL
	if keys[pygame.K_DOWN] and POSY + HEIGHT + VEL <= WINY:
		POSY += VEL
	if keys[pygame.K_SPACE]:
		isJump = True
	if isJump:
		print(f"POSY: {POSY} \n JUMP_VELOCITY: {JUMP_VELOCITY} \n")
		POSY -= JUMP_VELOCITY
		JUMP_VELOCITY -= JUMP_GRAVITY
		if JUMP_VELOCITY < -JUMP_HEIGHT:
			isJump = False
			JUMP_VELOCITY = JUMP_HEIGHT
	win.fill(BLACK)
	pygame.draw.rect(win, RED, (POSX, POSY, WIDTH, HEIGHT))
	pygame.display.update()


print("Good Bye!")

pygame.quit()
