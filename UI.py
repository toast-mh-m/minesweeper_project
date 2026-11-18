import pygame
from settings import initiate_center, screen, tile_sheet
from minesweeper import SpriteSheet

pygame.display.init()
pygame.font.init()

class Button:
   def __init__(self, x, y, width, height, text, font_size, font_color, bgcolor, interactable):
      self.width, self.height, self.font_color, self.base_text, self.bgcolor, self.interactable = width, height, font_color, text, bgcolor, interactable
      font = pygame.font.SysFont("Times New Roman", font_size)
      self.text = font.render(text, True, font_color)

      centerpos = screen.get_rect().center
      centerx, centery = centerpos
      if x == y == None:
         location = self.rect.get_rect(center=(centerx, centery))
      elif isinstance(x, int) and y == None:
         location = (x, centery)
      elif x == None and isinstance(y, int):
         location = (centerx - 45, centery + y)
      else:
         location = (x, y)

      localx, localy = location
      self.location = location
      self.rect = pygame.Rect((localx, localy, width, height))
      self.textlocation = self.text.get_rect(center=self.rect.center)

class OUTLINEBUTTON:
   def __init__(self, x, y, width, height, bgcolor):
      self.bgcolor = bgcolor

      centerpos = screen.get_rect().center
      centerx, centery = centerpos
      if x == y == None:
         location = self.rect.get_rect(center=(centerx, centery))
      elif isinstance(x, int) and y == None:
         location = (x, centery)
      elif x == None and isinstance(y, int):
         location = (centerx - 50, centery + y)
      else:
         location = (x, y)

      localx, localy = location
      self.rect = pygame.Rect((localx, localy, width, height))

class Text:
   def __init__(self, text, font_size, x, y, color):
      font = pygame.font.SysFont("Times New Roman", font_size)
      self.text = font.render(text, True, color)
      self.y = y
      if x == y == initiate_center:
         centerpos = screen.get_rect().center
         centerx, centery = centerpos
         self.textlocation = self.text.get_rect(center=(centerx, centery))
      else:
         self.textlocation = (x, y)

class Checkbox:
   def __init__(self, name, x, y, frame, scale, toggle):
      self.name, self.location, self.interactable = name, (x, y), False
      self.rect = pygame.Rect((x, y, 16 * scale, 16 * scale))
      self.image = tile_sheet.get_image(frame, 16, 16, scale)
      self.toggle = toggle

class DropDown:
   def __init__(self, name, x, y, list):
      self.name, self.location, self.interactable, self.list = name, (x, y), False, list
      self.rect = pygame.Rect((x, y, 100, 50))

class ArrowTile:
   def __init__(self, x, y, width, height):
      pass

def fontrendering(text, font_size, color):
  font = pygame.font.SysFont("Times New Roman", font_size)
  return font.render(text, True, color)