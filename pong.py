import pygame, random

def ball_animation():
	global ball_speed_x, ball_speed_y, left_player_score, right_player_score, score_time
	
	ball.x += ball_speed_x
	ball.y += ball_speed_y

	if ball.top <= 0 or ball.bottom >= screen_height:
		ball_speed_y *= -1
		
	# Left Player Score
	if ball.right <= 0: 
		score_time = pygame.time.get_ticks()
		left_player_score += 1
		
	# right player Score
	if ball.left >= screen_width:
		score_time = pygame.time.get_ticks()
		right_player_score += 1
		
	if ball.colliderect(left_player) and ball_speed_x < 0:
		if abs(ball.right - left_player.right) < 10:
			ball_speed_x *= -1	
		elif abs(ball.bottom - left_player.top) < 10 and ball_speed_y > 0:
			ball_speed_y *= -1
		elif abs(ball.top - left_player.bottom) < 10 and ball_speed_y < 0:
			ball_speed_y *= -1

	if ball.colliderect(right_player) and ball_speed_x > 0:
		if abs(ball.left - right_player.left) < 10:
			ball_speed_x *= -1	
		elif abs(ball.bottom - right_player.top) < 10 and ball_speed_y > 0:
			ball_speed_y *= -1
		elif abs(ball.top - right_player.bottom) < 10 and ball_speed_y < 0:
			ball_speed_y *= -1
		

def player_animation():
	keys = pygame.key.get_pressed()
	if keys[pygame.K_DOWN] and right_player.bottom + PLAYER_VELOSITY < screen_height:
		right_player.y += PLAYER_VELOSITY
	if keys[pygame.K_UP] and right_player.top - PLAYER_VELOSITY > 0:
		right_player.y -= PLAYER_VELOSITY
	if keys[pygame.K_s] and left_player.bottom + PLAYER_VELOSITY < screen_height:
		left_player.y += PLAYER_VELOSITY
	if keys[pygame.K_w] and left_player.top - PLAYER_VELOSITY > 0:
		left_player.y -= PLAYER_VELOSITY

def ball_start():
	global ball_speed_x, ball_speed_y, ball_moving, score_time

	ball.center = (screen_width//2, screen_height//2)
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

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    screen.blit(draw_text, (screen_width/2 - draw_text.get_width() /
                         2, screen_height/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

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
ball = pygame.Rect(screen_width // 2 - 10, screen_height // 2 - 10, 20, 20)
right_player = pygame.Rect(screen_width - 30, screen_height // 2 - 70, 20,100)
left_player = pygame.Rect(10, screen_height // 2 - 70, 20,100)

# Game Variables
ball_speed_x = 7 * random.choice((1,-1))
ball_speed_y = 7 * random.choice((1,-1))
FPS = 60
PLAYER_VELOSITY = 6
ball_moving = False
score_time = True

# Score Text
left_player_score = 0
right_player_score = 0
basic_font = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

run = True
while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False			
	
	#Game Logic
	ball_animation()
	player_animation()

	# Visuals 
	screen.fill(0)
	pygame.draw.rect(screen, WHITE, left_player)
	pygame.draw.rect(screen, WHITE, right_player)
	pygame.draw.rect(screen, WHITE, ball)
	pygame.draw.line(screen, WHITE, (screen_width / 2, 0),(screen_width / 2, screen_height), 5)

	if score_time:
		ball_start()

	left_player_text = basic_font.render(f'{left_player_score}',False,WHITE)
	screen.blit(left_player_text,(screen_width // 2 + 30, 10))

	right_player_text = basic_font.render(f'{right_player_score}',False,WHITE)
	screen.blit(right_player_text,(screen_width // 2 - 30, 10))

	winner_text = ""
	if left_player_score == 5:
		winner_text = "Left Wins!"

	if right_player_score == 5:
		winner_text = "Right Wins!"

	if winner_text != "":
		draw_winner(winner_text)                       
		break

	pygame.display.flip()
	clock.tick(FPS)

pygame.quit()
