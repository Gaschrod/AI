def draw_board():
    # clear screen and hide cursor
    print(term.home + term.clear + term.hide_cursor)

    map_y = (map_size[1] * 2) - 1

    row = -1
    col = 0
    x_repeat = 0

    while x_repeat < map_size[0]:
        x_repeat += 1

        while row <= map_y:
            row += 1
            if row == 0 and col == 0:
                print(term.move_xy(col, row) + term.on_black +"╔" + term.normal, end='', flush=True)
            elif row == map_y + 1 and col == 0:
                print(term.move_xy(col, row) + term.on_black +"╚" + term.normal, end='', flush=True)
            elif row == 0:
                print(term.move_xy(col, row) + term.on_black +"╦" + term.normal, end='', flush=True)
            elif row == map_y + 1:
                print(term.move_xy(col, row) + term.on_black +"╩" + term.normal, end='', flush=True)
            elif row % 2 == 0 and col % 4 == 0 and col != 0:
                print(term.move_xy(col, row) + term.on_black +"╬" + term.normal, end='', flush=True)
            elif row % 2 != 0:
                print(term.move_xy(col, row) + term.on_black +"║" + term.normal, end='', flush=True)
            else:
                print(term.move_xy(col, row) + term.on_black +"╠" + term.normal, end='', flush=True)

        if True: # ═ \n
            row = 0
            col += 1
            print(term.move_xy(col, row) + term.on_black +"═" + term.normal, end='', flush=True)

            while row <= map_y:
                row += 1
                if row % 2 != 0:
                    print(term.move_xy(col, row) + term.on_black +" " + term.normal, end='', flush=True)
                else:
                    print(term.move_xy(col, row) + term.on_black +"═" + term.normal, end='', flush=True)

        if True: # ═ o
            row = 0
            col += 1
            print(term.move_xy(col, row) + term.on_black +"═" + term.normal, end='', flush=True)

            while row <= map_y:
                row += 1
                if row % 2 != 0:
                    print(term.move_xy(col, row) + term.on_black +"o" + term.normal, end='', flush=True)
                else:
                    print(term.move_xy(col, row) + term.on_black +"═" + term.normal, end='', flush=True)

        if True: # ═ \n
            row = 0
            col += 1
            print(term.move_xy(col, row) + term.on_black +"═" + term.normal, end='', flush=True)

            while row <= map_y:
                row += 1
                if row % 2 != 0:
                    print(term.move_xy(col, row) + term.on_black +" " + term.normal, end='', flush=True)
                else:
                    print(term.move_xy(col, row) + term.on_black +"═" + term.normal, end='', flush=True)
            
        col +=1
        row = -1

    while row <= map_y:
        row += 1
        if row == 0:
            print(term.move_xy(col, row) + term.on_black +"╗" + term.normal, end='', flush=True)
        elif row % 2 != 0:
            print(term.move_xy(col, row) + term.on_black +"║" + term.normal, end='', flush=True)
        elif x_repeat == map_size[0]:
            print(term.move_xy(col, row) + term.on_black +"╣" + term.normal, end='', flush=True)

    print(term.move_xy(col, row) + term.on_black +"╝" + term.normal, end='', flush=True)

    for keys in werewolf_dico.keys():
        wolf_data = werewolf_dico.get(keys)
        keys = keys[1:-1]
        current_wolf = keys.split(", ")
        new_key = [int(current_wolf[0]) , int(current_wolf[1])]

        key_x = (int(new_key[0])*3 + int(new_key[0])-1) - 1
        key_y = (int(new_key[1])*2) -1

        if wolf_data[0] == 1:
            print(term.move_xy(key_x, key_y) + term.on_yellow +"●" + term.normal, end='', flush=True)
        else:
            print(term.move_xy(key_x, key_y) + term.on_red +"●" + term.normal, end='', flush=True)

    print("\n")

    for keys in food_dico.keys():
        food_data = food_dico.get(keys)
        keys = keys[1:-1]
        current_food = keys.split(", ")
        new_key = [int(current_food[0]) , int(current_food[1])]

        key_x = (int(new_key[0])*3 + int(new_key[0])-1) - 1
        key_y = (int(new_key[1])*2) -1

        print(term.move_xy(key_x, key_y) + term.on_green +"Ø" + term.normal, end='', flush=True)

draw_board()
