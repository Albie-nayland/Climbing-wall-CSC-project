import tkinter as tk
import json

Inverntory = 0

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
    print(Inverntory)

    root.mainloop()

#Opens the inventory window
def InventoryWindow():
    global root, InventoryText
    InventoryWindow = tk.Toplevel(root)
    InventoryWindow.geometry("500x500")

    InventoryTitle = tk.Label(InventoryWindow, text = "Inventory")
    InventoryTitle.pack()

    InventoryText = tk.Text(InventoryWindow, height = 1, width = 30)
    InventoryText.pack()

    AddButton = tk.Button(InventoryWindow, text = "Add To Inventory", command = AddInventory)
    AddButton.pack()

#Adds inventory to the inventory variable
def AddInventory():
    global InventoryText, Inverntory
    Inverntory = Inverntory + int(InventoryText.get("1.0", "end-1c"))
    print(Inverntory)

TkinterUI()



