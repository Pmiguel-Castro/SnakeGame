import pygame
from collections import deque
from random import randint 

#Plataforma do Jogo
pygame.init()
screen_width = 640
screen_height = 480
n_pixels = 20 
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake 2")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 48)

#Funções
def grab_apple(snake, score, height, width, apple):
    in_snake = True
    while in_snake:
        apple = (randint(0, width-1), randint(0, height-1))
        if apple not in snake: 
            in_snake = False
    score += 10
    text_score = font.render(f"Score: {score}", True, (255, 255, 255))
    return apple, score, text_score

def walk(snake, is_horizontal, is_positive):
    snk_head_x, snk_head_y = snake[-1]
    if is_horizontal == False and is_positive == True:
        snake.append((snk_head_x, snk_head_y+1))
    elif is_horizontal == False and is_positive == False:
        snake.append((snk_head_x, snk_head_y-1))
    elif is_horizontal == True and is_positive == True:
        snake.append((snk_head_x+1, snk_head_y))
    else:
        snake.append((snk_head_x-1, snk_head_y))

def in_game():
    #Estado Global (Variaveis)
    height = screen_height // n_pixels
    width = screen_width // n_pixels
    snake = deque([(0,0)])
    apple = (randint(1, width-1), randint(1, height-1))
    score = 0
    text_score = font.render(f"Score: {score}", True, (255, 255, 255))
    alive = True
    win = False
    is_horizontal = False
    is_positive = True
    
    while alive:
        #Definir a direção apartir da tecla apertada
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return alive, win, score
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    is_horizontal = False
                    is_positive = False
                elif event.key == pygame.K_DOWN:
                    is_horizontal = False
                    is_positive = True
                elif event.key == pygame.K_RIGHT:
                    is_horizontal = True
                    is_positive = True
                elif event.key == pygame.K_LEFT:
                    is_horizontal = True
                    is_positive = False
        
        #Chamar a função de andar
        walk(snake, is_horizontal, is_positive)

        #Analisar se ela enconsta nela mesma
        for i in range(len(snake)-1):
            if snake[-1] == snake[i]:
                alive = False
                break

        #Analisar se ela pega a maçã    
        if snake[-1] == apple:
            apple, score, text_score= grab_apple(snake, score, height, width, apple)
        
        #Analisar se ela bate em alguma parede
        elif snake[-1][0] >= width or snake[-1][1] >= height or snake[-1][0] < 0 or snake[-1][1] < 0:
            alive = False 
            break
        
        #Condição de vitória
        elif len(snake) == width*height:
            win = True
            break
        
        #Finalização da caminhada
        else:
            snake.popleft()

        #Visualização do Jogo
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 0, 0), (apple[0]*n_pixels, apple[1]*n_pixels, n_pixels, n_pixels))
        screen.blit(text_score, (10, 10))
        for snk_part in snake:
            if snk_part == snake[-1]:
                pygame.draw.rect(screen, (0, 128, 0), (snk_part[0]*n_pixels, snk_part[1]*n_pixels, n_pixels, n_pixels))    
            else:
                pygame.draw.rect(screen, (0, 255, 0), (snk_part[0]*n_pixels, snk_part[1]*n_pixels, n_pixels, n_pixels))
        #for i in range(width+2):
        #   pygame.draw.rect(screen, (128, 128, 128), (0, i*n_pixels, n_pixels, n_pixels))
        #   pygame.draw.rect(screen, (128, 128, 128), ((width+1)*n_pixels, i*n_pixels, n_pixels, n_pixels))
        #for i in range(height+2):    
        #   pygame.draw.rect(screen, (128, 128, 128), (i*n_pixels, (height+1)*n_pixels, n_pixels, n_pixels))
        #   pygame.draw.rect(screen, (128, 128, 128),(i*n_pixels, 0, n_pixels, n_pixels))
        pygame.display.flip()
        clock.tick(10)
    return alive, win, score

#Lógica do jogo:
playing = True
while playing:
    alive, win, score = in_game()

    if alive == False:
        screen.fill((0, 0, 0)) 
        text_death = font.render("Game Over!", True, (255, 255, 255))
        text_score = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(text_death, (screen_width//2-100, screen_height//2))
        screen.blit(text_score, (screen_width//2-100, screen_height//2 + 2*n_pixels))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        playing = True
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        playing = False
                        waiting = False

    elif win == True:
        screen.fill((0, 0, 0)) 
        text_win = font.render("You Win!", True, (255, 255, 255))
        screen.blit(text_win, (screen_width//2, screen_height//2))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        playing = True
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        playing = False
                        waiting = False
    else:
        playing = False
      
