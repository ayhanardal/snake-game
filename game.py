import pygame
import numpy as np
from sys import exit

pygame.init()

# variables

height = 900
witdh = 900
h_2 = 450
w_2 = 450
speed = 10    
snake_rotate = 0 # | 0 = Right | 1 = Left | 2 = Up | 3 = Down
game_mode = 0 # | 0 = pause | 1 = game
snake_movex = 0 
snake_movey = 0

moves_x_time = 14
moves_y_time = 14

display = pygame.display.set_mode(size = (witdh,height))
clock = pygame.time.Clock()

# position matrix

posy = np.zeros((30,30),dtype='int')
posx = np.zeros((30,30),dtype='int')
pos_x_inc = 0
pos_y_inc = 0

for i in range(30):

    pos_y_inc += 30
    pos_x_inc += 30
    posy[i] = pos_y_inc

    for j in range(30):
        posx[j,i] = pos_x_inc

# assets

font = pygame.font.SysFont('comicsansms',72)

text = font.render('Press Space',True,(230,230,230))
text_rect = text.get_rect(centerx = w_2, centery= h_2)

snake_head = pygame.Surface(size=(30,30))
snake_head.fill((255,0,0))
snake_head_rect = snake_head.get_rect(bottomright = (posx[1,moves_x_time],posy[moves_y_time,1]))

snake_list = [snake_head_rect, snake_head.get_rect(bottomright = (posx[1,moves_x_time - 1],posy[moves_y_time,1])),snake_head.get_rect(bottomright = (posx[1,moves_x_time - 2],posy[moves_y_time,1])),snake_head.get_rect(bottomright = (posx[1,moves_x_time - 3],posy[moves_y_time,1]))]

apple = pygame.Surface(size=(30,30))
apple.fill((0,255,0))
apple_rect = apple.get_rect(bottomright = (0,0))

apple_r_x = np.random.randint(5,25)
apple_r_y = np.random.randint(5,25)

bg = pygame.Surface(size=(witdh,height))
bg.fill((0,0,0))
bg_rect = bg.get_rect(topleft = (0,0))

# functions

def display_game():

    apple_rect.bottomright = (posx[1,apple_r_x],posy[apple_r_y,1])

    display.blit(bg,bg_rect)        
    display.blit(apple,apple_rect)

    for i in snake_list:
        display.blit(snake_head, i)

def move():
    global moves_x_time, moves_y_time, snake_movex, snake_movey, snake_rotate

    if snake_rotate == 0: # right
        moves_x_time += 1 
        snake_movex = posx[1,moves_x_time]

        a = []

        for i in range(len(snake_list)-1):
            a.append(snake_list[i])

        snake_list[0] = snake_head.get_rect(bottomright =(snake_movex,snake_movey))
        
        for i in range(len(a)):
            snake_list[i+1] = a[i]

    elif snake_rotate == 1: # left
        moves_x_time -= 1  
        snake_movex = posx[1,moves_x_time]
        
        a = []

        for i in range(len(snake_list)-1):
            a.append(snake_list[i])

        snake_list[0] = snake_head.get_rect(bottomright =(snake_movex,snake_movey))
        
        for i in range(len(a)):
            snake_list[i+1] = a[i]

    elif snake_rotate == 2: # up
        moves_y_time -= 1  
        snake_movey = posy[moves_y_time,1]
        
        a = []

        for i in range(len(snake_list)-1):
            a.append(snake_list[i])

        snake_list[0] = snake_head.get_rect(bottomright =(snake_movex,snake_movey))
        
        for i in range(len(a)):
            snake_list[i+1] = a[i]

    elif snake_rotate == 3: # down
        moves_y_time += 1  
        snake_movey = posy[moves_y_time,1]
        
        a = []

        for i in range(len(snake_list)-1):
            a.append(snake_list[i])

        snake_list[0] = snake_head.get_rect(bottomright =(snake_movex,snake_movey))
        
        for i in range(len(a)):
            snake_list[i+1] = a[i]

# game loop

while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()            

        if event.type == pygame.KEYDOWN:
                
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            
            if event.key == pygame.K_SPACE:
                snake_movex = posx[1,moves_x_time]
                snake_movey = posy[moves_y_time,1]
                game_mode = 1

            if event.key == pygame.K_RIGHT and (snake_rotate != 1):
                snake_rotate = 0

            if event.key == pygame.K_LEFT and (snake_rotate != 0):
                snake_rotate = 1
            
            if event.key == pygame.K_UP and (snake_rotate != 3):
                snake_rotate = 2
            
            if event.key == pygame.K_DOWN and (snake_rotate != 2):
                snake_rotate = 3
            
            

    if game_mode == 0:
        display.blit(bg,bg_rect)
        display.blit(text,text_rect)
        snake_movex = 0 
        snake_movey = 0
        moves_x_time = 14
        moves_y_time = 14
        snake_rotate = 0
        snake_head_rect = snake_head.get_rect(bottomright = (posx[1,moves_x_time],posy[moves_y_time,1]))
        snake_list = []
        snake_list = [snake_head_rect, snake_head.get_rect(bottomright = (posx[1,moves_x_time - 1],posy[moves_y_time,1])),snake_head.get_rect(bottomright = (posx[1,moves_x_time - 2],posy[moves_y_time,1])),snake_head.get_rect(bottomright = (posx[1,moves_x_time - 3],posy[moves_y_time,1]))]
        a = []

    elif game_mode == 1:

        move()

        display_game()
            
        # snake growing

        if snake_list[0].colliderect(apple_rect):            
            apple_r_x = np.random.randint(5,25)
            apple_r_y = np.random.randint(5,25)

            snake_list.append(snake_list[-1])

        # game over

        for i in range(len(snake_list)-1):
            if snake_list[0].colliderect(snake_list[i+1]):
                game_mode = 0

        # game area borders

        if snake_list[0].x == 0:
            game_mode = 0
        elif snake_list[0].x == 870:
            game_mode = 0
        elif snake_list[0].y == 90:
            game_mode = 0
        elif snake_list[0].y == 780:
            game_mode = 0

    pygame.display.update()
    clock.tick(speed)
