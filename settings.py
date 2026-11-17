import pygame
import os
from minesweeper import SpriteSheet

pygame.display.init()
display_info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 900
FULL_W, FULL_H = display_info.current_w, display_info.current_h

# =============== VARIABLES REGARDING EVERYTHING =============== #
# SCREEN_WIDTH, SCREEN_HEIGHT = FULL_W, FULL_H
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
# windowone = pygame.window.Window(title="Minesweeper", fullscreen_desktop=True)
windowone = pygame.window.Window(title="Minesweeper", fullscreen_desktop=False, size=(SCREEN_WIDTH, SCREEN_HEIGHT))
windowone.set_icon(icon)
screen = windowone.get_surface()
initiate_center = None

black_fading = pygame.Surface((FULL_W, FULL_H))
black_fading.fill(BLACK)

# =============== FUNCTIONS =============== #
def drawrect(color, rect):
    return pygame.draw.rect(screen, color, rect, 0)

def loadimg(folder, image):
    return pygame.image.load(os.path.join(folder, image)).convert_alpha()

def drawblit(text, location):
    return screen.blit(text, location)

# =============== BUTTONS, TEXT, & IMAGES =============== #
tile_sheet_image = loadimg("assets", "tile_sheet.png")
number_sheet_image = loadimg("assets", "number_sheet.png")
face_sheet_image = loadimg("assets", "face_sheet.png")

tile_sheet = SpriteSheet(tile_sheet_image)
number_sheet = SpriteSheet(number_sheet_image)
face_sheet = SpriteSheet(face_sheet_image)