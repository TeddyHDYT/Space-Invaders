### Space Invaders
### Elijah Brauch und Lukas Neumann
### 06.03.2025

# Imports
import pygame
import math
import random

# Load images
player = pygame.image.load("textures/player.png")
enemy = pygame.image.load("textures/enemy.png")

# Functions
def boundsCheck(positionX, positionY, offsetX, offsetY, width, height, screen):
    if 0 > positionX + offsetX:
        positionX = 0 - offsetX
    elif screen.get_width() < positionX + offsetX + width:
        positionX = screen.get_width() - width - offsetX
    if 0 > positionY + offsetY:
        positionY = 0 - offsetY
    elif screen.get_height() < positionY + offsetY + height:
        positionY = screen.get_height() - offsetY- height
    positionXY = (positionX, positionY)
    return positionXY

def boxcollisionCheck(x1,y1,offsetx1,offsety1,width1,height1,x2,y2,offsetx2,offsety2,width2,height2):
    noCollision = True
    if (x2 + offsetx2 > x1 + offsetx1 + width1) or (x2 + offsetx2 + width2 < x1 + offsetx1):
        noCollision = False
    if (y2 + offsety2 + height2 < y1 + offsety1) or (y2 + offsety2 > y1 + offsety1 + height1):
        noCollision = False
    return noCollision

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((400, 300), pygame.SCALED)
pygame.display.set_caption("Space Invaders")
pygame.display.set_icon(player)
clock = pygame.time.Clock()
running = True

# Variables
player_x = screen.get_width() / 2
player_y = screen.get_height() - 100
player_speed = 5
player_missile_list = []
player_missile_speed = 15
player_missile_cooldown = 5 # in frames
cooldown = 0
enemy_list = []
enemy_speed = 1

# Bounding boxes
player_bb = ()

# Main Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get pressed keys
    keys = pygame.key.get_pressed()
    input_x = keys[pygame.K_d] - keys[pygame.K_a] or keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
    input_y = keys[pygame.K_s] - keys[pygame.K_w] or keys[pygame.K_DOWN] - keys[pygame.K_UP]
    if keys[pygame.K_SPACE] and cooldown == 0:
        player_missile_list.append((player_x + 7, player_y, True))
        cooldown = player_missile_cooldown
    if keys[pygame.K_ESCAPE]:
        running = False

    # Player missile update
    for i in range(len(player_missile_list)):
        i -= 1
        player_missile_list[i] = (player_missile_list[i][0], player_missile_list[i][1] - player_missile_speed, True)
        if player_missile_list[i][1] < -10:
            player_missile_list[i] = (-10, -10, False)
        
    # Player missile cooldown
    if cooldown > 0:
        cooldown -= 1

    
    # Player missile cleanup
    for i in range(len(player_missile_list)):
        i -= 1
        if not player_missile_list[i][2]:
            player_missile_list.pop(i)
            break

    # Player speed normalization
    if abs(input_x) + abs(input_y) > 1:
        input_x = input_x / math.sqrt(2)
        input_y = input_y / math.sqrt(2)

    # Update player position
    player_x += math.floor(input_x * player_speed)
    player_y += math.floor(input_y * player_speed)

    # Player bounds check
    player_xy = boundsCheck(player_x, player_y, 0, 0, 15, 15, screen)
    player_x = player_xy[0]
    player_y = player_xy[1]


    # Draw screen
    screen.fill((10, 10, 15))
    for i in range(len(player_missile_list)):
        pygame.draw.rect(screen, (255, 0, 0), (player_missile_list[i][0], player_missile_list[i][1], 2, 4))
    screen.blit(player, (player_x, player_y))
    for i in range(len(enemy_list)):
        screen.blit(enemy, enemy_list[i])
    pygame.display.flip()
    clock.tick(30)


    # Enemy spawn
    if random.randint(0, 100) < 2:
        enemy_list.append((random.randint(0, screen.get_width() - 15), 0))


    #Enemy update
    for i in range(len(enemy_list)):
        enemy_list[i] = (enemy_list[i][0], enemy_list[i][1] + enemy_speed)


    # Enemy collision
    for i in range(len(enemy_list)):
        i -= 1
        for j in range(len(player_missile_list)):
            if boxcollisionCheck(player_missile_list[j][0], player_missile_list[j][1], 0, 0, 2, 4, enemy_list[i][0], enemy_list[i][1], 0, 0, 15, 15):
                enemy_list.pop(i)
                player_missile_list[j] = (-10, -10, False)
                break


    # Enemy player collision
    for i in range(len(enemy_list)):
        i -= 1
        if boxcollisionCheck(player_x, player_y, 0, 0, 15, 15, enemy_list[i][0], enemy_list[i][1], 0, 0, 15, 15):
            running = False


    # Enemy cleanup 
    for i in range(len(enemy_list)):
        if enemy_list[i][1] > screen.get_height():
            enemy_list.pop(i)
            break