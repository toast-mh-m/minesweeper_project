import pygame
# import os
import UI
import minesweeper
import configurating
import random

pygame.display.init()
pygame.font.init()
running = True
clock = pygame.time.Clock()

# =============== WINDOW =============== #
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 1000
windowone = pygame.window.Window(title="Minesweeper", size=(SCREEN_WIDTH, SCREEN_HEIGHT))
screen = windowone.get_surface()

# =============== FADING =============== #
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
black_fading = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
black_fading.fill(BLACK)
fading_value = 255
fading_time = 3


# =============== ENTITIES or just all things drawn =============== #
header_text = UI.Text("Minesweeper", 60, "center", "center", WHITE, screen)

start_button = UI.Button("center", 750, 100, 50, "Start", "Start", 20, WHITE, screen, BLACK, False)
outline_start_button = UI.Button("center", 750, 110, 60, "", "", 0, WHITE, screen, WHITE, False)

settings_button = UI.Button("center", 825, 100, 50, "Settings", "Settings", 20, WHITE, screen, BLACK, False)
outline_settings_button = UI.Button("center", 825, 110, 60, "", "", 0, WHITE, screen, WHITE, False)

TEST_CENTER = UI.Button("center", "center", 10, 10, "", "", 0, BLACK, screen, (255, 0, 0), False)

buttons = [start_button, settings_button]
tile_sheet_image = pygame.image.load("assets/tile_sheet.png").convert_alpha()
tile_sheet = minesweeper.SpriteSheet(tile_sheet_image)

# =============== OTHER VARIABLES / VALUES =============== #
gamestate = 0

# =============== SWEEPER VARIABLES =============== #
ALIVE =  True
sweeper_map = []
sweeper_map_location = []
tiles = []
tile_scale = 2
mines = 10


# =============== RUNNING =============== #
while running:
    screen.fill((0, 0, 0))
    mouse_pos = pygame.mouse.get_pos()
    clickable_mouse = False
    # screen.blit(tile_sheet, (0, 0))

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

            if fading_value >= 0:
                fading_value -= fading_time
            if fading_value == 0:
                start_button.interactable = True
        case "Start":
            for i in range(len(sweeper_map)):
                screen.blit(sweeper_map[i], sweeper_map_location[i])
        case "Settings":
            print("SETTINGS") # placeholder
            

        

    # =============== EVENT HANDLER =============== #
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # allows quitting of the window
          running = False


        for button in buttons:
            if button.rect.collidepoint(mouse_pos) and fading_value < 0  and button.interactable == True:
                button.text = UI.fontrendering(button.base_text, 20, ("#b3b3ff"))
                clickable_mouse = True
            else:
                button.text = UI.fontrendering(button.base_text, 20, WHITE)


        for i, tile in enumerate(tiles):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and tile.rect.collidepoint(mouse_pos) and tile.interactable == True and tile.flagged == False: # clicking on a non-flagged tile
                    tile.interactable = False
                    sweeper_map[i] = tile.revealed
                    # DEPTH-FIRST SEARCH
                    # if tile.empty:
                        # configurating.reveal_tiles_around(tiles, i, minesweeper.num_columns, minesweeper.num_rows, sweeper_map)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and tile.rect.collidepoint(mouse_pos) and tile.interactable == True: # left clicking on a tile
                
                if tile.flagged == True:
                    sweeper_map[i] = tile_sheet.get_image(0, 16, 16, tile_scale)
                    tile.flagged = False
                else:
                    sweeper_map[i] = tile_sheet.get_image(1, 16, 16, tile_scale)
                    tile.flagged = True
            
            elif tile.rect.collidepoint(mouse_pos) and tile.interactable == True: # hovering over any non-revealed tile
                clickable_mouse = True


        if clickable_mouse:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)



        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # left, 2 middle, 3 right
                if start_button.rect.collidepoint(event.pos) and start_button.interactable == True: # collided with mouse. event.pos gets mouse coords
                    gamestate = "Start"
                    start_button.interactable = False
                    settings_button.interactable = False
                    configurating.make_tiles(minesweeper.num_rows, minesweeper.num_columns, tile_sheet, tile_scale, SCREEN_WIDTH, SCREEN_HEIGHT, minesweeper.Tile, tiles, sweeper_map, sweeper_map_location, mines)
                    for tile in tiles:
                        tile.interactable = True


    #    movements(player.rect)
    screen.blit(black_fading, (0, 0))
    black_fading.set_alpha(fading_value)
    #    pygame.draw.rect(screen, (255, 0, 0), player.rect) # drawing red player
    # ============================ DEBUG ============================
    pygame.draw.rect(screen, TEST_CENTER.color, TEST_CENTER.rect, 0)
    windowone.flip() # always updating
    clock.tick(60) # fps




pygame.quit()