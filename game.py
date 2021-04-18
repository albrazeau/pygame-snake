import pygame
import sys
from utils import new_food, Snake

pygame.init()

width = 500
height = 500
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
font_color = (153, 255, 51)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake")

snake_size = 10
snake = Snake(width, height, snake_size, color=white)

food = new_food(width, height, snake_size, snake)

score_font_size = 20
score_font = pygame.font.Font(pygame.font.get_default_font(), score_font_size)

fps_font_size = 12
fps_font = pygame.font.Font(pygame.font.get_default_font(), fps_font_size)

clock = pygame.time.Clock()

score = 0
alive = True
while alive:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            alive = False

    keys = pygame.key.get_pressed()

    # set the snakes direction
    if keys[pygame.K_w] or keys[pygame.K_UP] and snake.direction != "down":
        snake.direction = "up"
    if keys[pygame.K_s] or keys[pygame.K_DOWN] and snake.direction != "up":
        snake.direction = "down"
    if keys[pygame.K_a] or keys[pygame.K_LEFT] and snake.direction != "right":
        snake.direction = "left"
    if keys[pygame.K_d] or keys[pygame.K_RIGHT] and snake.direction != "left":
        snake.direction = "right"

    # grow the snake
    ate_food = snake.collide_other(food)
    if ate_food:
        score += 1
        snake.add_tail()

    # move the snake
    if ate_food:
        snake.move(1)
        snake.add_tail()
        snake.move(1)
        food = new_food(width, height, snake_size, snake)
    else:
        snake.move(2)

    # don't let the snake go off the screen
    if snake.body[0].right > width:
        print("You lose!!!")
        alive = False
    if snake.body[0].left <= 0:
        print("You lose!!!")
        alive = False
    if snake.body[0].top >= height:
        print("You lose!!!")
        alive = False
    if snake.body[0].bottom <= 0:
        print("You lose!!!")
        alive = False

    if snake.collide_self():
        print("Self collision!")
        alive = False

    screen.fill(0)

    pygame.draw.rect(screen, red, food)
    snake.draw(screen)

    score_txt_surface = score_font.render(f"Score: {score}", True, green)
    screen.blit(score_txt_surface, (5, 5))

    fps_txt_surface = fps_font.render(f"FPS: {round(clock.get_fps())}", True, font_color)
    screen.blit(fps_txt_surface, (width - fps_font_size * 4, height - fps_font_size * 1.5))

    pygame.display.flip()


pygame.quit()
sys.exit()
