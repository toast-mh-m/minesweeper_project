import pygame


pygame.display.init() # initialization
pygame.font.init()
font = pygame.font.SysFont("Times New Roman", 20)
WHITE = (255, 255, 255)


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

def make_rect(x, y, width, height, text):
   temp_rect = pygame.Rect((x, y, width, height))
   if not text == "":
       temp_text = font.render(text, True, WHITE)
       temp_text_rect = temp_text.get_rect(center=(temp_rect.center))
   else:
      temp_text = None
      temp_text_rect = None
   return {
           "rect" : temp_rect,
           "text" : temp_text,
           "text center" : temp_text_rect
   }

class Player:
   def __init__(self, x, y, width, height):
      self.x = x
      self.y = y
      self.width = width
      self.height = height
      self.rect = pygame.Rect((x, y, width, height))

class Button:
   def __init__(self, x, y, width, height, text, screen):
      self.x = x
      self.y = y
      self.width = width
      self.height = height
      self.text = font.render(text, True, WHITE)
      if isinstance(x, int) and isinstance(y, int):
         self.rect = pygame.Rect((x, y, width, height))
      elif (x and y == "center"):
         self.rect = pygame.Rect((0, 0, width, height))
         self.rect.center = screen.get_rect().center
      self.centertext = self.text.get_rect(center=(self.rect.center))



def make_text(text, x, y):
   temp_text = font.render(text, True, WHITE)
   temp_text_rect = temp_text.get_rect(center=(x, y))
   return {
           "text" : temp_text,
           "text rect" : temp_text_rect
   }

def fontrendering(text):
  return font.render(text, True, WHITE)