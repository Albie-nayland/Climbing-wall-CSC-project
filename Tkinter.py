import tkinter as tk
import os
import json

print("Looking for file in:", os.getcwd())

#Opens the main tkinter window and creates all the button text etc.
def TkinterUI():
    from main import PyGame
    global root, FilePath, Inventory

    Inventory = 0

    ScriptDir = os.path.dirname(os.path.abspath(__file__))
    FilePath = os.path.join(ScriptDir, "Inventory.json")

    if os.path.exists(FilePath):
        try:
            with open(FilePath, 'r') as f:
                Inventory = json.load(f)
        except:
            pass
                

    root = tk.Tk()
    root.geometry("500x500")

    InventoryButton = tk.Button(text = "Inventory", command = InventoryWindow)
    InventoryButton.pack()

    VisualizeButton = tk.Button(text = "Visualize", command = PyGame)
    VisualizeButton.pack()
    print(Inventory)

    root.mainloop()

#Opens the inventory window
def InventoryWindow():
    global root, InventoryText, Inventory, InventoryLabel
    InventoryWindow = tk.Toplevel(root)
    InventoryWindow.geometry("500x500")

    InventoryLabel = tk.Label(InventoryWindow, text = "Inventory: " + str(Inventory))
    InventoryLabel.pack()

    InventoryText = tk.Text(InventoryWindow, height = 1, width = 30)
    InventoryText.pack()

    AddButton = tk.Button(InventoryWindow, text = "Add To Inventory", command = AddInventory)
    AddButton.pack()

    ClearInventoryButton = tk.Button(InventoryWindow, text = "Clear Inventory", command = ClearInventory)
    ClearInventoryButton.pack()

#Adds inventory to the inventory variable
def AddInventory():
    global InventoryText, Inventory, FilePath
    Inventory = Inventory + int(InventoryText.get("1.0", "end-1c"))
    SaveInventory()

def ClearInventory():
    global Inventory
    Inventory = 0
    SaveInventory()

def SaveInventory():
    global InventoryLabel, Inventory
    with open(FilePath, 'w') as f:
        json.dump(Inventory, f, indent = 4)
    InventoryLabel.config(text = "Inventory: " + str(Inventory))
    print(Inventory)

TkinterUI()



