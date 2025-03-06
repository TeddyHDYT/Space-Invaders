### Space Invaders
### Elijah Brauch und Lukas Neumann
### 05.03.2025

# Imports
import pygame

# initialize pygame
pygame.init()
screen = pygame.display.set_mode((400, 300), pygame.SCALED | pygame.RESIZABLE)
clock = pygame.time.Clock()
running = True

# Player
player = pygame.image.load("textures/player.png")
player = pygame.transform.rotate(player, 45)

# Main Loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    screen.blit(player, (200, 150))
    pygame.display.flip()
    clock.tick(10)