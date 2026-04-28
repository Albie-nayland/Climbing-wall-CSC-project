import tkinter as tk
import json

#Opens the main tkinter window and creates all the button text etc.
def TkinterUI():
    from main import PyGame
    global root
    root = tk.Tk()
    root.geometry("500x500")

    InventoryButton = tk.Button(text = "Inventory", command = InventoryWindow)
    InventoryButton.pack()

    VisualizeButton = tk.Button(text = "Visualize", command = PyGame)
    VisualizeButton.pack()

    root.mainloop()

#Opens the inventory window
def InventoryWindow():
    global root
    InventoryWindow = tk.Toplevel(root)
    InventoryWindow.geometry("500x500")


    InventoryTitle = tk.Label(InventoryWindow, text = "Inventory")
    InventoryTitle.pack()


TkinterUI()



