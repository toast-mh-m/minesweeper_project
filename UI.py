import pygame

pygame.display.init()
pygame.font.init()

class Button:
   def __init__(self, x, y, width, height, base_text, text, font_size, font_color, screen, color, interactable):
      self.x, self.y, self.width, self.height, self.font_color, self.base_text, self.color, self.interactable = x, y, width, height, font_color, base_text, color, interactable
      font = pygame.font.SysFont("Times New Roman", font_size)
      self.text = font.render(text, True, font_color)
      screen_w, screen_h = screen.get_size()
      self.rect = pygame.Rect((0, 0, width, height))

      match (x, y):
         case "center", int() as y_value:
            target_center = (screen_w // 2, y_value)

         case int() as x_value, "center":
            target_center = (x_value, screen_h // 2)

         case "center", "center":
            target_center = (screen_w // 2, screen_h // 2)

         case int() as x_value, int() as y_value:
            target_center = (x_value, y_value)
            
      self.rect.center = target_center
      self.location = self.text.get_rect(center=target_center)

class Text:
   def __init__(self, text, font_size, x, y, color, screen):
      font = pygame.font.SysFont("Times New Roman", font_size)
      self.text = font.render(text, True, color)
      self.x, self.y = x, y
      tl, tr = screen.get_size()
      match (x, y):
         case "center", int() as y:
            self.location = self.text.get_rect(center=(tl // 2, y))

         case int() as x, "center":
            self.location = self.text.get_rect(center=(x, tr // 2))

         case "center", "center":
            self.location = self.text.get_rect(center=(tl // 2, tr // 2))

         case int() as x, int() as y:
            self.location = self.text.get_rect(center=(x, y))

def fontrendering(text, font_size, color):
  font = pygame.font.SysFont("Times New Roman", font_size)
  return font.render(text, True, color)