import random

def number_images(number_sheet, tile_scale):
   number_0 = number_sheet.get_image(11, 13, 23, tile_scale)
   number_1 = number_sheet.get_image(10, 13, 23, tile_scale)
   number_2 = number_sheet.get_image(9, 13, 23, tile_scale)
   number_3 = number_sheet.get_image(8, 13, 23, tile_scale)
   number_4 = number_sheet.get_image(7, 13, 23, tile_scale)
   number_5 = number_sheet.get_image(6, 13, 23, tile_scale)
   number_6 = number_sheet.get_image(5, 13, 23, tile_scale)
   number_7 = number_sheet.get_image(4, 13, 23, tile_scale)
   number_8 = number_sheet.get_image(3, 13, 23, tile_scale)
   number_9 = number_sheet.get_image(2, 13, 23, tile_scale)
   number_blank = number_sheet.get_image(1, 13, 23, tile_scale)
   number_neg = number_sheet.get_image(0, 13, 23, tile_scale)

   return number_0, number_1, number_2, number_3, number_4, number_5, number_6, number_7, number_8, number_9, number_blank, number_neg

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
    tile_normal_mine = tile_sheet.get_image(5, 16, 16, tile_scale)

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
    for _ in range(mines):
        while same in old_positions:
            mine_position = random.randint(0, (len(sweeper_map) - 1))
            same = mine_position
        old_positions.append(mine_position)
        for tile in tiles:
            if tiles[mine_position] == tile:
                tile.revealed = tile_normal_mine
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

def reveal_tiles_around(tiles, tile_position, num_columns, num_rows, sweeper_map):
    # If the selected tile is empty, the algorithm first examines the tile to the right, then continues moving right until it reaches a terminal tile of that direction. 
    # (terminal tile here means reaching a mine or a number).
    # From there, it traverses downwards, then left, and finally upward. 
    # When a teminal tile is reached, then algorithm reveals it, and then backtracks to the previous tile to continue the process
    # DEPTHS FIRST SEARCH

    # stack is (current pos, direction index)
    stack = [(tile_position, 0)] # right 0, down 1, left 2, up 3
    visited = {tile_position}

    # reveal the first tile
    sweeper_map[tile_position] = tiles[tile_position].revealed

    while stack:
        curr_pos, direction = stack[-1]

        is_on_left_edge = curr_pos % num_columns == 0
        is_on_right_edge = (curr_pos + 1) % num_columns == 0
        is_on_top_row = curr_pos < num_columns
        is_on_bottom_row = curr_pos > (num_columns * num_rows) - num_columns - 1

        is_on_top_left = is_on_top_row or is_on_left_edge
        is_on_top_right = is_on_top_row or is_on_right_edge
        is_on_bottom_left = is_on_bottom_row or is_on_left_edge
        is_on_bottom_right = is_on_bottom_row or is_on_right_edge

        next_pos = None

        # check directions sequentially
        match direction:
            case 0 if not is_on_top_right: # top right
                next_pos = curr_pos - num_columns + 1
            case 1 if not is_on_top_left: # top left
                next_pos = curr_pos - num_columns - 1
            case 2 if not is_on_bottom_right: # bottom right
                next_pos = curr_pos + num_columns + 1
            case 3 if not is_on_bottom_left: # bottom left
                next_pos = curr_pos + num_columns - 1
            case 4 if not is_on_right_edge: # right
                next_pos = curr_pos + 1
            case 5 if not is_on_bottom_row: # bottom
                next_pos = curr_pos + num_columns
            case 6 if not is_on_left_edge: # left
                next_pos = curr_pos - 1
            case 7 if not is_on_top_row: # up
                next_pos = curr_pos - num_columns

        # if next_pos exists and was not previously visited
        if next_pos is not None and next_pos not in visited: 
            visited.add(next_pos)

            sweeper_map[next_pos] = tiles[next_pos].revealed
            tiles[next_pos].interactable = False

            # if this tile is empty, append it for next stack
            if tiles[next_pos].empty:
                stack.append((next_pos, 0))
                continue
        
        # if direction is less than 3 (not up just yet)
        if direction < 7:
            stack[-1] = (curr_pos, direction + 1)
        else:
            stack.pop()