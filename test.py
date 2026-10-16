import pygame
from defining import *


pygame.display.init()
pygame.font.init()
running = True
clock = pygame.time.Clock()


# =============== WINDOW =============== #
SCREEN_WIDTH, SCREEN_HEIGHT = 500, 500
windowone = pygame.window.Window(title="Small Test", size=(SCREEN_WIDTH, SCREEN_HEIGHT))
screen = windowone.get_surface()




# =============== ENTITIES or just all things drawn =============== #
info_text = make_text("Good morning!", (SCREEN_WIDTH // 2), 20)
button = make_rect(0, 0, 100, 50, "Click me!")
button["rect"].center = screen.get_rect().center
button["text center"].center = screen.get_rect().center
player = Player("p1", 175, 175, 50, 50)




gamestate = 0




# =============== RUNNING =============== #
while running:
   screen.fill((0, 0, 0))
   # =============== GAMESTATE =============== #
   if gamestate >= 1:
       screen.blit(info_text["text"], info_text["text rect"]) # text


       match gamestate:
           case 2:
               info_text["text"] = fontrendering("test")


   # =============== EVENT HANDLER =============== #
   for event in pygame.event.get():
       if event.type == pygame.WINDOWCLOSE:
           event.window.destroy()


       if event.type == pygame.QUIT: # allows quitting of the window
          running = False


       if event.type == pygame.MOUSEBUTTONDOWN:
           if event.button == 1: # left, 2 middle, 3 right
               if player.rect.collidepoint(event.pos): # collided with mouse. event.pos gets mouse coords
                   gamestate += 1  


   movements(player.rect)
   pygame.draw.rect(screen, (0, 175, 0), button["rect"], 0) # drawing green buttons
   screen.blit(button["text"], button["text center"]) # blitting button text
   pygame.draw.rect(screen, (255, 0, 0), player.rect) # drawing red player
   windowone.flip() # always updating
   clock.tick(60) # fps








pygame.quit()