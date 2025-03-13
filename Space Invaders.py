### Space Invaders
### Elijah Brauch und Lukas Neumann
### 06.03.2025

# readme.md for more information and instructions

# Imports
import pygame # Handling Rendering
import math # For doing Math
import random # For random numbers


# Load textures
player = pygame.image.load("textures/player.png")
enemy = pygame.image.load("textures/enemy.png")



#### Functions

# Bounds check
def boundsCheck(positionX, positionY, boundingBox, screen): # BoundingBox = (width, height), x,y = position from top left
    width = boundingBox[0]
    height = boundingBox[1]
    if 0 > positionX:
        positionX = 0
    elif screen.get_width() < positionX + width:
        positionX = screen.get_width() - width
    if 0 > positionY:
        positionY = 0 
    elif screen.get_height() < positionY + height:
        positionY = screen.get_height() - height
    positionXY = (positionX, positionY)
    return positionXY


# Collision check for two Boxes
def boxcollisionCheck(x1,y1,boundingBox1,x2,y2,boundingBox2): # BoundingBox = (width, height), x,y = position from top left
    width1 = boundingBox1[0]
    height1 = boundingBox1[1]
    width2 = boundingBox2[0]
    height2 = boundingBox2[1]
    noCollision = True
    if (x2 > x1  + width1) or (x2 + width2 < x1):
        noCollision = False
    if (y2 + height2 < y1) or (y2 > y1 + height1):
        noCollision = False
    return noCollision



### Initialize pygame
pygame.init()
font = pygame.font.SysFont("Agencyr", 32)
screen = pygame.display.set_mode((400, 300), pygame.SCALED)
pygame.display.set_caption("Space Invaders")
pygame.display.set_icon(player)
clock = pygame.time.Clock()
running = True



# Constants
player_speed = 3
player_missile_speed = 15
player_missile_cooldown = 6 # in frames



### Variables

# Player
player_x = screen.get_width() / 2
player_y = screen.get_height() - 100

# Missiles
player_missile_list = []
cooldown = 0
fireL = False

#Enemies
enemy_list = []
enemy_speed = 1

# Bounding boxes
player_bb = (14,16)
enemy_bb = (16,16)



### Main Loop

while running:

    # Event handling Quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



### Get pressed keys

    keys = pygame.key.get_pressed()

    # Movement
    input_x = keys[pygame.K_d] - keys[pygame.K_a] or keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
    input_y = keys[pygame.K_s] - keys[pygame.K_w] or keys[pygame.K_DOWN] - keys[pygame.K_UP]

    # Fire
    if keys[pygame.K_SPACE] and cooldown == 0:
        if fireL:
            player_missile_list.append((player_x + 1, player_y, True))
        else:
            player_missile_list.append((player_x + 14, player_y, True))
        fireL = not fireL
        cooldown = player_missile_cooldown
    
    # Quit
    if keys[pygame.K_ESCAPE]:
        running = False



###Missile Logic

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



### Player Logic

    # Player speed normalization
    if abs(input_x) + abs(input_y) > 1:
        input_x = input_x / math.sqrt(2)
        input_y = input_y / math.sqrt(2)



    # Update player position
    player_x += math.floor(input_x * player_speed)
    player_y += math.floor(input_y * player_speed)



    # Player bounds check
    player_xy = boundsCheck(player_x, player_y, player_bb, screen)
    player_x = player_xy[0]
    player_y = player_xy[1]



### Enemy Logic

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
            if boxcollisionCheck(player_missile_list[j][0], player_missile_list[j][1], (1,3), enemy_list[i][0], enemy_list[i][1], enemy_bb):
                enemy_list.pop(i)
                player_missile_list[j] = (-10, -10, False)
                break



    # Enemy player collision
    for i in range(len(enemy_list)):
        i -= 1
        if boxcollisionCheck(player_x, player_y, player_bb, enemy_list[i][0], enemy_list[i][1], enemy_bb):
            running = False



    # Enemy cleanup 
    for i in range(len(enemy_list)):
        if enemy_list[i][1] > screen.get_height():
            enemy_list.pop(i)
            break



### Rendering

    # Clear screen
    screen.fill((10, 10, 15))

    # Draw missiles
    for i in range(len(player_missile_list)):
        pygame.draw.rect(screen, (255, 0, 0), (player_missile_list[i][0], player_missile_list[i][1], 1, 3))

    # Draw player
    screen.blit(player, (player_x, player_y))

    # Draw enemies
    for i in range(len(enemy_list)):
        screen.blit(enemy, enemy_list[i])
    
    # Draw Texts
    screen.blit(font.render("FPS: " + str(int(clock.get_fps())), False, (255, 255, 255)), (0, 0)) # FPS

    # Update screen
    pygame.display.flip()
    clock.tick(30)