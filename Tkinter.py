import tkinter as tk
import os
import json

print("Looking for file in:", os.getcwd())

#Opens the main tkinter window and creates all the button text etc.
def TkinterUI():
    from main import PyGame
    global root, FilePath, Inventory

    Inventory = {
        "Hold1" : 0,
        "Hold2" : 0,
        "Hold3" : 0,
        "Hold4" : 0,
        "Hold5" : 0
    }

    ScriptDir = os.path.dirname(os.path.abspath(__file__))
    FilePath = os.path.join(ScriptDir, "Inventory.json")

    if os.path.exists(FilePath):
        try:
            with open(FilePath, 'r') as f:
                Data = json.load(f)
                for key in Inventory:
                    if key in Data:
                        Inventory[key] = Data[key]
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

    Hold1Button = tk.Button(InventoryWindow, text = "Add To Hold 1", command = lambda: AddInventory(1))
    Hold1Button.pack()

    Hold2Button = tk.Button(InventoryWindow, text = "Add To Hold 2", command = lambda: AddInventory(2))
    Hold2Button.pack()

    Hold3Button = tk.Button(InventoryWindow, text = "Add To Hold 3", command = lambda: AddInventory(3))
    Hold3Button.pack()

    Hold4Button = tk.Button(InventoryWindow, text = "Add To Hold 4", command = lambda: AddInventory(4))
    Hold4Button.pack()

    Hold5Button = tk.Button(InventoryWindow, text = "Add To Hold 5", command = lambda: AddInventory(5))
    Hold5Button.pack()


    ClearInventoryButton = tk.Button(InventoryWindow, text = "Clear Inventory", command = ClearInventory)
    ClearInventoryButton.pack()


#Adds inventory to the inventory variable
def AddInventory(Hold):
    global InventoryText, Inventory, FilePath
    Inventory[f"Hold{Hold}"] = InventoryText.get("1.0", "end-1c")
    SaveInventory()


def ClearInventory():
    global Inventory
    Inventory = {
        "Hold1" : 0,
        "Hold2" : 0,
        "Hold3" : 0,
        "Hold4" : 0,
        "Hold5" : 0
    }
    SaveInventory()


def SaveInventory():
    global InventoryLabel, Inventory
    with open(FilePath, 'w') as f:
        json.dump(Inventory, f, indent = 4)
    InventoryLabel.config(text = "Inventory: " + str(Inventory))
    print(Inventory)

if __name__ == "__main__":
    TkinterUI()



