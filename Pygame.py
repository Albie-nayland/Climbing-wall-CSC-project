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
    py.display.set_caption("wall 1")

    hold_change = True

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
                save_data()
                full_wall()
                running = False
                

            elif event.type == py.MOUSEBUTTONDOWN:
                for i in reversed(list(Inventory)):
                    x, y, r = Inventory[i][0], Inventory[i][1], Inventory[i][2]
                    if (mouse_x - x) ** 2 + (mouse_y - y) ** 2 <= r ** 2:
                        holding_index = i
                        break

            elif event.type == py.MOUSEBUTTONUP:
                if holding_index is not None:
                    if Inventory[holding_index][1] < 500:
                        Inventory[holding_index][5] = 1
                    else:
                        Inventory[holding_index][5] = 0

                    save_data()
                holding_index = None
            
            elif event.type == py.KEYDOWN:
                if event.key == py.K_r:
                    for i in Inventory:
                        x, y, r, colour, type, wall = Inventory[i][0], Inventory[i][1], Inventory[i][2], Inventory[i][3], Inventory[i][4], Inventory[i][5]
                        wall = 0
                        y = 550
                        x = hold_info[i[:-2]][0]
                        Inventory[i][0], Inventory[i][1], Inventory[i][2], Inventory[i][3], Inventory[i][4], Inventory[i][5] = x, y, r, colour, type, wall

        if holding_index is not None:
            Inventory[holding_index][0] = mouse_x
            Inventory[holding_index][1] = mouse_y
        else:
            hold_change = True

        # Draw tray
        py.draw.rect(screen, "gray", py.Rect(0, HEIGHT - 100, WIDTH, 100))

        # Draw holds using Inventory for position (Inventory just tracks what exists)
        for i in Inventory:
            x, y, r, colour, type, wall = Inventory[i][0], Inventory[i][1], Inventory[i][2], Inventory[i][3], Inventory[i][4], Inventory[i][5]
           
            if y >= 500:
                wall = 0
                if holding_index != i:
                    y = 550
                    x = hold_info[i[:-2]][0]
                

            elif y <= 500 and holding_index != i:
                y = y - (y % y_hole_distance) + y_hole_distance/2
                x = x - (x % x_hole_distance) + x_hole_distance/2
            if wall == 0 or wall == 1:
                py.draw.circle(screen, colour, (x, y), r)
            
            Inventory[i][0], Inventory[i][1], Inventory[i][2], Inventory[i][3], Inventory[i][4], Inventory[i][5] = x, y, r, colour, type, wall

        # Draw wall hole spots
        for spot in wall_spots:
            py.draw.circle(screen, "red", spot, 2)

        py.display.flip()

def wall_2():
    global num_holds

    print("hello")

    WIDTH, HEIGHT = 500, 600
    screen = py.display.set_mode((WIDTH, HEIGHT))
    py.display.set_caption("Pygame Window")

    hold_change = True

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
                save_data()
                full_wall()
                running = False

            elif event.type == py.MOUSEBUTTONDOWN:
                for i in reversed(list(Inventory)):
                    x, y, r = Inventory[i][0], Inventory[i][1], Inventory[i][2]
                    if (mouse_x - x) ** 2 + (mouse_y - y) ** 2 <= r ** 2:
                        holding_index = i
                        break

            elif event.type == py.MOUSEBUTTONUP:
                if holding_index is not None:
                    if Inventory[holding_index][1] < 500:
                        Inventory[holding_index][5] = 2
                    else:
                        Inventory[holding_index][5] = 0

                    save_data()
                holding_index = None

            elif event.type == py.KEYDOWN:
                if event.key == py.K_r:
                    for i in Inventory:
                        x, y, r, colour, type, wall = Inventory[i][0], Inventory[i][1], Inventory[i][2], Inventory[i][3], Inventory[i][4], Inventory[i][5]
                        wall = 0
                        y = 550
                        x = hold_info[i[:-2]][0]
                        Inventory[i][0], Inventory[i][1], Inventory[i][2], Inventory[i][3], Inventory[i][4], Inventory[i][5] = x, y, r, colour, type, wall

        if holding_index is not None:
            Inventory[holding_index][0] = mouse_x
            Inventory[holding_index][1] = mouse_y
        else:
            hold_change = True

        # Draw tray
        py.draw.rect(screen, "gray", py.Rect(0, HEIGHT - 100, WIDTH, 100))

        # Draw holds using Inventory for position (Inventory just tracks what exists)
        for i in Inventory:
            
            x, y, r, colour, type, wall = Inventory[i][0], Inventory[i][1], Inventory[i][2], Inventory[i][3], Inventory[i][4], Inventory[i][5]
            # wall = 0
            # if wall == 0:
            #     y = 550
            #     x = hold_info[i[:-2]][0]
            if y >= 500 and holding_index != i:
                y = 550
                x = hold_info[i[:-2]][0]
                wall = 0
        
            elif y <= 500 and holding_index != i:
                y = y - (y % y_hole_distance) + y_hole_distance/2
                x = x - (x % x_hole_distance) + x_hole_distance/2

            if wall == 0 or wall == 2:
                py.draw.circle(screen, colour, (x, y), r)
            Inventory[i][0], Inventory[i][1], Inventory[i][2], Inventory[i][3], Inventory[i][4], Inventory[i][5] = x, y, r, colour, type, wall

        # Draw wall hole spots
        for spot in wall_spots:
            py.draw.circle(screen, "red", spot, 2)

        py.display.flip()

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
                wall_1()
            elif mouse_x > 350 and mouse_x < 650:
                running = False
                wall_2()

        py.draw.rect(screen, "green", py.Rect(25, 25, 300, 550))
        py.draw.rect(screen, "blue", py.Rect(350, 25, 300, 550))
        py.draw.rect(screen, "red", py.Rect(675, 25, 300, 550))
        py.display.flip()  # update screen

full_wall()

# Quit cleanly
py.quit()
