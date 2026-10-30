import pygame
# import os
import UI
import minesweeper
import configurating

pygame.display.init()
pygame.font.init()
pygame.mixer.init()

# =============== MISC VARIABLES =============== #
running = True
end_game = False
win = False
clock = pygame.time.Clock()
minesweeper_time = 0

# =============== OTHER VARIABLES / VALUES =============== #
gamestate = 0

# =============== SWEEPER VARIABLES =============== #
ALIVE =  True
sweeper_map = []
sweeper_map_location = []

# =============== AUDIO VARIABLES =============== #
explode_sfx = pygame.mixer.Sound("audio/lose.mp3")
explode_sfx.set_volume(0.25)
tick_sfx = pygame.mixer.Sound("audio/tick.mp3")
tick_sfx.set_volume(0.1)

# =============== WINDOW =============== #
display_info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = display_info.current_w, display_info.current_h
icon = pygame.image.load("assets/icon.png")
windowone = pygame.window.Window(title="Minesweeper", fullscreen_desktop=True)
windowone.set_icon(icon)
screen = windowone.get_surface()

# =============== FADING =============== #
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
black_fading = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
black_fading.fill(BLACK)
fading_value = 255
fading_time = 5

# =============== BUTTONS, TEXT, & EVERYTHING ELSE =============== #
header_text = UI.Text("Minesweeper", 60, "center", "center", WHITE, screen)

start_button = UI.Button("center", 750, 100, 50, "Start", "Start", 20, WHITE, screen, BLACK, False)
outline_start_button = UI.Button("center", 750, 110, 60, "", "", 0, WHITE, screen, WHITE, False)

settings_button = UI.Button("center", 825, 100, 50, "Settings", "Settings", 20, WHITE, screen, BLACK, False)
outline_settings_button = UI.Button("center", 825, 110, 60, "", "", 0, WHITE, screen, WHITE, False)

TEST_CENTER = UI.Button("center", "center", 10, 10, "", "", 0, BLACK, screen, (255, 0, 0), False)

buttons = [start_button, settings_button]

# =============== MINESWEEPER UI =============== #
tile_sheet_image = pygame.image.load("assets/tile_sheet.png").convert_alpha()
tile_sheet = minesweeper.SpriteSheet(tile_sheet_image)

number_sheet_image = pygame.image.load("assets/number_sheet.png").convert_alpha()
number_sheet = minesweeper.SpriteSheet(number_sheet_image)


face_sheet_image = pygame.image.load("assets/face_sheet.png").convert_alpha()
face_sheet = minesweeper.SpriteSheet(face_sheet_image)
face = minesweeper.Face(face_sheet, minesweeper.tile_scale, SCREEN_WIDTH, SCREEN_HEIGHT, False)

# =============== TIMER VARIABLES =============== #
timer_active = False
timer_num_img, timer_num_local = minesweeper.minesweeper_timer(number_sheet, minesweeper.tile_scale, SCREEN_WIDTH, SCREEN_HEIGHT, minesweeper.num_columns, minesweeper.num_rows)
mine_num_img, mine_num_local = minesweeper.remaining_mines(number_sheet, minesweeper.tile_scale, SCREEN_WIDTH, SCREEN_HEIGHT, minesweeper.num_columns, minesweeper.num_rows)
# =============== RUNNING =============== #
while running:
    screen.fill((50, 50, 50))
    mouse_pos = pygame.mouse.get_pos()
    clickable_mouse = False

    # =============== GAMESTATE =============== #
    match gamestate:
        case 0: # =============== BEGINNING SCREEN =============== #
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
        case "Start": # =============== GAMEPLAY =============== #
            # ===== SHOW ALL TILES =====
            for i in range(len(sweeper_map)):
                screen.blit(sweeper_map[i], sweeper_map_location[i])

            # ===== TIMER & MINES DISPLAY ====
            minesweeper_time, timer_active, timer_num_img = minesweeper.timer(minesweeper_time, timer_active, timer_num_img, number_sheet, minesweeper.tile_scale, tick_sfx)
            minesweeper.mines, mine_num_img = minesweeper.mines_display(minesweeper.mines, mine_num_img, number_sheet, minesweeper.tile_scale)

            for i in range(len(timer_num_img)):
                screen.blit(timer_num_img[i], timer_num_local[i])
                screen.blit(mine_num_img[i], mine_num_local[i])

            pygame.draw.rect(screen, BLACK, face.rect, 0)
            screen.blit(face.img, (face.x, face.y))


        case "Settings": # =============== SETTINGS SCREEN =============== #
            print("SETTINGS") # placeholder
            

        

    # =============== EVENT HANDLER =============== #
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # allows quitting of the window
          running = False

        # =============== RESTARTING! =============== #
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if face.rect.collidepoint(mouse_pos) and face.interactable:
                    minesweeper.mines = minesweeper.total_mines
                    minesweeper.tiles = []
                    sweeper_map = []
                    sweeper_map_location = []
                    minesweeper_time = 0
                    configurating.make_tiles(minesweeper.num_rows, minesweeper.num_columns, tile_sheet, minesweeper.tile_scale, SCREEN_WIDTH, SCREEN_HEIGHT, minesweeper.Tile, minesweeper.tiles, sweeper_map, sweeper_map_location, minesweeper.mines)
                    end_game = False
                    win = False
                    for tile in minesweeper.tiles:
                        tile.interactable = True

        # =============== BUTTON UI VISUALS =============== #
        for button in buttons:
            if button.rect.collidepoint(mouse_pos) and fading_value < 0  and button.interactable == True:
                button.text = UI.fontrendering(button.base_text, 20, ("#b3b3ff"))
                clickable_mouse = True
            else:
                button.text = UI.fontrendering(button.base_text, 20, WHITE)

        # =============== TILE LOGIC =============== #
        if not end_game or win:
            for i, tile in enumerate(minesweeper.tiles):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and tile.rect.collidepoint(mouse_pos) and tile.interactable == True and tile.flagged == False: # clicking on a non-flagged tile
                        tile.interactable = False
                        if tile.mine:
                            tile.revealed_img = tile_sheet.get_image(3, 16, 16, minesweeper.tile_scale)
                            sweeper_map[i] = tile.revealed_img
                            tile.revealed = True
                            end_game = True
                            explode_sfx.play()
                        else:
                            sweeper_map[i] = tile.revealed_img
                            tile.revealed = True
                            timer_active = True
                        if tile.empty:
                            configurating.reveal_tiles_around(minesweeper.tiles, i, minesweeper.num_columns, minesweeper.num_rows, sweeper_map)

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and tile.rect.collidepoint(mouse_pos) and tile.interactable == True: # right clicking on a tile
                    
                    if tile.flagged:
                        sweeper_map[i] = tile_sheet.get_image(0, 16, 16, minesweeper.tile_scale)
                        tile.flagged = False
                        minesweeper.mines += 1
                    else:
                        sweeper_map[i] = tile_sheet.get_image(1, 16, 16, minesweeper.tile_scale)
                        tile.flagged = True
                        minesweeper.mines -= 1
                
                elif tile.rect.collidepoint(mouse_pos) and tile.interactable == True: # hovering over any non-revealed tile
                    clickable_mouse = True

                if tile.revealed and tile.flagged: # if it's revealed and also flagged, unflag it
                    tile.flagged = False
                    minesweeper.mines += 1
        elif end_game:
            timer_active = False

        # =============== CHECK IF WON =============== #
        tally_revealed = 0
        for tile in minesweeper.tiles:
            if not end_game:
                if tile.revealed and not tile.mine:
                    tally_revealed += 1

                if tally_revealed == ((minesweeper.num_columns * minesweeper.num_rows) - minesweeper.total_mines):
                    win = True
                    timer_active = False

        # =============== UI BUTTON LOGIC =============== #
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # left, 2 middle, 3 right
                if start_button.rect.collidepoint(event.pos) and start_button.interactable == True: # collided with mouse. event.pos gets mouse coords
                    gamestate = "Start"
                    start_button.interactable = False
                    settings_button.interactable = False
                    face.interactable = True
                    configurating.make_tiles(minesweeper.num_rows, minesweeper.num_columns, tile_sheet, minesweeper.tile_scale, SCREEN_WIDTH, SCREEN_HEIGHT, minesweeper.Tile, minesweeper.tiles, sweeper_map, sweeper_map_location, minesweeper.mines)
                    for tile in minesweeper.tiles:
                        tile.interactable = True

        # =============== FACE LOGIC =============== #
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and face.rect.collidepoint(mouse_pos) and face.interactable == True: # pressing down face
            face.img = minesweeper.change_face(face, "clicked", face_sheet)
        
        elif win:
            face.img = minesweeper.change_face(face, "win", face_sheet)

            for tile in minesweeper.tiles:
                tile.interactable = False
        
        elif end_game:
            face.img = minesweeper.change_face(face, "lost", face_sheet)
        
        elif not end_game:
            face.img = minesweeper.change_face(face, "smile", face_sheet)

        
        if face.rect.collidepoint(mouse_pos) and face.interactable == True: # hovering over face
            clickable_mouse = True

        # =============== MOUSE LOGIC =============== #
        if clickable_mouse:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


    #    movements(player.rect)
    screen.blit(black_fading, (0, 0))
    black_fading.set_alpha(fading_value)
    #    pygame.draw.rect(screen, (255, 0, 0), player.rect) # drawing red player
    # ============================ DEBUG ============================
    # pygame.draw.rect(screen, TEST_CENTER.color, TEST_CENTER.rect, 0)
    windowone.flip() # always updating
    clock.tick(60) # fps




pygame.quit()
