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

# Tabelle mit weißem Rahmen
table_frame = Frame(frm, bg="white", bd=2)
table_frame.grid(column=0, row=2, columnspan=2, padx=5, pady=5)
def CreateTable():
    global tree
    tree = ttk.Treeview(
        table_frame,
        columns=("Item", "Price"),
        show='headings'
    )
    tree.heading("Item", text="Item")
    tree.heading("Price", text="Price")
    tree.column("Item", width=80, anchor="center")
    tree.column("Price", width=120, anchor="w")

    # Style anpassen
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", 
        background="#222222",         # dunkles Grau für leere Felder
        foreground="white",           # weiß für Text
        fieldbackground="#222222",    # dunkles Grau für leere Felder
        rowheight=25,
        font=("Arial", 10)
    )


    style.configure("Cusotom.TButton",
        background="#444444",         # helleres Grau für Schaltflächen)
        foreground="white",           # weiß für Text in Schaltflächen
        font=("Arial", 10, "bold")   
    )

    style.map("Custom.TButton",
    background=[("active", "#666666")],   # Hintergrund beim Hover/Klick
    foreground=[("active", "white")]
    )
    
    style.configure("Treeview.Heading",
        background="#444444",         # helleres Grau für Kopfzeile (Kategorien)
        foreground="white",           # weiß für Text in Kopfzeile
        font=("Arial", 10, "bold")
    )
    style.map("Treeview.Heading",
        background=[("active", "#666666")],  # helleres Grau beim Hover/Klick
        foreground=[("active", "white")]
    )


    style.map("Treeview", 
        background=[("selected", "#333333")], 
        foreground=[("selected", "#ffffff")]
    )

    # Alternate row color (dunkleres Grau für belegte Zeilen)
    style.configure("Treeview", 
        background="#222222", 
        foreground="white", 
        fieldbackground="#222222"
    )
    style.map("Treeview", background=[("selected", "#333333")])

    tree.tag_configure('filled', background="#181818")  # noch dunkleres Grau für belegte Zeilen

    # Beispiel-Daten einfügen mit Tag für belegte Zeilen
    tree.insert("", "end", values=("Football", "$10"), tags=('filled',))
    tree.insert("", "end", values=("Pair Socks", "$5"), tags=('filled',))




    tree.pack(padx=2, pady=2)
def CreateLabel():
    # create and configure label
    Welcome = "~Welcome to Spendifiy!~"
    label = ttk.Label(frm, text=Welcome, background="black", foreground="white", font=("Arial", 14), anchor="center")
    label.grid(column=0, row=1, columnspan=2, sticky="w", pady=10, ipadx=10, ipady=2)


def delete_selected_item():
    selected = tree.selection()
    if not selected:
        pass
    else:
        tree.delete(selected)
        print("Deleted Item:",selected)
    
    
def open_add_item_window():
    add_win = Toplevel(root)
    add_win.title("Add Item")
    add_win.configure(bg="black")
    add_win.geometry("250x120")
    add_win.resizable(False, False)

    Label(add_win, text="Item:", bg="black", fg="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_item = Entry(add_win)
    entry_item.grid(row=0, column=1, padx=10, pady=5)
    Label(add_win, text="Price:", bg="black", fg="white").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry_prize = Entry(add_win)
    entry_prize.grid(row=1, column=1, padx=10, pady=5)

    def add_to_table():
        item = entry_item.get()
        prize = entry_prize.get()

        # Check if fields are empty
        if not item or not prize:
            err_win_empty = Toplevel(root)
            err_win_empty.title("Error - Empty Fields")
            err_win_empty.configure(bg="red")
            err_win_empty.geometry("380x200")
            err_win_empty.resizable(False, False)
            Label(err_win_empty, text="Please fill in all fields.", bg="red", fg="white", font=("Arial", 12, "bold")).pack(pady=20)
            Button(
                err_win_empty,
                text="Okay",
                command=err_win_empty.destroy,
                bg="#444444",
                fg="white",
                font=("Arial", 11, "bold"),
                width=12,
                height=2
            ).pack(pady=5)
            return

        # Check if prize is a valid integer and item is a string
        try:
            prize_int = int(prize)
        except ValueError:
            err_win_invalid_type = Toplevel(root)
            err_win_invalid_type.title("Error - Invalid Type")
            err_win_invalid_type.configure(bg="red")
            err_win_invalid_type.geometry("380x200")
            err_win_invalid_type.resizable(False, False)
            Label(err_win_invalid_type, text="Invalid Type! Price must be a number.", bg="red", fg="white", font=("Arial", 12, "bold")).pack(pady=20)
            Button(
                err_win_invalid_type,
                text="Okay",
                command=err_win_invalid_type.destroy,
                bg="#444444",
                fg="white",
                font=("Arial", 11, "bold"),
                width=12,
                height=2
            ).pack(pady=5)
            return

        # Optional: Check if item is only letters (no numbers)
        if not item.isalpha(): # isalpha checks if all characters are letters
            err_win_invalid_type = Toplevel(root)
            err_win_invalid_type.title("Error - Invalid Item")
            err_win_invalid_type.configure(bg="red")
            err_win_invalid_type.geometry("380x200")
            err_win_invalid_type.resizable(False, False)
            Label(err_win_invalid_type, text="Invalid Item! Name must only contain letters.", bg="red", fg="white", font=("Arial", 12, "bold")).pack(pady=20)
            Button(
                err_win_invalid_type,
                text="Okay",
                command=err_win_invalid_type.destroy,
                bg="#444444",
                fg="white",
                font=("Arial", 11, "bold"),
                width=12,
                height=2
            ).pack(pady=5)
            return

        # If all checks pass, insert into table
        tree.insert("", "end", values=(item, prize_int), tags=('filled',))
        add_win.destroy()
        
                   
    add_btn = Button(add_win, text="Add", command=add_to_table, bg="#444444", fg="white")
    add_btn.grid(row=2, column=0, columnspan=2, pady=10)
    
def delete_selected_item():
    selected = tree.selection()
    if not selected:
        pass
    else:
        print("Deleted item:", selected)
        tree.delete(selected)
 
 

def  edit_selected_item():
    
    selected = tree.selection()
    if not tree.selection(): # if NO selection
        no_selection_win = Toplevel(root)
        no_selection_win.title("Error - No Selection")
        no_selection_win.configure(bg="red")
        no_selection_win.geometry("380x200")
        no_selection_win.resizable(False, False)
        Label(no_selection_win, text="Please select an item to edit.", bg="red", fg="white", font=("Arial", 12, "bold")).pack(pady=20)
        Button(
            no_selection_win,
            text="Okay",
            command=no_selection_win.destroy,
            bg="#444444",
            fg="white",
            font=("Arial", 11, "bold"),
            width=12,
            height=2
        ).pack(pady=5)
        return
    else: #if there IS a selection
            selected = tree.selection()
            values = tree.item(selected, 'values') #get selected + values
            print(values)
            item_edit = values[0] #item
            price_edit = values[1] #price

            edit_win = Toplevel(root)
            edit_win.title("Edit Values")
            edit_win.configure(bg="black")
            edit_win.geometry("380x200")
            edit_win.resizable(False, False)
            Label(edit_win, text="Please fill in all fields.", bg="red", fg="white", font=("Arial", 12, "bold")).pack(pady=20)
            Button(
                edit_win,
                text="Okay",
                command=edit_win.destroy,
                bg="#444444",
                fg="white",
                font=("Arial", 11, "bold"),
                width=12,
                height=2
            ).pack(pady=5)
            return

            # Check if prize is a valid integer and item is a string
            try:
                prize_int = int(prize)
            except ValueError:
                err_win_invalid_type = Toplevel(root)
                err_win_invalid_type.title("Error - Invalid Type")
                err_win_invalid_type.configure(bg="red")
                err_win_invalid_type.geometry("380x200")
                err_win_invalid_type.resizable(False, False)
                
                Label(add_win, text="Item:", bg="black", fg="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
                item_edit = Entry(add_win)
                item_edit.grid(row=0, column=1, padx=10, pady=5)
                Label(add_win, text="Price:", bg="black", fg="white").grid(row=1, column=0, padx=10, pady=5, sticky="w")
                price_edit = Entry(add_win)
                price_edit.grid(row=1, column=1, padx=10, pady=5)
                Button(
                    err_win_invalid_type,
                    text="Okay",
                    command=err_win_invalid_type.destroy,
                    bg="#444444",
                    fg="white",
                    font=("Arial", 11, "bold"),
                    width=12,
                    height=2
                ).pack(pady=5)
                return

            # Optional: Check if item is only letters (no numbers)
            if not item.isalpha(): # isalpha checks if all characters are letters
                err_win_invalid_type = Toplevel(root)
                err_win_invalid_type.title("Error - Invalid Item")
                err_win_invalid_type.configure(bg="red")
                err_win_invalid_type.geometry("380x200")
                err_win_invalid_type.resizable(False, False)
                Label(err_win_invalid_type, text="Invalid Item! Name must only contain letters.", bg="red", fg="white", font=("Arial", 12, "bold")).pack(pady=20)
                Button(
                    err_win_invalid_type,
                    text="Okay",
                    command=err_win_invalid_type.destroy,
                    bg="#444444",
                    fg="white",
                    font=("Arial", 11, "bold"),
                    width=12,
                    height=2
                ).pack(pady=5)
                return

            # If all checks pass, insert into table
            tree.insert("", "end", values=(item, prize_int), tags=('filled',))
            add_win.destroy()
        
 
 
 
        
def CreateButtons():
    global style
    style = ttk.Style()
    style.configure("Custom.TButton",
        background="#444444",      # Button-Hintergrund
        foreground="white",        # Button-Textfarbe
        font=("Arial", 11, "bold")
    )
    style.map("Custom.TButton",
        background=[("active", "#666666")],   # Hintergrund beim Hover/Klick
        foreground=[("active", "white")]
    )
    def CreateButtonAdd(): 
        add_button = ttk.Button(frm, text="Add Item", style="Custom.TButton", command=open_add_item_window,  width=12)
        add_button.grid(column=0, row=3, sticky="w", padx=10, pady=5)   

    def CreateButtonDelete():
        delete_button = ttk.Button(frm, text="Delete Item", style="Custom.TButton", command=delete_selected_item, width=12)
        delete_button.grid(column=1, row=3, sticky="w", padx=5, pady=5)

    def CreatebuttonEdit():
        edit_button = ttk.Button(frm, text="Edit Item", style="Custom.TButton", command=edit_selected_item,  width=12)
        edit_button.grid(column=0, row=4, sticky="w", padx=10, pady=5)

    def CreateButtonClose():
        close_button = ttk.Button(frm, text="Close", style="Custom.TButton", command=root.destroy, width=12)
        close_button.grid(column=1, row=4, sticky="w", padx=5, pady=5)
       
    CreateButtonAdd()
    CreateButtonDelete()
    CreatebuttonEdit()
    CreateButtonClose() 

    
CreateTable() 
CreateLabel()
CreateButtons()
#configure color of the frame
frm.configure(style="Black.TFrame")
style = ttk.Style()
style.configure("Black.TFrame", background="black")

#mainloop (this keeps the window open)
root.mainloop()

#ToDo:buttion functionality - resize window dynamic - logo - currency converter