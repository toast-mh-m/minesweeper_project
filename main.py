import pygame, os
import UI, minesweeper, configurating
from settings import *

pygame.display.init()
pygame.font.init()
pygame.mixer.init()
clock = pygame.time.Clock()
explode_sfx = pygame.mixer.Sound(os.path.join("audio", "lose.mp3"))
tick_sfx = pygame.mixer.Sound(os.path.join("audio", "tick.mp3"))
explode_sfx.set_volume(0.25)
tick_sfx.set_volume(0.1)


# == Menu
def Menu():
    global header_text, start_button, outline_start_button, settings_button, outline_settings_button, back_button, quit_button, outline_quit_button, buttons, credits
    header_text = UI.Text(text="Test", font_size=60, x=initiate_center, y=initiate_center, color=WHITE)
    difference = 0
    if SCREEN_WIDTH == FULL_W:
        difference = 75
    else:
        difference = 30
    
    credits = UI.Text("made by /jm\\", 15, 10, SCREEN_HEIGHT - difference, WHITE)
    outline_start_button = UI.OUTLINEBUTTON(None, 75, 110, 60, WHITE)
    outline_settings_button = UI.OUTLINEBUTTON(None, 150, 110, 60, WHITE)
    outline_quit_button = UI.OUTLINEBUTTON(None, 225, 110, 60, WHITE)

    start_button = UI.Button(x=None, y=80, width=100, height=50, text="Start", font_size=20, font_color=WHITE, bgcolor=BLACK, interactable=False)
    settings_button = UI.Button(None, 155, 100, 50, "Settings", 20, WHITE, BLACK, False)
    quit_button = UI.Button(None, 230, 100, 50, "Quit", 20, WHITE, BLACK, False)
    back_button = UI.Button(35, 20, 75, 50, "\N{LEFTWARDS ARROW} Back", 20, WHITE, BLACK, False)

    buttons = [start_button, settings_button, back_button, quit_button]

# == Settings
fullscreen_checkbox = aspectratio_checkbox = None

def Settings(which_checkbox, boolean, frame):
    global checkboxes, settings_header, fullscreen_text, fullscreen_checkbox, aspectratio_text, aspectratio_checkbox
    settings_header = UI.Text(text="~ Video & Audio ~", font_size=23, x=90, y=160, color=WHITE)
    fullscreen_text = UI.Text("Fullscreen?", 20, 75, 200, WHITE)
    aspectratio_text = UI.Text("Aspect Ratio:", 20, 75, 275, WHITE)
    # ar_leftbutton = UI.Button(x=200, y=190, width=16, height=16, text="")

    scale = (minesweeper.tile_scale - 0.5)
    match which_checkbox:
        case "Fullscreen":
            fullscreen_checkbox = UI.Checkbox(name="Fullscreen", x=200, y=190, frame=frame, scale=scale, toggle=boolean)
        case "AspectRatio":
            aspectratio_checkbox = UI.DropDown(name="AspectRatio", x=250, y=265, list=frame)
        case _:
            pass

    checkboxes = [fullscreen_checkbox, aspectratio_checkbox]


preference_data = None
try: # if have opened prior
    if os.path.isfile("preferences.txt"):
        pass

    with open("preferences.txt", "r") as f:
        preference_data = f.readlines()

    # == fullscreen
    frame = 17 if eval(preference_data[1][12:]) else 16
    Settings("Fullscreen", eval(preference_data[1][12:]), frame)
    # == aspect ratio
    list = [""]
    Settings("AspectRatio", None, list)

    
except FileNotFoundError:
    with open("preferences.txt", "w") as f:
        f.write("***** - PLAYER PREFERENCES - *****")
        f.write("\nFullscreen: False")
        f.write("\nAspectRatio: 800x600")

    with open("preferences.txt", "r") as f:
        preference_data = f.readlines()

    # == fullscreen
    frame = 17 if eval(preference_data[1][12:]) else 16
    Settings("Fullscreen", False, frame)
    # == aspect ratio
    list = [""]
    Settings("AspectRatio", None, list)







# with open("user\\config.txt") as f:
#     contents = f.read()

#     if username in contents: # FINDING STRINGS WITHIN FILE
#         print(f"found {username}")
#     else:
#         print(f"did not find ")


# configtxt = open("user\\test.txt", "x") # ADDING NEW TXT FILES
# os.remove("user\\test.txt") # REMOVING TXT FILES




face = minesweeper.Face(face_sheet, SCREEN_WIDTH, SCREEN_HEIGHT, False)

timer_num_img, timer_num_local = minesweeper.minesweeper_timer(number_sheet, SCREEN_WIDTH, SCREEN_HEIGHT)
mine_num_img, mine_num_local = minesweeper.remaining_mines(number_sheet, SCREEN_WIDTH, SCREEN_HEIGHT)

# =============== RUNNING =============== #
while running:
    screen.fill(GRAY)
    mouse_pos = pygame.mouse.get_pos()
    clickable_mouse = False

    # =============== SETTINGS LOGIC =============== #
    for checkbox in checkboxes:
        match checkbox.name:
            case "Fullscreen":
                end_result = frame = None
                if checkbox.toggle:
                    SCREEN_WIDTH, SCREEN_HEIGHT = FULL_W, FULL_H
                    windowone.set_fullscreen(True)
                    end_result = True
                    frame = 17
                elif not checkbox.toggle:
                    SCREEN_WIDTH = SCREEN_HEIGHT = 900
                    windowone.set_windowed()
                    end_result = False
                    frame = 16

                windowone.size = (SCREEN_WIDTH, SCREEN_HEIGHT)

                with open("preferences.txt", "a") as f:
                    if end_result:
                        preference_data[1] = "Fullscreen: True\n"
                    else:
                        preference_data[1] = "Fullscreen: False\n"

                with open("preferences.txt", "w") as f:
                    f.writelines(preference_data)

                Settings("Fullscreen", end_result, frame)
            case "AspectRatio":
                end_result = frame = None
                pass


    Menu()

    # =============== GAMESTATE =============== #
    match gamestate:
        case "Menu": # =============== MENU SCREEN =============== #
            for button in [outline_start_button, outline_settings_button, outline_quit_button, start_button, settings_button, quit_button]:
                drawrect(button.bgcolor, button.rect)

            for text in [header_text, credits, start_button, settings_button, quit_button]:
                drawblit(text.text, text.textlocation)

            for checkbox in checkboxes:
                checkbox.interactable = False

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
            drawrect(back_button.bgcolor, back_button.rect)
            drawblit(back_button.text, back_button.location)
            drawblit(face.img, (face.x, face.y))
            back_button.interactable = True



        case "Settings": # =============== SETTINGS SCREEN =============== #
            back_button.interactable = True

            for checkbox in checkboxes:
                checkbox.interactable = True
            drawrect(back_button.bgcolor, back_button.rect)
            drawblit(back_button.text, back_button.location)

            for thing in [fullscreen_text, settings_header, aspectratio_text]:
                drawblit(thing.text, thing.textlocation)
                
            drawblit(fullscreen_checkbox.image, fullscreen_checkbox.location)

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

        for checkbox in checkboxes:
            if gamestate == "Settings" and checkbox.interactable:
                if MOUSEDOWN:
                    if ev.button == 1 and checkbox.rect.collidepoint(mouse_pos):
                        if not checkbox.toggle:
                            checkbox.image = tile_sheet.get_image(17, 16, 16, (minesweeper.tile_scale - 0.5))
                            checkbox.toggle = True
                        elif checkbox.toggle:
                            checkbox.image = tile_sheet.get_image(16, 16, 16, (minesweeper.tile_scale - 0.5))
                            checkbox.toggle = False

                elif checkbox.rect.collidepoint(mouse_pos):
                    clickable_mouse = True

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