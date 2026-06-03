import pygame as py
import os, json

# Initialize all imported pygame modules
py.init()

# --- Global Data Structures ---
num_holds = {}    # Tracks the number/counts of specific holds
hold_info = {}    # Stores base layout definitions (e.g., default tray X-coordinates)
Inventory = {}    # Main state tracker for instantiated holds. 
                  # Format per item: [x, y, radius, colour, type, wall_id]

# A convenience dictionary mapping string keys to their actual dictionary objects
# loops through this to cleanly parse and distribute loaded JSON data.
dicts = {
    "num_holds": num_holds,
    "hold_info": hold_info,
    "Inventory": Inventory
}

# --- File I/O (Save/Load system) ---
# Determine the directory of the currently running script to prevent path issues
ScriptDir = os.path.dirname(os.path.abspath(__file__))
FilePath = os.path.join(ScriptDir, "Inventory.json")

# Load existing save data if the file exists
if os.path.exists(FilePath):
    try:
        with open(FilePath, 'r') as f:
            Data = json.load(f)
            # Update the global dictionaries with the saved data
            for key in Data:
                for i in Data[key]:
                    dicts[key].update({i: Data[key][i]})
    except Exception as e:
        print(f"Failed to load save: {e}")

def save_data():
    """Serializes the current state of the application into a JSON file."""
    with open(FilePath, 'w') as f:
        json.dump({
            "num_holds": num_holds,
            "hold_info": hold_info,
            "Inventory": Inventory
        }, f, indent=2)

# --- Wall 1 Interface ---
def wall_1():
    global num_holds

    # Dimensions for the Wall 1 sub-window
    WIDTH, HEIGHT = 397, 600
    screen = py.display.set_mode((WIDTH, HEIGHT))
    py.display.set_caption("Slab wall")

    wall_image = py.image.load("Climbing-wall-CSC-project\Slab wall CSC.png").convert_alpha()
    wall_image = py.transform.scale(wall_image, (WIDTH + 492, HEIGHT - 95))

    hold_change = True
    holding_index = None  # Tracks the key of the hold currently being dragged
    
    # Grid setup parameters for snapping system
    y_hole_distance = 20
    x_hole_distance = 20
    offset = x_hole_distance / 2
    wall_spots = []
    
    # Generate the coordinate positions for the red grid background holes
    for n in range(HEIGHT - 100): # Stop 100px short of the bottom to account for the tray
        if n % y_hole_distance == 0:
            for i in range(WIDTH):
                if i % x_hole_distance == 0:
                    # Centers the coordinate inside the imaginary grid cell
                    wall_spots.append((i + offset, n + y_hole_distance / 2))

    running = True
    while running:
        screen.fill("black")
        screen.blit(wall_image, (-3, 0))
        mouse_x, mouse_y = py.mouse.get_pos()

        # Event processing loop
        for event in py.event.get():
            if event.type == py.QUIT:
                save_data()      # Auto-save layout on close
                full_wall()      # Return back to the main selector wall
                running = False
                
            elif event.type == py.MOUSEBUTTONDOWN:
                # Iterate backward through the inventory so items drawn on top are selected first
                for i in reversed(list(Inventory)):
                    x, y, r = Inventory[i][0], Inventory[i][1], Inventory[i][2]
                    # Pythagorean theorem to check if click is inside the circular hold boundary
                    if (mouse_x - x) ** 2 + (mouse_y - y) ** 2 <= r ** 2:
                        holding_index = i
                        break # Stop looking; we found our dragged object

            elif event.type == py.MOUSEBUTTONUP:
                if holding_index is not None:
                    # If released above the bottom tray (Y < 500), assign it to Wall 1
                    if Inventory[holding_index][1] < 500:
                        Inventory[holding_index][5] = 1 # wall_id index updated
                    else:
                        Inventory[holding_index][5] = 0 # 0 means it's sitting unassigned in the tray

                    save_data()
                holding_index = None # Drop the hold
            
            elif event.type == py.KEYDOWN:
                # Reset shortcut: If 'R' is pressed, clear all items back to the tray
                if event.key == py.K_r:
                    for i in Inventory:
                        x, y, r, colour, type, wall = Inventory[i][0], Inventory[i][1], Inventory[i][2], Inventory[i][3], Inventory[i][4], Inventory[i][5]
                        wall = 0
                        y = 550 # Tray center line
                        # Extract the base name (strip off unique instance characters) to find default X pos
                        x = hold_info[i[:-2]][0]
                        Inventory[i][0], Inventory[i][1], Inventory[i][2], Inventory[i][3], Inventory[i][4], Inventory[i][5] = x, y, r, colour, type, wall

        # Dragging logic: Lock hold positions directly to mouse coordinates
        if holding_index is not None:
            Inventory[holding_index][0] = mouse_x
            Inventory[holding_index][1] = mouse_y
        else:
            hold_change = True

        # Draw the gray bottom tray
        py.draw.line(screen, "Dark green", (170, 0), (-30, HEIGHT), 10)
        py.draw.rect(screen, "gray", py.Rect(0, HEIGHT - 105, WIDTH, 105))

        # Position calculator and rendering routine for active holds
        for i in Inventory:
            x, y, r, colour, type, wall = Inventory[i][0], Inventory[i][1], Inventory[i][2], Inventory[i][3], Inventory[i][4], Inventory[i][5]
           
            # Behavior if item is sitting in or near the tray area
            if y >= 500:
                wall = 0
                if holding_index != i: # If not being dragged, lock to tray base center lines
                    y = 550
                    x = hold_info[i[:-2]][0]
                
            # Behavior if item is placed up on the climbing wall structure
            elif y <= 500 and holding_index != i:
                # Snapping formula: Locks hold coordinates mathematically to the closest grid node
                y = y - (y % y_hole_distance) + y_hole_distance/2 
                x = x - (x % x_hole_distance) + x_hole_distance/2 - 3
            
            # Render item only if it belongs to the Tray (0) or this active window (1)
            if wall == 0 or wall == 1:
                py.draw.circle(screen, colour, (x, y), r)
            
            # Commit any recalculated grid modifications back to state dict
            Inventory[i][0], Inventory[i][1], Inventory[i][2], Inventory[i][3], Inventory[i][4], Inventory[i][5] = x, y, r, colour, type, wall

        # Render background grid layout dots
        # for spot in wall_spots:
        #     py.draw.circle(screen, "red", spot, 1)

        py.display.flip()

# --- Wall 2 Interface ---
def wall_2():
    global num_holds

    # Dimensions for Wall 2 sub-window
    WIDTH, HEIGHT = 750, 600
    screen = py.display.set_mode((WIDTH, HEIGHT))
    py.display.set_caption("Vertical wall")

    wall_image = py.image.load("Climbing-wall-CSC-project\Climbing wall vert 2.png").convert_alpha()
    wall_image = py.transform.scale(wall_image, (WIDTH + 170, HEIGHT - 80))

    hold_change = True
    holding_index = None
    
    # Grid setup parameters identical to Wall 1
    y_hole_distance = 20
    x_hole_distance = 20
    offset = x_hole_distance/2
    wall_spots = []
    
    # Generate background grid positions
    for n in range(HEIGHT - 100):
        if n % y_hole_distance == 0:
            for i in range(WIDTH):
                if i % x_hole_distance == 0:
                    wall_spots.append((i + offset, n + y_hole_distance / 2))

    running = True
    while running:
        screen.fill("black")
        screen.blit(wall_image, (0,-1))
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
                    # If dropped high up, assign it to Wall ID 2
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

        py.draw.line(screen, "dark green", (WIDTH + 26, 0), (WIDTH-190, HEIGHT), 10)
        py.draw.line(screen, "dark green", (240, 0), (-130, HEIGHT), 10)

        # Draw tray
        py.draw.rect(screen, "gray", py.Rect(0, HEIGHT - 100, WIDTH, 100))

        # Dynamic positioning and drawing calculation loop
        for i in Inventory:
            x, y, r, colour, type, wall = Inventory[i][0], Inventory[i][1], Inventory[i][2], Inventory[i][3], Inventory[i][4], Inventory[i][5]
            
            if y >= 500 and holding_index != i:
                y = 550
                x = hold_info[i[:-2]][0]
                wall = 0
        
            elif y <= 500 and holding_index != i:
                y = y - (y % y_hole_distance) + y_hole_distance/2
                x = x - (x % x_hole_distance) + x_hole_distance/2

            # Render logic explicit to Wall 2 (Draw if tray item or Wall 2 item)
            if wall == 0 or wall == 2:
                py.draw.circle(screen, colour, (x, y), r)
            Inventory[i][0], Inventory[i][1], Inventory[i][2], Inventory[i][3], Inventory[i][4], Inventory[i][5] = x, y, r, colour, type, wall

            

        py.display.flip()

# --- Wall 3 Interface ---
def wall_3():
    global num_holds

    # Dimensions for Wall 2 sub-window
    WIDTH, HEIGHT = 750, 600
    screen = py.display.set_mode((WIDTH, HEIGHT))
    py.display.set_caption("Vertical wall")

    wall_image = py.image.load("Coming soon.png").convert_alpha()
    wall_image = py.transform.scale(wall_image, (WIDTH, HEIGHT))

    hold_change = True
    holding_index = None


    running = True
    while running:
        screen.fill("black")
        screen.blit(wall_image, (0,0))
        mouse_x, mouse_y = py.mouse.get_pos()

        for event in py.event.get():
            if event.type == py.QUIT:
                save_data()
                full_wall()
                running = False

        py.display.flip()

# --- Main Dashboard / Hub Selector ---
def full_wall():
    mouse_down = False
    
    

    # Large format display layout to accommodate choice pillars
    WIDTH, HEIGHT = 1000, 600
    screen = py.display.set_mode((WIDTH, HEIGHT))
    
    py.display.set_caption("Pygame Window")
    
    running = True
    while running:
        
        mouse_x, mouse_y = py.mouse.get_pos()
        
        for event in py.event.get():
            if event.type == py.QUIT:
                running = False
            elif event.type == py.MOUSEBUTTONDOWN:
                mouse_down = True
            elif event.type == py.MOUSEBUTTONUP:
                mouse_down = False
                
        # Click/Navigation Boundaries detection
        if mouse_y > 25 and mouse_y < 575 and mouse_down:
            # If clicked inside Green Pillar column bounds -> Open Wall 1
            if mouse_x > 25 and mouse_x < 325:
                running = False
                wall_3()
            # If clicked inside Blue Pillar column bounds -> Open Wall 2
            elif mouse_x > 350 and mouse_x < 650:
                running = False
                wall_2()
            elif mouse_x > 675 and mouse_x < 975:
                running = False
                wall_1()

        # Render choice pillar graphics to screen
        py.draw.rect(screen, "green", py.Rect(25, 25, 300, 550))  # Pillar 1 (Wall 1 Button)
        py.draw.rect(screen, "blue", py.Rect(350, 25, 300, 550))   # Pillar 2 (Wall 2 Button)
        py.draw.rect(screen, "red", py.Rect(675, 25, 300, 550))    # Pillar 3 (Unused/Empty option)
        
        py.display.flip()  

# --- Entry Point Execution ---
full_wall()

# Safe shutdown procedure once main wrapper loops complete
py.quit()