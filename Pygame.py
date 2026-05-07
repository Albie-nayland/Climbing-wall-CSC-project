import pygame as py
import sys

# Initialise py
py.init()

# Screen setup
WIDTH, HEIGHT = 500, 600
screen = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption("Pygame Window")

# Clock (controls FPS)
clock = py.time.Clock()

#Variables
offset = 0
does_offset = 1
mouse_offset = 0
wall_spots = []
holds_dict = {"small" : 5, "medium" : 5, "large" : 5}
holds_full_dict = {}
for i in holds_dict:
    for n in range(holds_dict[i]):
        if i == "small":
            holds_full_dict.update({len(holds_full_dict) : [50, 550, 15]})
        elif i == "medium":
            holds_full_dict.update({len(holds_full_dict) : [100, 550, 25]})
        elif i == "large":
            holds_full_dict.update({len(holds_full_dict) : [175, 550, 45]})
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
        elif event.type == py.MOUSEBUTTONDOWN:
            mouse_down = True
            for i in holds_full_dict:
                x, y, r = holds_full_dict[i]
                if (mouse_x - x)**2 + (mouse_y - y)**2 <= r**2:
                    holding_index = i
                    break

        elif event.type == py.MOUSEBUTTONUP:
            mouse_down = False
            holding_index = None
    # --- Update ---
    if holding_index is not None:
        holds_full_dict[holding_index][0] = mouse_x
        holds_full_dict[holding_index][1] = mouse_y

    for i in wall_spots:
        py.draw.circle(screen, "red", i, 2)


    if mouse_y % x_hole_distance < x_hole_distance/2:
        mouse_offset = x_hole_distance - x_hole_distance/4
    else:
        mouse_offset = x_hole_distance/4

    # --- DRAWING ---#
    py.draw.rect(screen, "gray", py.Rect(0, HEIGHT - 100, WIDTH, 100))
    for i in holds_full_dict:
        if holds_full_dict[i][1] % x_hole_distance < x_hole_distance/2:
            hold_offset = x_hole_distance - x_hole_distance/4
        else:
            hold_offset = x_hole_distance/4
        if holds_full_dict[i][1] < 500:
            holds_full_dict[i][0], holds_full_dict[i][1] = (holds_full_dict[i][0] - (holds_full_dict[i][0] % x_hole_distance) + hold_offset, (holds_full_dict[i][1] - (holds_full_dict[i][1] % y_hole_distance) + y_hole_distance/2))
            py.draw.circle(screen, "blue", (holds_full_dict[i][0], holds_full_dict[i][1]), holds_full_dict[i][2])
        else:
            if holding_index is None:
                if holds_full_dict[i][2] == 15:
                    holds_full_dict[i][0], holds_full_dict[i][1] = (50, 550)
                elif holds_full_dict[i][2] == 25:
                    holds_full_dict[i][0], holds_full_dict[i][1] = (100, 550)
                elif holds_full_dict[i][2] == 45:
                    holds_full_dict[i][0], holds_full_dict[i][1] = (175, 550)
            py.draw.circle(screen, "blue", (holds_full_dict[i][0], holds_full_dict[i][1]), holds_full_dict[i][2])


    py.display.flip()  # update screen

# Quit cleanly
py.quit()
sys.exit()