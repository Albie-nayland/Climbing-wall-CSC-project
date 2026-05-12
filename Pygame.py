import pygame as py
import os, json

# Initialise py
py.init()

num_holds = {}
hold_info = {}
hold_pos = {}
wall_1_holds = {}
wall_1_hold_info = {}

dicts = {
    "num_holds" : num_holds,
    "hold_info" : hold_info,
    "hold_pos" : hold_pos
}

ScriptDir = os.path.dirname(os.path.abspath(__file__))
FilePath = os.path.join(ScriptDir, "num_holds.json")

if os.path.exists(FilePath):
        try:
            with open(FilePath, 'r') as f:
                Data = json.load(f)
                for key in Data:
                    for i in Data[key]:
                        dicts[key].update({i:Data[key][i]})
        except:
            pass
print(num_holds)
for i in num_holds:
    for j in range(num_holds[i]):
        hold_pos.update({i + "_" + j:(hold_info[i][0], hold_info[i][1])})
print(hold_pos)


#Variables
mouse_down = False
offset = 0
does_offset = 1
mouse_offset = 0
wall_spots = []

def wall_1():
    
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
            elif event.type == py.MOUSEBUTTONDOWN:
                for i in num_holds:
                    x, y, r = hold_info[i][0], hold_info[i][1], hold_info[i][2]
                    if (mouse_x - x)**2 + (mouse_y - y)**2 <= r**2:
                        holding_index = i
                        break
                
            elif event.type == py.MOUSEBUTTONUP:
                holding_index = None

        if holding_index is not None:
            hold_info[holding_index][0] = mouse_x
            hold_info[holding_index][1] = mouse_y

        for i in num_holds:
            x, y, r = hold_info[i][0], hold_info[i][1], hold_info[i][2]
            if y <= 500:
                num_holds.update({i:num_holds[i] - 1})
                wall_1_hold_info.update({i:hold_info[i]})
                if i in wall_1_holds:
                    wall_1_holds[i] += 1
                else:
                    wall_1_holds.update({i:1})
        

        # if mouse_y % x_hole_distance < x_hole_distance/2:
        #     mouse_offset = x_hole_distance - x_hole_distance/4
        # else:
        #     mouse_offset = x_hole_distance/4        

        #Drawing
        py.draw.rect(screen, "gray", py.Rect(0, HEIGHT - 100, WIDTH, 100))

        for i in wall_spots:
            py.draw.circle(screen, "red", i, 2)

        for i in num_holds:
                for j in range(num_holds[i]):
                    py.draw.circle(screen, hold_info[i][3], (hold_info[i][0], hold_info[i][1]), hold_info[i][2])

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
