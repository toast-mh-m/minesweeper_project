import pygame

### initialization ###
pygame.display.init()
pygame.font.init()


def movements(player):
   player_speed = 10
   player_speed_diag = player_speed * 0.707
   key_w, key_a, key_s, key_d = pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d
   # movement
   key = pygame.key.get_pressed()

   if key[key_a] and key[key_w] == True:
       player.move_ip(-player_speed_diag, -player_speed_diag)
   elif key[key_d] and key[key_w] == True:
      player.move_ip(player_speed_diag, -player_speed_diag)
   elif key[key_a] and key[key_s] == True:
      player.move_ip(-player_speed_diag, player_speed_diag)
   elif key[key_d] and key[key_s] == True:
      player.move_ip(player_speed_diag, player_speed_diag)
   elif key[key_a] == True:
      player.move_ip(-player_speed, 0)
   elif key[key_d] == True:
      player.move_ip(player_speed, 0)
   elif key[key_w] ==  True:
      player.move_ip(0, -player_speed)
   elif key[key_s] == True:
      player.move_ip(0, player_speed)

   if key[pygame.K_1] == True:
      print(pygame.mouse.get_pos())

class Player:
   def __init__(self, x, y, width, height):
      self.x = x
      self.y = y
      self.width = width
      self.height = height
      self.rect = pygame.Rect((x, y, width, height))

class Button:
   def __init__(self, x, y, width, height, base_text, text, font_size, font_color, screen, color, interactable):
      self.x = x
      self.y = y
      self.width = width
      self.height = height
      self.font_color = font_color
      self.base_text = base_text
      font = pygame.font.SysFont("Times New Roman", font_size)
      self.text = font.render(text, True, font_color)
      self.color = color
      self.interactable = interactable
      
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
      self.x = x
      self.y = y
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