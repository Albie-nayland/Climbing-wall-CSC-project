import tkinter as tk
from tkinter import ttk
import os
import json

print("Looking for file in:", os.getcwd())

#Opens the main tkinter window and creates all the button text etc.
def TkinterUI():
    from main import PyGame
    global root, FilePath, Inventory, hold_info, num_holds

    num_holds = {}
    hold_info = {}
    Inventory = {}

    ScriptDir = os.path.dirname(os.path.abspath(__file__))
    FilePath = os.path.join(ScriptDir, "Inventory.json")

    if os.path.exists(FilePath):
        try:
            with open(FilePath, 'r') as f:
                Data = json.load(f)
                if "hold_info" in Data:
                    hold_info = Data["hold_info"]   
                if "Inventory" in Data:
                    Inventory = Data["Inventory"]           
        except:
            pass

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

    AmountLabel = tk.Label(InventoryWindow, text = "Amount")
    AmountLabel.pack()

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

    for i in hold_info:
        Holds.append(i)
    print(Holds)


    HoldBox = ttk.Combobox(InventoryWindow, values = Holds)
    HoldBox.pack()
    
    AddInventoryButton = tk.Button(InventoryWindow, text = "Add Inventory", command = AddInventory)
    AddInventoryButton.pack()

    RemoveInventoryButton = tk.Button(InventoryWindow, text = "Remove Inventory", command = RemoveInventory)
    RemoveInventoryButton.pack()

    SaveInventoryButton = tk.Button(InventoryWindow, text = "Save Inventory", command = SaveInventory)
    SaveInventoryButton.pack()

    ClearInventoryButton = tk.Button(InventoryWindow, text = "Clear Inventory", command = ClearInventory)
    ClearInventoryButton.pack()


def AddInventory():
    global Inventory, InventoryText, ColorText, HoldTypeBox, SizeBox, HoldBox
    amount = InventoryText.get("1.0", "end-1c")
    Color = ColorText.get("1.0", "end-1c")
    HoldType = HoldTypeBox.get()
    Size = SizeBox.get()
    Hold = HoldBox.get()

    HoldData = [int(Size), Color.lower(), HoldType.lower()]

    if Hold == "New":
        if not any(v[2:5] == HoldData for v in hold_info.values()):

         hold_info[str(Color) + "_" + str(HoldType.lower()) + "_0"] = [50, 550, int(Size), Color, HoldType]
         print (hold_info)

         HoldNumber = 0
         for i in range(int(amount)):
             Inventory[str(Color) + "_" + str(HoldType.lower()) + "_0_" + str(HoldNumber)] = [50, 550, int(Size), Color, HoldType, 0]
             HoldNumber = HoldNumber + 1


        else:
         print("error")
        
    else:
        num_holds[Hold] = int(num_holds[Hold]) + int(amount)
        print(num_holds)
    

def RemoveInventory():
    global HoldBox, InventoryText
    amount = InventoryText.get("1.0", "end-1c")
    Hold = HoldBox.get()
    if Hold in hold_info:
        for i in range(int(amount)):
         Matching = [j for j in Inventory if j.startswith(Hold + "_")]
         if Matching:
             del Inventory[Matching[-1]]
        if not any(j.startswith(Hold + "_") for j in Inventory):
             del hold_info[Hold]
    print(Inventory)


def ClearInventory():
    global Inventory, hold_info
    hold_info = {}
    Inventory = {}


def SaveInventory():
    global InventoryLabel, Inventory, hold_info

    data = {
        "hold_info": hold_info,
        "Inventory": Inventory
    }

    with open(FilePath, 'w') as f:
        json.dump(data, f, indent = 2)

    InventoryLabel.config(text = "Inventory: " + str(Inventory))
    print(Inventory)


if __name__ == "__main__":
    TkinterUI()



