import pygame
import random

pygame.init()

WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)

car_img = pygame.image.load("car.png")
car_width, car_height = 50, 100
car_img = pygame.transform.scale(car_img, (car_width, car_height))

car_x = WIDTH // 2 - car_width // 2
car_y = HEIGHT - 150
car_speed = 5

enemy_width, enemy_height = 50, 100
enemy_x = random.randint(0, WIDTH - enemy_width)
enemy_y = -100
enemy_speed = 5

coin_radius = 10
coins = []
coin_spawn_time = 30
frames = 0
collected_coins = 0

font = pygame.font.Font(None, 36)

running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and car_x > 0:
        car_x -= car_speed
    if keys[pygame.K_RIGHT] and car_x < WIDTH - car_width:
        car_x += car_speed

    frames += 1
    if frames % coin_spawn_time == 0:
        coin_x = random.randint(50, WIDTH - 50)
        coin_y = -20

        coin_type = random.choice(["regular", "silver", "gold"])
        if coin_type == "regular":
            value = 1
            color = YELLOW
            radius = 10
        elif coin_type == "silver":
            value = 2
            color = SILVER
            radius = 12
        else:
            value = 3
            color = GOLD
            radius = 14

        coins.append([coin_x, coin_y, value, color, radius])

    for coin in coins:
        coin[1] += 5

    for coin in coins[:]:
        coin_rect = pygame.Rect(coin[0] - coin[4], coin[1] - coin[4], coin[4] * 2, coin[4] * 2)
        car_rect = pygame.Rect(car_x, car_y, car_width, car_height)
        if car_rect.colliderect(coin_rect):
            collected_coins += coin[2]
            coins.remove(coin)

    coins = [coin for coin in coins if coin[1] < HEIGHT]

    enemy_y += enemy_speed
    if enemy_y > HEIGHT:
        enemy_x = random.randint(0, WIDTH - enemy_width)
        enemy_y = -100

    enemy_speed = 5 + collected_coins // 5

    enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
    if car_rect.colliderect(enemy_rect):
        print("Game Over!")
        running = False

    screen.blit(car_img, (car_x, car_y))
    pygame.draw.rect(screen, RED, (enemy_x, enemy_y, enemy_width, enemy_height))

    for coin in coins:
        pygame.draw.circle(screen, coin[3], (coin[0], coin[1]), coin[4])

    score_text = font.render(f"Coins: {collected_coins}", True, BLACK)
    screen.blit(score_text, (WIDTH - 150, 10))

    pygame.display.update()
    clock.tick(30)

pygame.quit()
