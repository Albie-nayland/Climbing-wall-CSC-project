import pygame as py
import os, json

py.init()

num_holds = {}
hold_info = {}
Inventory = {}
dicts = {
    "num_holds": num_holds,
    "hold_info": hold_info,
    "Inventory": Inventory
}

ScriptDir = os.path.dirname(os.path.abspath(__file__))
FilePath = os.path.join(ScriptDir, "Inventory.json")

if os.path.exists(FilePath):
    try:
        with open(FilePath, 'r') as f:
            Data = json.load(f)
            for key in Data:
                for i in Data[key]:
                    dicts[key].update({i: Data[key][i]})
    except Exception as e:
        print(f"Failed to load save: {e}")

def save_data():
    with open(FilePath, 'w') as f:
        json.dump({
            "num_holds": num_holds,
            "hold_info": hold_info,
            "Inventory": Inventory
        }, f, indent=2)

def wall_1():
    global num_holds

    WIDTH, HEIGHT = 500, 600
    screen = py.display.set_mode((WIDTH, HEIGHT))
    py.display.set_caption("Pygame Window")

    holding_index = None
    y_hole_distance = 25
    x_hole_distance = 25
    offset = x_hole_distance / 2
    wall_spots = []
    for n in range(HEIGHT - 100):
        if n % y_hole_distance == 0:
            for i in range(WIDTH):
                if i % x_hole_distance == 0:
                    
                    wall_spots.append((i + offset, n + y_hole_distance / 2))

    running = True
    while running:
        screen.fill("black")
        mouse_x, mouse_y = py.mouse.get_pos()

        for event in py.event.get():
            if event.type == py.QUIT:
                save_data()  # Save on quit, not every frame
                running = False

            elif event.type == py.MOUSEBUTTONDOWN:
                for i in reversed(list(Inventory)):
                    x, y, r = Inventory[i][0], Inventory[i][1], Inventory[i][2]
                    if (mouse_x - x) ** 2 + (mouse_y - y) ** 2 <= r ** 2:
                        holding_index = i
                        break

            elif event.type == py.MOUSEBUTTONUP:
                if holding_index is not None:
                    save_data()  # Save when you drop a hold
                holding_index = None

        if holding_index is not None:
            Inventory[holding_index][0] = mouse_x
            Inventory[holding_index][1] = mouse_y

        # Draw tray
        py.draw.rect(screen, "gray", py.Rect(0, HEIGHT - 100, WIDTH, 100))

        # Draw holds using Inventory for position (Inventory just tracks what exists)
        for i in Inventory:
            x, y, r, colour, type = Inventory[i][0], Inventory[i][1], Inventory[i][2], Inventory[i][3], Inventory[i][4]
            if y >= 500 and holding_index != i:
                y = 550
                x = hold_info[i[:-2]][0]
            else:
                y = y - (y % y_hole_distance) + y_hole_distance/2
                x = x - (x % x_hole_distance) + x_hole_distance/2
                
            py.draw.circle(screen, colour, (x, y), r)
            Inventory[i][0], Inventory[i][1], Inventory[i][2], Inventory[i][3], Inventory[i][4] = x, y, r, colour, type

        # Draw wall hole spots
        for spot in wall_spots:
            py.draw.circle(screen, "red", spot, 2)

        py.display.flip()

def interactable_wall_1():
    does_offset = 1

    # Screen setup
    WIDTH, HEIGHT = 500, 600
    screen = py.display.set_mode((WIDTH, HEIGHT))
    py.display.set_caption("Pygame Window")

    holds_used = {}
    holding_index = None

    y_hole_distance = 25
    x_hole_distance = 2*y_hole_distance

    for n in range(HEIGHT - 100):
            if n % y_hole_distance == 0:
                does_offset += 1
                for i in range(WIDTH):
                    if i % x_hole_distance == 0:
                        if does_offset % 2 == 0:
                            offset = x_hole_distance - x_hole_distance/4
                        else:
                            offset = x_hole_distance/4
                        wall_spots.append((i + offset, n + y_hole_distance/2))

    # Main loop
    running = True
    while running:
        screen.fill("black")  # background colour
        mouse_x, mouse_y = py.mouse.get_pos()
        # --- Events ---
        for event in py.event.get():
            if event.type == py.QUIT:
                running = False
                full_wall()
            elif event.type == py.MOUSEBUTTONDOWN:
                mouse_down = True
                for i in holds_full_dict_1:
                    x, y, r = holds_full_dict_1[i]
                    if (mouse_x - x)**2 + (mouse_y - y)**2 <= r**2:
                        holding_index = i
                        break

            elif event.type == py.MOUSEBUTTONUP:
                mouse_down = False
                holding_index = None
        # --- Update ---
        if holding_index is not None:
            holds_full_dict_1[holding_index][0] = mouse_x
            holds_full_dict_1[holding_index][1] = mouse_y

        for i in wall_spots:
            py.draw.circle(screen, "red", i, 2)


        if mouse_y % x_hole_distance < x_hole_distance/2:
            mouse_offset = x_hole_distance - x_hole_distance/4
        else:
            mouse_offset = x_hole_distance/4

        # --- DRAWING ---#
        py.draw.rect(screen, "gray", py.Rect(0, HEIGHT - 100, WIDTH, 100))

        for i in holds_full_dict_1:
            if holds_full_dict_1[i][1] % x_hole_distance < x_hole_distance/2:
                hold_offset = x_hole_distance - x_hole_distance/4
            else:
                hold_offset = x_hole_distance/4
            if holds_full_dict_1[i][1] < 500:
                holds_full_dict_1[i][0], holds_full_dict_1[i][1] = (holds_full_dict_1[i][0] - (holds_full_dict_1[i][0] % x_hole_distance) + hold_offset, (holds_full_dict_1[i][1] - (holds_full_dict_1[i][1] % y_hole_distance) + y_hole_distance/2))
                py.draw.circle(screen, "blue", (holds_full_dict_1[i][0], holds_full_dict_1[i][1]), holds_full_dict_1[i][2])
            else:
                if holding_index is None:
                    if holds_full_dict_1[i][2] == 15:
                        holds_full_dict_1[i][0], holds_full_dict_1[i][1] = (50, 550)
                    elif holds_full_dict_1[i][2] == 25:
                        holds_full_dict_1[i][0], holds_full_dict_1[i][1] = (100, 550)
                    elif holds_full_dict_1[i][2] == 45:
                        holds_full_dict_1[i][0], holds_full_dict_1[i][1] = (175, 550)
                py.draw.circle(screen, "blue", (holds_full_dict_1[i][0], holds_full_dict_1[i][1]), holds_full_dict_1[i][2])
        # for i in holds_full_dict_1:
        #     if holds_full_dict_1[1] < 500 and i not in wall_1:
        #         holds_full_dict_1.update({len(holds_full_dict_1) : []})

        py.display.flip()  # update screen

def interactable_wall_2():
    does_offset = 1

    # Screen setup
    WIDTH, HEIGHT = 500, 600
    screen = py.display.set_mode((WIDTH, HEIGHT))
    py.display.set_caption("Pygame Window")

    holds_used = {}
    holding_index = None

    y_hole_distance = 25
    x_hole_distance = 2*y_hole_distance

    mouse_down = False

    for n in range(HEIGHT - 100):
            if n % y_hole_distance == 0:
                does_offset += 1
                for i in range(WIDTH):
                    if i % x_hole_distance == 0:
                        if does_offset % 2 == 0:
                            offset = x_hole_distance - x_hole_distance/4
                        else:
                            offset = x_hole_distance/4
                        wall_spots.append((i + offset, n + y_hole_distance/2))

    # Main loop
    running = True
    while running:
        screen.fill("black")  # background colour
        mouse_x, mouse_y = py.mouse.get_pos()
        # --- Events ---
        for event in py.event.get():
            if event.type == py.QUIT:
                running = False
                full_wall()
            elif event.type == py.MOUSEBUTTONDOWN:
                mouse_down = True
                for i in holds_full_dict_1:
                    x, y, r = holds_full_dict_1[i]
                    if (mouse_x - x)**2 + (mouse_y - y)**2 <= r**2:
                        holding_index = i
                        break

            elif event.type == py.MOUSEBUTTONUP:
                mouse_down = False
                holding_index = None
        # --- Update ---
        if holding_index is not None:
            holds_full_dict_1[holding_index][0] = mouse_x
            holds_full_dict_1[holding_index][1] = mouse_y

        for i in wall_spots:
            py.draw.circle(screen, "red", i, 2)


        if mouse_y % x_hole_distance < x_hole_distance/2:
            mouse_offset = x_hole_distance - x_hole_distance/4
        else:
            mouse_offset = x_hole_distance/4

        # --- DRAWING ---#
        py.draw.rect(screen, "gray", py.Rect(0, HEIGHT - 100, WIDTH, 100))
        for i in holds_full_dict_1:
            if holds_full_dict_1[i][1] % x_hole_distance < x_hole_distance/2:
                hold_offset = x_hole_distance - x_hole_distance/4
            else:
                hold_offset = x_hole_distance/4
            if holds_full_dict_1[i][1] < 500:
                holds_full_dict_1[i][0], holds_full_dict_1[i][1] = (holds_full_dict_1[i][0] - (holds_full_dict_1[i][0] % x_hole_distance) + hold_offset, (holds_full_dict_1[i][1] - (holds_full_dict_1[i][1] % y_hole_distance) + y_hole_distance/2))
                py.draw.circle(screen, "blue", (holds_full_dict_1[i][0], holds_full_dict_1[i][1]), holds_full_dict_1[i][2])
            else:
                if holding_index is None:
                    if holds_full_dict_1[i][2] == 15:
                        holds_full_dict_1[i][0], holds_full_dict_1[i][1] = (50, 550)
                    elif holds_full_dict_1[i][2] == 25:
                        holds_full_dict_1[i][0], holds_full_dict_1[i][1] = (100, 550)
                    elif holds_full_dict_1[i][2] == 45:
                        holds_full_dict_1[i][0], holds_full_dict_1[i][1] = (175, 550)
                py.draw.circle(screen, "blue", (holds_full_dict_1[i][0], holds_full_dict_1[i][1]), holds_full_dict_1[i][2])
        py.display.flip()  # update screen

def interactable_wall_3():
    does_offset = 1

    # Screen setup
    WIDTH, HEIGHT = 500, 600
    screen = py.display.set_mode((WIDTH, HEIGHT))
    py.display.set_caption("Pygame Window")

    holds_used = {}
    holding_index = None

    y_hole_distance = 25
    x_hole_distance = 2*y_hole_distance

    mouse_down = False

    for n in range(HEIGHT - 100):
            if n % y_hole_distance == 0:
                does_offset += 1
                for i in range(WIDTH):
                    if i % x_hole_distance == 0:
                        if does_offset % 2 == 0:
                            offset = x_hole_distance - x_hole_distance/4
                        else:
                            offset = x_hole_distance/4
                        wall_spots.append((i + offset, n + y_hole_distance/2))

    # Main loop
    running = True
    while running:
        screen.fill("black")  # background colour
        mouse_x, mouse_y = py.mouse.get_pos()
        # --- Events ---
        for event in py.event.get():
            if event.type == py.QUIT:
                running = False
                full_wall()
            elif event.type == py.MOUSEBUTTONDOWN:
                mouse_down = True
                for i in holds_full_dict_3:
                    x, y, r = holds_full_dict_3[i]
                    if (mouse_x - x)**2 + (mouse_y - y)**2 <= r**2:
                        holding_index = i
                        break

            elif event.type == py.MOUSEBUTTONUP:
                mouse_down = False
                holding_index = None
        # --- Update ---
        if holding_index is not None:
            holds_full_dict_3[holding_index][0] = mouse_x
            holds_full_dict_3[holding_index][1] = mouse_y

        for i in wall_spots:
            py.draw.circle(screen, "red", i, 2)


        if mouse_y % x_hole_distance < x_hole_distance/2:
            mouse_offset = x_hole_distance - x_hole_distance/4
        else:
            mouse_offset = x_hole_distance/4

        # --- DRAWING ---#
        py.draw.rect(screen, "gray", py.Rect(0, HEIGHT - 100, WIDTH, 100))
        for i in holds_full_dict_3:
            if holds_full_dict_3[i][1] % x_hole_distance < x_hole_distance/2:
                hold_offset = x_hole_distance - x_hole_distance/4
            else:
                hold_offset = x_hole_distance/4
            if holds_full_dict_3[i][1] < 500:
                holds_full_dict_3[i][0], holds_full_dict_3[i][1] = (holds_full_dict_3[i][0] - (holds_full_dict_3[i][0] % x_hole_distance) + hold_offset, (holds_full_dict_3[i][1] - (holds_full_dict_3[i][1] % y_hole_distance) + y_hole_distance/2))
                py.draw.circle(screen, "blue", (holds_full_dict_3[i][0], holds_full_dict_3[i][1]), holds_full_dict_3[i][2])
            else:
                if holding_index is None:
                    if holds_full_dict_3[i][2] == 15:
                        holds_full_dict_3[i][0], holds_full_dict_3[i][1] = (50, 550)
                    elif holds_full_dict_3[i][2] == 25:
                        holds_full_dict_3[i][0], holds_full_dict_3[i][1] = (100, 550)
                    elif holds_full_dict_3[i][2] == 45:
                        holds_full_dict_3[i][0], holds_full_dict_3[i][1] = (175, 550)
                py.draw.circle(screen, "blue", (holds_full_dict_3[i][0], holds_full_dict_3[i][1]), holds_full_dict_3[i][2])
        py.display.flip()  # update screen

def full_wall():
    mouse_down = False
    # Screen setup
    WIDTH, HEIGHT = 1000, 600
    screen = py.display.set_mode((WIDTH, HEIGHT))
    py.display.set_caption("Pygame Window")
    
    running = True
    while running:

        screen.fill("black")  # background colour
        mouse_x, mouse_y = py.mouse.get_pos()
        # --- Events ---
        for event in py.event.get():
            if event.type == py.QUIT:
                running = False
            elif event.type == py.MOUSEBUTTONDOWN:
                mouse_down = True
            elif event.type == py.MOUSEBUTTONUP:
                mouse_down = False
        if mouse_y > 25 and mouse_y < 575 and mouse_down:
            if mouse_x > 25 and mouse_x < 325:
                running = False
                interactable_wall_1()
            elif mouse_x > 350 and mouse_x < 650:
                running = False
                interactable_wall_2()
            elif mouse_x > 675 and mouse_x < 975:
                running = False
                interactable_wall_3()

        py.draw.rect(screen, "green", py.Rect(25, 25, 300, 550))
        py.draw.rect(screen, "blue", py.Rect(350, 25, 300, 550))
        py.draw.rect(screen, "red", py.Rect(675, 25, 300, 550))
        py.display.flip()  # update screen

wall_1()

# Quit cleanly
py.quit()
