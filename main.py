import pygame
import os
import UI
import minesweeper
import configurating

pygame.display.init()
pygame.font.init()
pygame.mixer.init()
clock = pygame.time.Clock()
explode_sfx = pygame.mixer.Sound(os.path.join("audio", "lose.mp3"))
tick_sfx = pygame.mixer.Sound(os.path.join("audio", "tick.mp3"))
explode_sfx.set_volume(0.25)
tick_sfx.set_volume(0.1)

display_info = pygame.display.Info()

# =============== FUNCTIONS =============== #
def drawrect(color, rect):
    return pygame.draw.rect(screen, color, rect, 0)

def loadimg(folder, image):
    return pygame.image.load(os.path.join(folder, image)).convert_alpha()

def drawblit(text, location):
    return screen.blit(text, location)

# =============== VARIABLES REGARDING EVERYTHING =============== #
SCREEN_WIDTH, SCREEN_HEIGHT = display_info.current_w, display_info.current_h
gamestate = "Menu"
running = True
end_game = win = timer_active = False

fading_value = 255
fading_time = 5

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)

# =============== WINDOW =============== #
icon = pygame.image.load(os.path.join("assets", "icon.png"))
windowone = pygame.window.Window(title="Minesweeper", fullscreen_desktop=True)
windowone.set_icon(icon)
screen = windowone.get_surface()

black_fading = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
black_fading.fill(BLACK)

# =============== BUTTONS, TEXT, & IMAGES =============== #
header_text = UI.Text("Minesweeper", 60, "center", "center", WHITE, screen)

start_button = UI.Button("center", 750, 100, 50, "Start", "Start", 20, WHITE, screen, BLACK, False)
outline_start_button = UI.Button("center", 750, 110, 60, "", "", 0, WHITE, screen, WHITE, False)

settings_button = UI.Button("center", 825, 100, 50, "Settings", "Settings", 20, WHITE, screen, BLACK, False)
outline_settings_button = UI.Button("center", 825, 110, 60, "", "", 0, WHITE, screen, WHITE, False)

back_button = UI.Button(35, 20, 75, 50, "\N{LEFTWARDS ARROW} Back", "\N{LEFTWARDS ARROW} Back", 20, WHITE, screen, BLACK, False)

quit_button = UI.Button("center", 900, 100, 50, "Quit", "Quit", 20, WHITE, screen, BLACK, False)
outline_quit_button = UI.Button("center", 900, 110, 60, "", "", 0, WHITE, screen, WHITE, False)

buttons = [start_button, settings_button, back_button, quit_button]

tile_sheet_image = loadimg("assets", "tile_sheet.png")
number_sheet_image = loadimg("assets", "number_sheet.png")
face_sheet_image = loadimg("assets", "face_sheet.png")

tile_sheet = minesweeper.SpriteSheet(tile_sheet_image)
number_sheet = minesweeper.SpriteSheet(number_sheet_image)
face_sheet = minesweeper.SpriteSheet(face_sheet_image)

face = minesweeper.Face(face_sheet, SCREEN_WIDTH, SCREEN_HEIGHT, False)

timer_num_img, timer_num_local = minesweeper.minesweeper_timer(number_sheet, SCREEN_WIDTH, SCREEN_HEIGHT)
mine_num_img, mine_num_local = minesweeper.remaining_mines(number_sheet, SCREEN_WIDTH, SCREEN_HEIGHT)

credits = UI.Button((SCREEN_WIDTH - 50), (SCREEN_HEIGHT - 60), 100, 50, "made by /jm\\", "made by /jm\\", 15, WHITE, screen, BLACK, False)


# =============== RUNNING =============== #
while running:
    screen.fill(GRAY)
    mouse_pos = pygame.mouse.get_pos()
    clickable_mouse = False

    # =============== GAMESTATE =============== #
    match gamestate:
        case "Menu": # =============== MENU SCREEN =============== #
            for button in [outline_start_button, start_button, outline_settings_button, settings_button, credits, outline_quit_button, quit_button]:
                drawrect(button.color, button.rect)

            for text in [header_text, start_button, settings_button, credits, quit_button]:
                drawblit(text.text, text.location)

            if fading_value >= 0:
                fading_value -= fading_time
            elif fading_value <= 0:
                start_button.interactable = settings_button.interactable = quit_button.interactable = True
        case "Start": # =============== GAMEPLAY SCREEN =============== #
            # ===== UPDATE TIMERS ====
            minesweeper.minesweeper_time, timer_active, timer_num_img = minesweeper.timer_display(minesweeper.minesweeper_time, timer_active, timer_num_img, number_sheet, minesweeper.tile_scale, tick_sfx)
            minesweeper.mines, mine_num_img = minesweeper.mines_display(minesweeper.mines, mine_num_img, number_sheet, minesweeper.tile_scale)

            # ===== SHOW ALL TILES =====
            for i in range(len(minesweeper.sweeper_map)):
                drawblit(minesweeper.sweeper_map[i], minesweeper.sweeper_map_location[i])

            for i in range(len(timer_num_img)):
                drawblit(timer_num_img[i], timer_num_local[i])
                drawblit(mine_num_img[i], mine_num_local[i])


            drawrect(BLACK, face.rect)
            drawrect(back_button.color, back_button.rect)
            drawblit(back_button.text, back_button.location)
            drawblit(face.img, (face.x, face.y))
            back_button.interactable = True



        case "Settings": # =============== SETTINGS SCREEN =============== #
            back_button.interactable = True
            drawrect(back_button.color, back_button.rect)
            drawblit(back_button.text, back_button.location)

        case "Quitting":
            if fading_value < 255:
                fading_value += fading_time
            elif fading_value == 255:
                running = False

    # ============================== EVENT HANDLER ============================== #
    for ev in pygame.event.get():
        MOUSEDOWN = (ev.type == pygame.MOUSEBUTTONDOWN)


        if ev.type == pygame.QUIT: # allows quitting of the window
          running = False

        # =============== RESTARTING! =============== #
        if MOUSEDOWN and ev.button == 1:
            if face.rect.collidepoint(mouse_pos) and face.interactable:
                minesweeper.mines = minesweeper.total_mines
                minesweeper.tiles = []
                minesweeper.sweeper_map = []
                minesweeper.sweeper_map_location = []
                minesweeper.minesweeper_time = 0
                configurating.make_tiles(minesweeper.num_rows, minesweeper.num_columns, tile_sheet, minesweeper.tile_scale, SCREEN_WIDTH, SCREEN_HEIGHT, minesweeper.Tile, minesweeper.tiles, minesweeper.sweeper_map, minesweeper.sweeper_map_location, minesweeper.mines)
                end_game = False
                win = False

                for tile in minesweeper.tiles:
                    tile.interactable = True

        # =============== BUTTON UI VISUALS =============== #
        for button in buttons:
            if button.rect.collidepoint(mouse_pos) and fading_value < 0  and button.interactable:
                button.text = UI.fontrendering(button.base_text, 20, ("#b3b3ff"))
                clickable_mouse = True
            else:
                button.text = UI.fontrendering(button.base_text, 20, WHITE)

        # =============== TILE LOGIC =============== #
        if not end_game or win:
            for i, tile in enumerate(minesweeper.tiles):
                if MOUSEDOWN and ev.button == 1 and tile.rect.collidepoint(mouse_pos) and tile.interactable and not tile.flagged: # clicking on a non-flagged tile
                        tile.interactable = False
                        if tile.mine:
                            tile.revealed_img = tile_sheet.get_image(3, 16, 16, minesweeper.tile_scale)
                            minesweeper.sweeper_map[i] = tile.revealed_img
                            tile.revealed = True
                            end_game = True
                            explode_sfx.play()
                        else:
                            minesweeper.sweeper_map[i] = tile.revealed_img
                            tile.revealed = True
                            timer_active = True
                        if tile.empty:
                            configurating.reveal_tiles_around(minesweeper.tiles, i, minesweeper.num_columns, minesweeper.num_rows, minesweeper.sweeper_map)

                elif MOUSEDOWN and ev.button == 3 and tile.rect.collidepoint(mouse_pos) and tile.interactable: # right clicking on a tile
                    
                    if tile.flagged:
                        minesweeper.sweeper_map[i] = tile_sheet.get_image(0, 16, 16, minesweeper.tile_scale)
                        tile.flagged = False
                        minesweeper.mines += 1
                    else:
                        minesweeper.sweeper_map[i] = tile_sheet.get_image(1, 16, 16, minesweeper.tile_scale)
                        tile.flagged = True
                        minesweeper.mines -= 1
                
                elif tile.rect.collidepoint(mouse_pos) and tile.interactable: # hovering over any non-revealed tile
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

        # =============== FACE LOGIC =============== #
        if MOUSEDOWN and ev.button == 1 and face.rect.collidepoint(mouse_pos) and face.interactable: # pressing down face
            face.img = minesweeper.change_face(face, "clicked", face_sheet)

        elif win:
            face.img = minesweeper.change_face(face, "win", face_sheet)

            for tile in minesweeper.tiles:
                tile.interactable = False
        
        elif end_game:
            face.img = minesweeper.change_face(face, "lost", face_sheet)
        elif not end_game:
            face.img = minesweeper.change_face(face, "smile", face_sheet)

        if face.rect.collidepoint(mouse_pos) and face.interactable: # hovering over face
            clickable_mouse = True

        # =============== MOUSE LOGIC =============== #
        if clickable_mouse:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            # =============== UI BUTTON LOGIC =============== #
        if MOUSEDOWN:
            if ev.button == 1:
                if start_button.rect.collidepoint(mouse_pos) and start_button.interactable and gamestate == "Menu": # pressing start from menu
                    gamestate = "Start"
                    start_button.interactable = False
                    settings_button.interactable = False
                    face.interactable = True
                    configurating.make_tiles(minesweeper.num_rows, minesweeper.num_columns, tile_sheet, minesweeper.tile_scale, SCREEN_WIDTH, SCREEN_HEIGHT, minesweeper.Tile, minesweeper.tiles, minesweeper.sweeper_map, minesweeper.sweeper_map_location, minesweeper.mines)
                    for tile in minesweeper.tiles:
                        tile.interactable = True

                elif settings_button.rect.collidepoint(mouse_pos) and settings_button.interactable and gamestate == "Menu": # pressing settings from menu
                    gamestate = "Settings"
                    start_button.interactable = False
                    settings_button.interactable = False

                if back_button.rect.collidepoint(mouse_pos) and back_button.interactable and gamestate == "Start": # going back to menu from start
                    gamestate = "Menu"
                    start_button.interactable = True
                    settings_button.interactable = True
                    face.interactable = False
                    
                    minesweeper.mines = minesweeper.total_mines
                    minesweeper.tiles = []
                    minesweeper.sweeper_map = []
                    minesweeper.sweeper_map_location = []
                    minesweeper.minesweeper_time = 0
                    end_game = False
                    win = False
                    timer_active = False

                    for tile in minesweeper.tiles:
                        tile.interactable = False

                elif back_button.rect.collidepoint(mouse_pos) and back_button.interactable and gamestate == "Settings": # going back to menu from settings
                    gamestate = "Menu"
                    start_button.interactable = True
                    settings_button.interactable = True

                if quit_button.rect.collidepoint(mouse_pos) and quit_button.interactable and gamestate == "Menu": # quitting
                    start_button.interactable = settings_button.interactable = quit_button.interactable = False
                    gamestate = "Quitting"



    drawblit(black_fading, (0, 0))
    black_fading.set_alpha(fading_value)
    windowone.flip()
    clock.tick(60)

print("goodbye!")
pygame.quit()