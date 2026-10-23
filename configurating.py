import random
import minesweeper

def make_tiles(num_rows, num_columns, tile_sheet, tile_scale, SCREEN_WIDTH, SCREEN_HEIGHT, Tile, tiles, sweeper_map, sweeper_map_location, mines):
    # ======================================== TILE APPEARANCES ========================================
    tile_empty = tile_sheet.get_image(15, 16, 16, tile_scale)
    tile_one = tile_sheet.get_image(14, 16, 16, tile_scale)
    tile_two = tile_sheet.get_image(13, 16, 16, tile_scale)
    tile_three = tile_sheet.get_image(12, 16, 16, tile_scale)
    tile_four = tile_sheet.get_image(11, 16, 16, tile_scale)
    tile_five = tile_sheet.get_image(10, 16, 16, tile_scale)
    tile_six = tile_sheet.get_image(9, 16, 16, tile_scale)
    tile_seven = tile_sheet.get_image(8, 16, 16, tile_scale)
    tile_eight = tile_sheet.get_image(7, 16, 16, tile_scale)
    tile_death_mine = tile_sheet.get_image(3, 16, 16, tile_scale)

    # ======================================== CREATING ALL TILES ========================================
    for rows in range(num_rows):
        for columns in range(num_columns):
            temp_tile_img = tile_sheet.get_image(0, 16, 16, tile_scale)
            x_local = (columns * (16 * tile_scale)) + ((SCREEN_WIDTH // 2)) - (num_columns * 8 * tile_scale)
            y_local = (rows * (16 * tile_scale)) + ((SCREEN_HEIGHT // 2)) - (num_rows * 8 * tile_scale)
            temp_tile_location = (x_local, y_local)

            temp_tile = Tile(temp_tile_img, temp_tile_location, False, tile_sheet, tile_scale)
            tiles.append(temp_tile)
            sweeper_map.append(temp_tile.img)
            sweeper_map_location.append(temp_tile.location)

    # ======================================== SELECTING WHICH TILES ARE MINES ========================================
    old_positions = [-1]
    same = -1
    for i in range(mines):
        while same in old_positions:
            mine_position = random.randint(0, (len(sweeper_map) - 1))
            same = mine_position
        old_positions.append(mine_position)
        # print(mine_position)
        for tile in tiles:
            if tiles[mine_position] == tile:
                tile.revealed = tile_death_mine
                tile.mine = True

    # ======================================== NON-MINE TILES DETECTING MINES AROUND THEM  ========================================
    tile_position = 0

    for tile in tiles:
        is_on_left_edge = tile_position % num_columns == 0
        is_on_right_edge = (tile_position + 1) % num_columns == 0
        is_on_top_row = tile_position < num_columns
        is_on_bottom_row = tile_position > (num_columns * num_rows) - num_columns - 1

        tile_number = 0
        check_surroundings_for_mines = { "left" : not(is_on_left_edge) and tiles[tile_position - 1].mine,
                                         "right" : not(is_on_right_edge) and tiles[tile_position + 1].mine,
                                         "top": not(is_on_top_row) and tiles[tile_position - num_columns].mine,
                                         "bottom": not(is_on_bottom_row) and tiles[tile_position + num_columns].mine,
                                         "top left": not(is_on_top_row) and not(is_on_left_edge) and tiles[tile_position - (num_columns + 1)].mine,
                                         "top right": not(is_on_top_row) and not(is_on_right_edge) and tiles[tile_position - (num_columns - 1)].mine,
                                         "bottom left": not(is_on_bottom_row) and not(is_on_left_edge) and tiles[tile_position + (num_columns - 1)].mine,
                                         "bottom right": not(is_on_bottom_row) and not(is_on_right_edge) and tiles[tile_position + (num_columns + 1)].mine
                                        }    
        if tile.revealed == None:
            checks = sum([check_surroundings_for_mines["left"],
                          check_surroundings_for_mines["right"],
                          check_surroundings_for_mines["top"],
                          check_surroundings_for_mines["bottom"],
                          check_surroundings_for_mines["top left"],
                          check_surroundings_for_mines["top right"],
                          check_surroundings_for_mines["bottom left"],
                          check_surroundings_for_mines["bottom right"]

            ])
            tile_number = checks
                    
        if tile.mine == False:
            match tile_number:
                case 0:
                    tile.revealed = tile_empty
                    tile.empty = True
                case 1:
                    tile.revealed = tile_one
                case 2:
                    tile.revealed = tile_two
                case 3:
                    tile.revealed = tile_three
                case 4:
                    tile.revealed = tile_four
                case 5:
                    tile.revealed = tile_five
                case 6:
                    tile.revealed = tile_six
                case 7:
                    tile.revealed = tile_seven
                case 8:
                    tile.revealed = tile_eight

        tile_position += 1

# def reveal_tiles_around(tiles, tile_position, num_columns, num_rows, sweeper_map):
#     is_on_left_edge = tile_position % num_columns == 0
#     is_on_right_edge = (tile_position + 1) % num_columns == 0
#     is_on_top_row = tile_position < num_columns
#     is_on_bottom_row = tile_position > (num_columns * num_rows) - num_columns - 1

#     clear_surroundings = { "left" : not(is_on_left_edge) and not(tiles[tile_position - 1].mine),
#                             "right" : not(is_on_right_edge) and not(tiles[tile_position + 1].mine),
#                             "top": not(is_on_top_row) and not(tiles[tile_position - num_columns].mine),
#                             "bottom": not(is_on_bottom_row) and not(tiles[tile_position + num_columns].mine),
#                             "top left": not(is_on_top_row) and not(is_on_left_edge) and not(tiles[tile_position - (num_columns + 1)].mine),
#                             "top right": not(is_on_top_row) and not(is_on_right_edge) and not(tiles[tile_position - (num_columns - 1)].mine),
#                             "bottom left": not(is_on_bottom_row) and not(is_on_left_edge) and not(tiles[tile_position + (num_columns - 1)].mine),
#                             "bottom right": not(is_on_bottom_row) and not(is_on_right_edge) and not(tiles[tile_position + (num_columns + 1)].mine)
#                         }
#     around_position = 0
#     temp_position = tile_position
#     backlog_positions = []
#     for tile in tiles:
#         if tile.empty:
#             for x in clear_surroundings:
#                 around_position = check_surroundings_for_empty(x, clear_surroundings, temp_position, num_columns)
#                 sweeper_map[around_position] = tiles[around_position].revealed
#                 tiles[around_position].interactable = False
#                 tile.empty_flag = False
#                 if tiles[around_position].empty:
#                     backlog_positions.append(around_position)
#         elif backlog_positions:
#             for x in clear_surroundings:
#                 if not backlog_positions:
#                     return
#                 backlog_positions[0] = check_surroundings_for_empty(x, clear_surroundings, temp_position, num_columns)
#                 around_position = backlog_positions[0]
#                 sweeper_map[around_position] = tiles[around_position].revealed
#                 tiles[around_position].interactable = False
#                 tile.empty = False
#                 backlog_positions.pop(0)
#                 if tiles[around_position].empty:
#                     backlog_positions.append(around_position)
#         else:
#             pass

                


# def check_surroundings_for_empty(x, clear_surroundings, temp_position, num_columns):
#     around_position = 0

#     match (x, clear_surroundings[x]):
#         case ("left", True):
#             around_position = temp_position - 1
#         case ("right", True):
#             around_position = temp_position + 1
#         case ("top", True):
#             around_position = temp_position - num_columns
#         case ("bottom", True):
#             around_position = temp_position + num_columns
#         case ("top left", True):
#             around_position = temp_position - (num_columns + 1)
#         case ("top right", True):
#             around_position = temp_position - (num_columns - 1)
#         case ("bottom left", True):
#             around_position = temp_position + (num_columns - 1)
#         case ("bottom right", True):
#             around_position = temp_position + (num_columns + 1)

#     return around_position