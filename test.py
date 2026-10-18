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
windowone = pygame.window.Window(title="Small Test", size=(SCREEN_WIDTH, SCREEN_HEIGHT))
screen = windowone.get_surface()


# =============== ENTITIES or just all things drawn =============== #
textone = Text("testg", "center", "center", WHITE, screen)
buttonone = Button("center", "center", 100, 50, "clickington", screen)
# player = Player(175, 175, 50, 50)


gamestate = 0


# =============== RUNNING =============== #
while running:
   screen.fill((0, 0, 0))
   # =============== GAMESTATE =============== #
   if gamestate >= 1:
       screen.blit(textone.text, textone.location) # text

       match gamestate:
           case 2:
               textone.text = fontrendering("test")

   # =============== EVENT HANDLER =============== #
   for event in pygame.event.get():
       if event.type == pygame.QUIT: # allows quitting of the window
          running = False



       if event.type == pygame.MOUSEBUTTONDOWN:
           if event.button == 1: # left, 2 middle, 3 right
               if buttonone.rect.collidepoint(event.pos): # collided with mouse. event.pos gets mouse coords
                   gamestate += 1 


#    movements(player.rect)
   pygame.draw.rect(screen, (0, 175, 0), buttonone.rect, 0) # drawing green buttons
   screen.blit(buttonone.text, buttonone.location) # blitting button text
#    pygame.draw.rect(screen, (255, 0, 0), player.rect) # drawing red player
   windowone.flip() # always updating
   clock.tick(60) # fps




pygame.quit()