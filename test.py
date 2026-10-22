import pygame
# import os
from UI import *
from minesweeper import *

pygame.display.init()
pygame.font.init()
running = True
clock = pygame.time.Clock()
username = "test"


# =============== WINDOW =============== #
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 1000
windowone = pygame.window.Window(title="Minesweeper", size=(SCREEN_WIDTH, SCREEN_HEIGHT))
screen = windowone.get_surface()

# =============== WINDOW =============== #
black_fading = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
black_fading.fill(BLACK)
fading_value = 255
fading_time = 3


# =============== ENTITIES or just all things drawn =============== #
header_text = Text("Minesweeper", 60, "center", "center", WHITE, screen)

start_button = Button("center", 750, 100, 50, "Start", "Start", 20, WHITE, screen, BLACK, False)
outline_start_button = Button("center", 750, 110, 60, "", "", 0, WHITE, screen, WHITE, False)

settings_button = Button("center", 825, 100, 50, "Settings", "Settings", 20, WHITE, screen, BLACK, False)
outline_settings_button = Button("center", 825, 110, 60, "", "", 0, WHITE, screen, WHITE, False)

buttons = [outline_start_button, start_button, outline_settings_button, settings_button]
# =============== OTHER VARIABLES / VALUES =============== #
gamestate = 0
interactable = False

# =============== RUNNING =============== #
while running:
    screen.fill((0, 0, 0))
    mouse_pos = pygame.mouse.get_pos()
    clickable_mouse = False

    
    
    # =============== GAMESTATE =============== #
    match gamestate:
        case 0:
            pygame.draw.rect(screen, outline_start_button.color, outline_start_button.rect, 0) # OUTLINE start button
            pygame.draw.rect(screen, start_button.color, start_button.rect, 0) # start button base

            pygame.draw.rect(screen, outline_settings_button.color, outline_settings_button, 0) # OUTLINE settings button
            pygame.draw.rect(screen, settings_button.color, settings_button.rect, 0) # settings button base
            screen.blit(header_text.text, header_text.location) # SHOW header txt
            screen.blit(start_button.text, start_button.location) # SHOW blitting start text
            screen.blit(settings_button.text, settings_button.location) # SHOW blitting settings text

            if fading_value > 0:
                fading_value -= fading_time
            if fading_value == 0:
                interactable = True

        case "Start":
            print("start!")
            
        case "Settings":
            print("SETTINGS") # placeholder
            

        

    # =============== EVENT HANDLER =============== #
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # allows quitting of the window
          running = False


        for button in buttons:
            if button.rect.collidepoint(mouse_pos) and fading_value == 0:
                button.text = fontrendering(button.base_text, 20, ("#b3b3ff"))
                clickable_mouse = True
            else:
                button.text = fontrendering(button.base_text, 20, WHITE)
        

        if clickable_mouse:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)



        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # left, 2 middle, 3 right
                if start_button.rect.collidepoint(event.pos) and interactable == True: # collided with mouse. event.pos gets mouse coords
                    gamestate = "Start"
                    minesweeper_start()

    #    movements(player.rect)
    screen.blit(black_fading, (0, 0))
    black_fading.set_alpha(fading_value)
    #    pygame.draw.rect(screen, (255, 0, 0), player.rect) # drawing red player

    windowone.flip() # always updating
    clock.tick(60) # fps




pygame.quit()