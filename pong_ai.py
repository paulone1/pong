import pygame, random

def ball_animation():
	global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
	
	ball.x += ball_speed_x
	ball.y += ball_speed_y

	if ball.top <= 0 or ball.bottom >= screen_height:
		ball_speed_y *= -1
		
	# Player Score
	if ball.left <= 0: 
		score_time = pygame.time.get_ticks()
		player_score += 1
		
	# Opponent Score
	if ball.right >= screen_width:
		score_time = pygame.time.get_ticks()
		opponent_score += 1
		
	if ball.colliderect(player) and ball_speed_x > 0:
		if abs(ball.right - player.left) < 10:
			ball_speed_x *= -1	
		elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
			ball_speed_y *= -1
		elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
			ball_speed_y *= -1

	if ball.colliderect(opponent) and ball_speed_x < 0:
		if abs(ball.left - opponent.right) < 10:
			ball_speed_x *= -1	
		elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
			ball_speed_y *= -1
		elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
			ball_speed_y *= -1
		

def player_animation():
	player.y += player_speed

	if player.top <= 0:
		player.top = 0
	if player.bottom >= screen_height:
		player.bottom = screen_height

def opponent_ai():
	if opponent.top < ball.y:
		opponent.y += opponent_speed
	if opponent.bottom > ball.y:
		opponent.y -= opponent_speed

	if opponent.top <= 0:
		opponent.top = 0
	if opponent.bottom >= screen_height:
		opponent.bottom = screen_height

def ball_start():
	global ball_speed_x, ball_speed_y, ball_moving, score_time

	ball.center = (screen_width/2, screen_height/2)
	current_time = pygame.time.get_ticks()

	if current_time - score_time < 700:
		number_three = basic_font.render("3",False,WHITE)
		screen.blit(number_three,(screen_width/2 - 10, screen_height/2 + 20))
	if 700 < current_time - score_time < 1400:
		number_two = basic_font.render("2",False,WHITE)
		screen.blit(number_two,(screen_width/2 - 10, screen_height/2 + 20))
	if 1400 < current_time - score_time < 2100:
		number_one = basic_font.render("1",False,WHITE)
		screen.blit(number_one,(screen_width/2 - 10, screen_height/2 + 20))

	if current_time - score_time < 2100:
		ball_speed_y, ball_speed_x = 0,0
	else:
		ball_speed_x = 7 * random.choice((1,-1))
		ball_speed_y = 7 * random.choice((1,-1))
		score_time = None

# General setup
pygame.mixer.pre_init(44100,-16,1, 1024)
pygame.init()
clock = pygame.time.Clock()

# Main Window
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Pong')

# Colors
WHITE = (255,255,255)

# Game Rectangles
ball = pygame.Rect(screen_width // 2 - 15, screen_height // 2 - 15, 20, 20)
player = pygame.Rect(screen_width - 30, screen_height // 2 - 70, 20,100)
opponent = pygame.Rect(10, screen_height // 2 - 70, 20,100)

# Game Variables
ball_speed_x = 7 * random.choice((1,-1))
ball_speed_y = 7 * random.choice((1,-1))
player_speed = 0
opponent_speed = 7
FPS = 60
ball_moving = False
score_time = True

# Score Text
player_score = 0
opponent_score = 0
basic_font = pygame.font.SysFont('comicsans', 40)

run = True
while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False			
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				player_speed -= 6
			if event.key == pygame.K_DOWN:
				player_speed += 6
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_UP:
				player_speed += 6
			if event.key == pygame.K_DOWN:
				player_speed -= 6
	
	#Game Logic
	ball_animation()
	player_animation()
	opponent_ai()

	# Visuals 
	screen.fill(0)
	pygame.draw.rect(screen, WHITE, player)
	pygame.draw.rect(screen, WHITE, opponent)
	pygame.draw.rect(screen, WHITE, ball)
	pygame.draw.line(screen, WHITE, (screen_width / 2, 0),(screen_width / 2, screen_height), 5)

	if score_time:
		ball_start()

	player_text = basic_font.render(f'{player_score}',False,WHITE)
	screen.blit(player_text,(screen_width // 2 - 30, 10))

	opponent_text = basic_font.render(f'{opponent_score}',False,WHITE)
	screen.blit(opponent_text,(screen_width // 2 + 30, 10))

	pygame.display.flip()
	clock.tick(FPS)

pygame.quit()
