#Run the PyGame script in this function
def PyGame():
    print("PyGame")

#This function runs the tkinter file and opens the tkinter window
#BUG the run tkinter runs mutiple times after closing the window
def RunTkinter():
    import Tkinter
    Tkinter.TkinterUI()

RunTkinter()
