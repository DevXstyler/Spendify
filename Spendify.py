# Include librarys
from tkinter import *
from tkinter import ttk

#initialize tkinter
root = Tk()
root.configure(bg="black")

# Set the title of the window
root.title("Spendify")

# Set the size of the window
root.geometry("300x200")

# Create a frame to hold the widgets
frm = ttk.Frame(root, padding=10)

# Add the frame to the root window
frm.grid(column=0, row=0, sticky=(N, W, E, S))

#frm.grid() creates a grid layout for the frame 
# (means that widgets inside the frame will be arranged in a grid)
frm.grid()

# create and configure label
Welcome = "~Welcome to Spendifiy!~"
ttk.Label(frm, text=Welcome,background="black",foreground="white").grid(column=0, row=1)


ttk.Treeview(frm, columns=("Amount", "Category"), show='headings').grid(column=0, row=2)

# Create a button that closes the window
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=3)

#configure color of the frame
frm.configure(style="Black.TFrame")
style = ttk.Style()
style.configure("Black.TFrame", background="black")


#mainloop (this keeps the window open)
root.mainloop()

#ToDo:Configure Table - 