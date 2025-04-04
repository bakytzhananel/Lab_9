import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 500, 500
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
WHITE = (255, 255, 255)

snake_pos = [100, 100]
snake_body = [[100, 100], [80, 100], [60, 100]]
direction = 'RIGHT'
change_to = direction

food = None
food_spawn_time = 0

score = 0
level = 1
speed = 10

clock = pygame.time.Clock()
running = True

def spawn_food():
    value = random.choice([1, 2, 3])
    color = RED if value == 1 else SILVER if value == 2 else GOLD
    pos = [random.randrange(1, WIDTH // CELL_SIZE) * CELL_SIZE,
           random.randrange(1, HEIGHT // CELL_SIZE) * CELL_SIZE]
    timer = 150
    return {'pos': pos, 'value': value, 'color': color, 'timer': timer}

food = spawn_food()

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                change_to = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                change_to = 'DOWN'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                change_to = 'RIGHT'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                change_to = 'LEFT'

    direction = change_to

    if direction == 'UP':
        snake_pos[1] -= CELL_SIZE
    elif direction == 'DOWN':
        snake_pos[1] += CELL_SIZE
    elif direction == 'LEFT':
        snake_pos[0] -= CELL_SIZE
    elif direction == 'RIGHT':
        snake_pos[0] += CELL_SIZE

    if snake_pos[0] < 0 or snake_pos[0] >= WIDTH or snake_pos[1] < 0 or snake_pos[1] >= HEIGHT:
        running = False

    if snake_pos == food['pos']:
        score += food['value']
        food = spawn_food()
    else:
        snake_body.pop()

    snake_body.insert(0, list(snake_pos))

    for block in snake_body[1:]:
        if snake_pos == block:
            running = False

    food['timer'] -= 1
    if food['timer'] <= 0:
        food = spawn_food()

    for block in snake_body:
        pygame.draw.rect(screen, GREEN, pygame.Rect(block[0], block[1], CELL_SIZE, CELL_SIZE))

    pygame.draw.rect(screen, food['color'], pygame.Rect(food['pos'][0], food['pos'][1], CELL_SIZE, CELL_SIZE))

    font = pygame.font.Font(None, 30)
    score_text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))

    if score > 0 and score % 4 == 0:
        level = score // 4 + 1
        speed = 10 + (level * 2)

    pygame.display.update()
    clock.tick(speed)

pygame.quit()
sys.exit()
