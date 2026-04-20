# import libraries
import pygame
import time
import random

# snake speed
snake_speed = 15

# window size
window_x = 720
window_y = 480

# colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# init pygame
pygame.init()

# create window
pygame.display.set_caption('Змейка')
game_window = pygame.display.set_mode((window_x, window_y))

# FPS controller
fps = pygame.time.Clock()

# snake start position
snake_position = [100, 50]

# initial snake body
snake_body = [[100, 50],
              [90, 50],
              [80, 50],
              [70, 50]
              ]

# normal fruit position
fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                  random.randrange(1, (window_y // 10)) * 10]

fruit_spawn = True

# disappearing fruit position
t_fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                    random.randrange(1, (window_y // 10)) * 10]

t_fruit_spawn = True
t_fruit_weight = 25  # extra points fruit

# direction
direction = 'RIGHT'
change_to = direction

# score
score = 0

# level system
level = 1

# font
font = pygame.font.Font(None, 30)

# draw text function
def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, 'white')
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# show score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    game_window.blit(score_surface, score_rect)

# game over function
def game_over():
    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render(
        'Your Score is : ' + str(score), True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_x / 2, window_y / 4)

    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()

    time.sleep(2)
    pygame.quit()
    quit()

# timer for disappearing fruit
counter = 7
timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event, 1000)
foo = False  # controls visibility

# fruit scores
fruit_weight_list = [10, 15, 20]

# main loop
while True:

    # handle events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

        # timer event for disappearing fruit
        elif event.type == timer_event:
            counter -= 1

            if counter >= 8:
                foo = True
            else:
                foo = False

            if counter == 0:
                counter = 12

    # prevent opposite direction
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # move snake
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10

    # grow snake
    snake_body.insert(0, list(snake_position))

    # check normal fruit collision
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += random.choice(fruit_weight_list)
        fruit_spawn = False
    else:
        snake_body.pop()

    # respawn fruit
    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                          random.randrange(1, (window_y // 10)) * 10]

    fruit_spawn = True

    # clear screen
    game_window.fill(black)

    # disappearing fruit logic
    if foo:
        if snake_position[0] == t_fruit_position[0] and snake_position[1] == t_fruit_position[1]:
            counter = 7
            score += t_fruit_weight
            t_fruit_spawn = False

        pygame.draw.rect(game_window, 'orange',
                         (t_fruit_position[0], t_fruit_position[1], 10, 10))

        if not t_fruit_spawn:
            counter = 7
            t_fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                                random.randrange(1, (window_y // 10)) * 10]

        t_fruit_spawn = True

    # draw snake
    for pos in snake_body:
        pygame.draw.rect(game_window, green,
                         pygame.Rect(pos[0], pos[1], 10, 10))

    # draw normal fruit
    pygame.draw.rect(game_window, white,
                     pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

    # wall collision
    if snake_position[0] < 0 or snake_position[0] > window_x - 10:
        game_over()
    if snake_position[1] < 0 or snake_position[1] > window_y - 10:
        game_over()

    # self collision
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    # level up
    if score >= level * 3:
        level += 1
        snake_speed += 5

    # draw level
    drawText('Level %s' % (level), font, game_window, 640, 10)

    # show score
    show_score(1, white, 'times new roman', 20)

    # update screen
    pygame.display.update()

    # control FPS
    fps.tick(snake_speed)