import pygame
import math
import configurating

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

def minesweeper_timer(number_sheet, tile_scale, SCR_W, SCR_H, num_columns, num_rows):
   timer_num_img = []
   timer_num_local = []

   for i in range(3):
      digit = number_sheet.get_image(1, 13, 23, tile_scale)
      x_local = (i * (13 * tile_scale)) + ((SCR_W // 2)) + (num_columns * 3.7 * tile_scale)
      y_local = ((23 * tile_scale)) + ((SCR_H // 2)) - (num_rows * 13.1 * tile_scale)
      digit_location = (x_local, y_local)

      timer_num_img.append(digit)
      timer_num_local.append(digit_location)

   return timer_num_img, timer_num_local

def timer(minesweeper_time, timer_active, timer_num_img, number_sheet, tile_scale):
   number_0, number_1, number_2, number_3, number_4, number_5, number_6, number_7, number_8, number_9, number_blank, x = configurating.number_images(number_sheet, tile_scale)
   
   if timer_active:
      minesweeper_time += 1/60

   time_string = str(math.trunc(minesweeper_time))
   match len(time_string):
         case 1:
            visible_num = "_" + "_" + time_string
         case 2:
            visible_num = "_" + time_string
         case 3:
            visible_num = time_string
         case _:
            visible_num = "999"

   img_position = 0
   for digit in visible_num:
        match digit:
         case "_":
            timer_num_img[img_position] = number_blank
         case "0":
            timer_num_img[img_position] = number_0
         case "1":
            timer_num_img[img_position] = number_1
         case "2":
            timer_num_img[img_position] = number_2
         case "3":
            timer_num_img[img_position] = number_3
         case "4":
            timer_num_img[img_position] = number_4
         case "5":
            timer_num_img[img_position] = number_5
         case "6":
            timer_num_img[img_position] = number_6
         case "7":
            timer_num_img[img_position] = number_7
         case "8":
            timer_num_img[img_position] = number_8
         case "9":
            timer_num_img[img_position] = number_9

        img_position += 1
   
   return minesweeper_time, timer_active, timer_num_img

def remaining_mines(number_sheet, tile_scale, SCR_W, SCR_H, num_columns, num_rows):
   mine_num_img = []
   mine_num_local = []

   for i in range(3):
      digit = number_sheet.get_image(1, 13, 23, tile_scale)
      x_local = (i * (13 * tile_scale)) + ((SCR_W // 2)) - (num_columns * 8 * tile_scale)
      y_local = ((23 * tile_scale)) + ((SCR_H // 2)) - (num_rows * 13.1 * tile_scale)
      digit_location = (x_local, y_local)

      mine_num_img.append(digit)
      mine_num_local.append(digit_location)

   return mine_num_img, mine_num_local

def mines_display(mines, mine_num_img, number_sheet, tile_scale):
    number_0, number_1, number_2, number_3, number_4, number_5, number_6, number_7, number_8, number_9, number_blank, number_neg, = configurating.number_images(number_sheet, tile_scale)

    mines_string = str(mines)
    if mines >= 0: # positive mines
        match len(mines_string):
            case 1:
                display = "_" + "_" + mines_string
            case 2:
                display = "_" + mines_string
            case 3:
                display = mines_string
            case _:
                display = "999"
    elif -100 < mines < 0: # negative mines
        match len(mines_string):
            case 2:
                display = "_" + mines_string
            case 3:
                display = mines_string
            case 4:
                display = mines_string[1:]
            case 5:
                display = "999"

    img_position = 0
    for digit in display:
        match digit:
           case "_":
                mine_num_img[img_position] = number_blank
           case "0":
                mine_num_img[img_position] = number_0
           case "1":
                mine_num_img[img_position] = number_1
           case "2":
                mine_num_img[img_position] = number_2
           case "3":
                mine_num_img[img_position] = number_3
           case "4":
                mine_num_img[img_position] = number_4
           case "5":
                mine_num_img[img_position] = number_5
           case "6":
                mine_num_img[img_position] = number_6
           case "7":
                mine_num_img[img_position] = number_7
           case "8":
                mine_num_img[img_position] = number_8
           case "9":
                mine_num_img[img_position] = number_9
           case "-":
                mine_num_img[img_position] = number_neg

        img_position += 1

    return mines, mine_num_img

def face_sheet_config(face_sheet, tile_scale, SCR_W, SCR_H, num_columns, num_rows):
   size = tile_scale - 0.25
   face_sheet_img = face_sheet.get_image(4, 24, 24, size)
   x_local = (25 * tile_scale) + (SCR_W // 2) - (num_columns * 3.9 * tile_scale)
   y_local = (25 * tile_scale) + (SCR_H // 2) - (num_rows * 13.43 * tile_scale)
   face_sheet_local = (x_local, y_local)

   return face_sheet_img, face_sheet_local, size