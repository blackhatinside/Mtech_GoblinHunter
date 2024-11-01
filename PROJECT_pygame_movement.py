import pygame

print("Hello World")

win_x = 500
win_y = 500
x = 50
y = 50
width = 40
height = 60
vel = 10
BLACK = (0, 0, 0)
RED = (255, 0, 0)

pygame.init()

win = pygame.display.set_mode((win_x, win_y))
pygame.display.set_caption(("First Game"))

run = True
while run:
	pygame.time.delay(100)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	keys = pygame.key.get_pressed()
	if keys[pygame.K_LEFT] and x - vel >= 0:
		x -= vel
	if keys[pygame.K_RIGHT] and x + width + vel <= win_x:
		x += vel
	if keys[pygame.K_UP] and y - vel >= 0:
		y -= vel
	if keys[pygame.K_DOWN] and y + height + vel <= win_y:
		y += vel
	win.fill(BLACK)
	pygame.draw.rect(win, RED, (x, y, width, height))
	pygame.display.update()


print("Good Bye!")

pygame.quit()
