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

# Return position in bounds
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


# Collision check for two Boxes, returns True if no collision
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

font = pygame.font.SysFont("Agencyr", 32) # get font from system
screen = pygame.display.set_mode((400, 300), pygame.SCALED) # create display
pygame.display.set_caption("Space Invaders") # set name
pygame.display.set_icon(player) # set icon
clock = pygame.time.Clock()

### Variables

# Game
running = True
score = 0
leveltick = 0
nextLevel_cooldown = 30 # in seconds (at 30 frames per second)
between_levels = False

# Player
player_x = screen.get_width() / 2
player_y = screen.get_height() - 100
player_speed = 3
player_missile_speed = 15
player_missile_cooldown = 3 # in frames
player_dash_speed = 10
player_dash_time = 3 # in frames
player_dash_cooldown = 10 # in frames

# Missiles
player_missile_list = []
missile_cooldown = 0
fireL = False

# Dash
dash_cooldown = 0
dashing = False
dash_time = 0
dash_x = 0
dash_y = 0

#Enemies
enemy_list = []
enemy_speed = 1
enemy_spawnchance = 0.1
enemy_maxInit = 3
enemy_max = enemy_maxInit
enemy_maxIncrease = 2

# Bounding boxes
player_bb = (14,16)
enemy_bb = (16,16)



### Main Loop

while running:

### Ticks

    # Level tick
    leveltick += 1

    # Player missile cooldown
    if missile_cooldown > 0:
        missile_cooldown -= 1
    
    # Player dash cooldown
    if dash_cooldown > 0:
        dash_cooldown -= 1
    
    # Player dash time
    if dash_time > 0:
        dash_time -= 1



### Event handling Quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



### Get pressed keys

    keys = pygame.key.get_pressed()

    # Movement
    input_x = keys[pygame.K_d] - keys[pygame.K_a] or keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
    input_y = keys[pygame.K_s] - keys[pygame.K_w] or keys[pygame.K_DOWN] - keys[pygame.K_UP]

    # Fire
    if keys[pygame.K_SPACE] and missile_cooldown == 0:
        if fireL:
            player_missile_list.append((player_x + 1, player_y, True))
        else:
            player_missile_list.append((player_x + 14, player_y, True))
        fireL = not fireL
        missile_cooldown = player_missile_cooldown
    
    # Dash
    if keys[pygame.K_LSHIFT] and dash_cooldown == 0 and (input_x != 0 or input_y != 0):
        dashing = True
        dash_x = input_x
        dash_y = input_y
        dash_time = player_dash_time
        dash_cooldown = player_dash_cooldown
    if dashing and dash_time == 0:
        dashing = False


    
    # Quit
    if keys[pygame.K_ESCAPE]:
        quit()



###Missile Logic

    # Player missile update
    for i in range(len(player_missile_list)):
        i -= 1
        player_missile_list[i] = (player_missile_list[i][0], player_missile_list[i][1] - player_missile_speed, True)
        if player_missile_list[i][1] < -10:
            player_missile_list[i] = (-10, -10, False)



    # Player missile cleanup
    try: 
        player_missile_list.remove((-10, -10, False))
    except:
        pass



### Player Logic

    # Player speed normalization
    if abs(input_x) + abs(input_y) > 1:
        input_x = input_x / math.sqrt(2)
        input_y = input_y / math.sqrt(2)



    # Update player position
    if dashing:
        player_x += math.floor(dash_x * player_dash_speed)
        player_y += math.floor(dash_y * player_dash_speed)
    else:
        player_x += math.floor(input_x * player_speed)
        player_y += math.floor(input_y * player_speed)



    # Player bounds check
    player_xy = boundsCheck(player_x, player_y, player_bb, screen)
    player_x = player_xy[0]
    player_y = player_xy[1]



### Enemy Logic

    # Enemy spawn
    if random.randint(0, 100) < enemy_spawnchance * 100 and len(enemy_list) < enemy_max and leveltick < nextLevel_cooldown*30:
        randomEnemy = random.randint(0, screen.get_width() - 16), -20, True

        validspawn = True
        for i in range(len(enemy_list)):
            if boxcollisionCheck(randomEnemy[0], randomEnemy[1], enemy_bb, enemy_list[i][0], enemy_list[i][1], enemy_bb):
                validspawn = False
                break
        if validspawn:
            enemy_list.append(randomEnemy)



    #Enemy update
    for i in range(len(enemy_list)):
        enemy_list[i] = (enemy_list[i][0], enemy_list[i][1] + enemy_speed, True)
    
    # Increase max enemies
    if leveltick % 300 == 0:
        enemy_max += enemy_maxIncrease

    # Next level
    if leveltick >= nextLevel_cooldown * 30 and len(enemy_list) == 0:
        between_levels = True
        enemy_max = enemy_maxInit
        enemy_speed += 1
        leveltick = 0
    else:
        between_levels = False


    # Enemy missile collision
    for i in range(len(enemy_list)):
        i -= 1
        for j in range(len(player_missile_list)):
            j -= 1
            if boxcollisionCheck(player_missile_list[j][0], player_missile_list[j][1], (1,3), enemy_list[i][0], enemy_list[i][1], enemy_bb):
                enemy_list[i] = (-100, -100, False)
                player_missile_list[j] = (-10, -10, False)
                score += 50
                break
        if enemy_list[i][1] > screen.get_height():
            enemy_list[i] = (-100, -100, False)
            break



    # Enemy player collision
    if not between_levels:
        for i in range(len(enemy_list)):
            i -= 1
            if boxcollisionCheck(player_x, player_y, player_bb, enemy_list[i][0], enemy_list[i][1], enemy_bb):
                running = False


    # Enemy cleanup
    try:
        enemy_list.remove((-100, -100, False))
    except:
        pass

    # Check if any enemy hits the lower border
    if not between_levels:
        for enemy_pos in enemy_list:
            if enemy_pos[1] + enemy_bb[1] >= screen.get_height():
                running = False
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
        screen.blit(enemy, (enemy_list[i][0], enemy_list[i][1]))
    
    # Draw Texts
    scoreText = font.render(str(score), False, (255, 255, 255))
    screen.blit(scoreText, ((screen.get_width() - scoreText.get_width()) / 2, 10)) # Score

    # Update screen
    pygame.display.flip()
    clock.tick(30)


    # Restart button
    if not running:
        screen.fill((0, 0, 0))
        gameOverText = font.render("Game Over", False, (255, 0, 0))
        finalScoreText = font.render(f"Score: {score}", False, (255, 255, 255))
        restartText = font.render("Press R to Restart", False, (255, 255, 255))
        screen.blit(gameOverText, ((screen.get_width() - gameOverText.get_width()) / 2, screen.get_height() / 2 - 40))
        screen.blit(finalScoreText, ((screen.get_width() - finalScoreText.get_width()) / 2, screen.get_height() / 2))
        screen.blit(restartText, ((screen.get_width() - restartText.get_width()) / 2, screen.get_height() / 2 + 40))
        pygame.display.flip()
        
        # Wait for restart
        waiting_for_restart = True
        while waiting_for_restart:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting_for_restart = False
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    waiting_for_restart = False
                    running = True
                    score = 0
                    leveltick = 0
                    player_x = screen.get_width() / 2
                    player_y = screen.get_height() - 100
                    player_missile_list = []
                    missile_cooldown = 0
                    dash_cooldown = 0
                    dashing = False
                    dash_time = 0
                    dash_x = 0
                    dash_y = 0
                    enemy_list = []
                    enemy_speed = 1
                    enemy_max = enemy_maxInit

