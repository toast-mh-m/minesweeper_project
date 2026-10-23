import pygame

### initialization ###
pygame.display.init()
pygame.font.init()

num_rows = 9
num_columns = 9

class SpriteSheet:
    def __init__(self, image):
        self.image = image

    def get_image(self, frame, width, height, scale):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.image, (0, 0), (frame * width, 0, width, height))
        image = pygame.transform.scale(image, (scale * width, scale * height))

        return image

class Tile:
    def __init__(self, img, location, interactable, sheet, tile_scale):
        self.img = img
        self.location = location
        self.interactable = interactable
        self.rect = img.get_rect(topleft=location)
        self.revealed = None
        self.mine = False
        self.flagged = False
        self.empty = False
        self.empty_flag = False