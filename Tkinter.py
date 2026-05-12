import tkinter as tk
from tkinter import ttk
import os
import json

print("Looking for file in:", os.getcwd())

#Opens the main tkinter window and creates all the button text etc.
def TkinterUI():
    from main import PyGame
    global root, FilePath, Inventory, hold_info, num_holds

    Inventory = {}

    num_holds = {}
    hold_info = {}

    ScriptDir = os.path.dirname(os.path.abspath(__file__))
    FilePath = os.path.join(ScriptDir, "Inventory.json")

    if os.path.exists(FilePath):
        try:
            with open(FilePath, 'r') as f:
                Data = json.load(f)
                if "num_holds" in Data:
                    num_holds = Data["num_holds"]  
                if "hold_info" in Data:
                    hold_info = Data["hold_info"]              
        except:
            pass

    Inventory = num_holds

    root = tk.Tk()
    root.geometry("500x500")

    InventoryButton = tk.Button(text = "Inventory", command = InventoryWindow)
    InventoryButton.pack()

    VisualizeButton = tk.Button(text = "Visualize", command = PyGame)
    VisualizeButton.pack()
    print(num_holds)
    print(hold_info)
    root.mainloop()

#Opens the inventory window
def InventoryWindow():
    global root, InventoryText, Inventory, InventoryLabel, hold_info, ColorText, HoldTypeBox, SizeBox, HoldBox
    InventoryWindow = tk.Toplevel(root)
    InventoryWindow.geometry("500x500")
    HoldTypes = ["Crimp", "Jug", "Pinch", "Slooper"]
    Sizes = ["1", "2", "3", "4", "5", "10", "15", "20"]
    Holds = ["New",]


    InventoryLabel = tk.Label(InventoryWindow, text = "Inventory: " + str(Inventory))
    InventoryLabel.pack()

    InventoryText = tk.Text(InventoryWindow, height = 1, width = 30)
    InventoryText.pack()

    ColorLabel = tk.Label(InventoryWindow, text = "Color")
    ColorLabel.pack()

    ColorText = tk.Text(InventoryWindow, height = 1, width = 30)
    ColorText.pack()

    HoldTypeBox = ttk.Combobox(InventoryWindow, values = HoldTypes)
    HoldTypeBox.pack()

    SizeBox = ttk.Combobox(InventoryWindow, values = Sizes)
    SizeBox.pack()

    for i in Inventory:
        Holds.append(i)
    print(Holds)


    HoldBox = ttk.Combobox(InventoryWindow, values = Holds)
    HoldBox.pack()
    
    AddInventoryButton = tk.Button(InventoryWindow, text = "Add Inventory", command = AddInventory)
    AddInventoryButton.pack()

    SaveInventoryButton = tk.Button(InventoryWindow, text = "Save Inventory", command = SaveInventory)
    SaveInventoryButton.pack()

    ClearInventoryButton = tk.Button(InventoryWindow, text = "Clear Inventory", command = ClearInventory)
    ClearInventoryButton.pack()


    
    


def AddInventory():
    global Inventory, InventoryText, ColorText, HoldTypeBox, SizeBox, HoldBox, num_holds
    amount = InventoryText.get("1.0", "end-1c")
    Color = ColorText.get("1.0", "end-1c")
    HoldType = HoldTypeBox.get()
    Size = SizeBox.get()
    Hold = HoldBox.get()

    if Hold == "New":
        NewHoldNumber = 1
        for i in hold_info:
            NewHoldNumber = NewHoldNumber + 1

        hold_info["hold" + str(NewHoldNumber)] = [300, 550, Size, Color, HoldType]
        num_holds["hold" + str(NewHoldNumber)] = [amount]
        print (hold_info)
        print(num_holds)
        

        


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
    global InventoryLabel, Inventory, hold_info
    with open(FilePath, 'w') as f:
        json.dump(Inventory, f, indent = 4)
        json.dump(hold_info, f, indent = 4 )
    InventoryLabel.config(text = "Inventory: " + str(Inventory))
    print(Inventory)

if __name__ == "__main__":
    TkinterUI()



