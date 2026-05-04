import pygame as py
import sys

# Initialise py
py.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption("Pygame Window")

# Clock (controls FPS)
clock = py.time.Clock()

# Main loop
running = True
while running:
    clock.tick(60)  # 60 FPS

    # --- Events ---
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False

    # --- Update ---
    # (game logic goes here)

    # --- Draw ---
    screen.fill((30, 30, 40))  # background colour

    py.display.flip()  # update screen

# Quit cleanly
py.quit()
sys.exit()