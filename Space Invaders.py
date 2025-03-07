### Space Invaders
### Elijah Brauch und Lukas Neumann
### 06.03.2025

# Imports
import pygame
import math

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((400, 300), pygame.SCALED)
clock = pygame.time.Clock()
running = True

# Variables
player_xy = (200,200)
player_speed = 5
player_missile_list = []
player_missile_speed = 10

# Player
player = pygame.image.load("textures/player.png")

# Main Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get pressed keys
    keys = pygame.key.get_pressed()
    x = keys[pygame.K_d] - keys[pygame.K_a]
    y = keys[pygame.K_s] - keys[pygame.K_w]
    if keys[pygame.K_SPACE]:
        player_missile_list.append((player_xy[0] + 7, player_xy[1], True))
    if keys[pygame.K_ESCAPE]:
        running = False

    # Player missile update
    for i in range(len(player_missile_list)):
        i -= 1
        player_missile_list[i] = (player_missile_list[i][0], player_missile_list[i][1] - player_missile_speed, True)
        if player_missile_list[i][1] < -10:
            player_missile_list[i] = (-10, -10, False)
    # Player missile cleanup
    for i in range(len(player_missile_list)):
        i -= 1
        if not player_missile_list[i][2]:
            player_missile_list.pop(i)
            break

    # Player speed normalization
    if abs(x) + abs(y) > 1:
        x = x / math.sqrt(2)
        y = y / math.sqrt(2)

    # Update player position
    player_xy = (math.floor(x * player_speed) + player_xy[0], math.floor(y * player_speed) + player_xy[1])

    # Player bounds check
    if player_xy[0] < -2:
        player_xy = (-2, player_xy[1])
    if player_xy[0] > 385:
        player_xy = (385, player_xy[1])
    if player_xy[1] < 0:
        player_xy = (player_xy[0], 0)
    if player_xy[1] > 285:
        player_xy = (player_xy[0], 285)

    # Draw screen
    screen.fill((10, 10, 15))
    for i in range(len(player_missile_list)):
        pygame.draw.rect(screen, (255, 0, 0), (player_missile_list[i][0], player_missile_list[i][1], 2, 5))
    screen.blit(player, player_xy)
    pygame.display.flip()
    clock.tick(30)