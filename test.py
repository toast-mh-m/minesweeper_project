import pygame
import os
from defining import *

pygame.display.init()
pygame.font.init()
running = True
clock = pygame.time.Clock()
username = "test"


# =============== WINDOW =============== #
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 1000
windowone = pygame.window.Window(title="Minesweeper", size=(SCREEN_WIDTH, SCREEN_HEIGHT))
screen = windowone.get_surface()


# =============== ENTITIES or just all things drawn =============== #
header_text = Text("Minesweeper", 60, "center", "center", WHITE, screen)
start_button = Button("center", 750, 100, 50, "Start", 20, WHITE, screen, BLACK)
outline_start_button = Button("center", 750, 110, 60, "", 0, WHITE, screen, WHITE)
black_fading = pygame.Rect((0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

gamestate = 0


# =============== RUNNING =============== #
while running:
    screen.fill((0, 0, 0))
    # =============== GAMESTATE =============== #
    match gamestate:
       case 0:
            screen.blit(header_text.text, header_text.location)
        

    # =============== EVENT HANDLER =============== #
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # allows quitting of the window
          running = False



        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # left, 2 middle, 3 right
                if start_button.rect.collidepoint(event.pos): # collided with mouse. event.pos gets mouse coords
                    gamestate += 1 


    #    movements(player.rect)
    pygame.draw.rect(screen, outline_start_button.color, outline_start_button.rect, 0) # outline
    pygame.draw.rect(screen, start_button.color, start_button.rect, 0) # drawing start button
    screen.blit(start_button.text, start_button.location) # blitting button text
    #    pygame.draw.rect(screen, (255, 0, 0), player.rect) # drawing red player
    windowone.flip() # always updating
    clock.tick(60) # fps




pygame.quit()