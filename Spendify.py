# Include librarys
from tkinter import *
from tkinter import ttk
import os 
import json

USERDATA_DIR = os.path.join(os.path.expanduser("~"), ".spendifiy")
USERDATA_FILE = os.path.join(USERDATA_DIR, "userdata.json")



#initialize tkinter
root = Tk()
root.configure(bg="black")




selected_currency = StringVar()
selected_currency.set("US Dollar")  # Default currency

def save_userdata():
    data = {
        "table_data": table_data,
        "selected_currency": selected_currency.get()
    }
    os.makedirs(USERDATA_DIR, exist_ok=True)
    with open(USERDATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_userdata():
    if os.path.exists(USERDATA_FILE):
        with open(USERDATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            table_data.clear()
            table_data.extend(data.get("table_data", []))
            if "selected_currency" in data:
                selected_currency.set(data["selected_currency"])
            return True
    return False

# --- Currency formatting and storage ---
currency_formats = {
    "US Dollar": lambda v: f"${v}",
    "Euro":      lambda v: f"{v}€",
    "Pound":     lambda v: f"£{v}",
    "Rupien":    lambda v: f"₹{v}",
    "Yen":       lambda v: f"¥{v}",
    "Schweizer Franken": lambda v: f"{v} CHF"
}
currency_options = list(currency_formats.keys())
table_data = []  # [{'item':..., 'value':...}]



# Set the title of the window
root.title("Spendify")

# Set the size of the window
root.geometry("280x490")

# Create a frame to hold the widgets
frm = ttk.Frame(root, padding=10)
frm.grid(column=0, row=0, sticky=(N, W, E, S))
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
        background="#222222",
        foreground="white",
        fieldbackground="#222222",
        rowheight=25,
        font=("Arial", 10)
    )
    style.configure("Cusotom.TButton",
        background="#444444",
        foreground="white",
        font=("Arial", 10, "bold")   
    )
    style.map("Custom.TButton",
        background=[("active", "#666666")],
        foreground=[("active", "white")]
    )
    style.configure("Treeview.Heading",
        background="#444444",
        foreground="white",
        font=("Arial", 10, "bold")
    )
    style.map("Treeview.Heading",
        background=[("active", "#666666")],
        foreground=[("active", "white")]
    )
    style.map("Treeview", 
        background=[("selected", "#333333")], 
        foreground=[("selected", "#ffffff")]
    )
    style.configure("Treeview", 
        background="#222222", 
        foreground="white", 
        fieldbackground="#222222"
    )
    style.map("Treeview", background=[("selected", "#333333")])
    tree.tag_configure('filled', background="#181818")

    # Beispiel-Daten einfügen mit Tag für belegte Zeilen
    table_data.clear()
    if not load_userdata():
        fmt = currency_formats["US Dollar"]
        tree.insert("", "end", values=("Football", fmt(10)), tags=('filled',))
        tree.insert("", "end", values=("Pair Socks", fmt(5)), tags=('filled',))
    else:
        fmt = currency_formats[selected_currency.get()]
        for entry in table_data:
            tree.insert("", "end", values=(entry['item'], fmt(entry['value'])), tags=('filled',))

    tree.pack(padx=2, pady=2)

def CreateLabel():
    Welcome = "~Welcome to Spendifiy!~"
    label = ttk.Label(frm, text=Welcome, background="black", foreground="white", font=("Arial", 14), anchor="center")
    label.grid(column=0, row=1, columnspan=2, sticky="w", pady=10, ipadx=10, ipady=2)

def update_currency(*args):
    currency = selected_currency.get()
    fmt = currency_formats[currency]
    for i, entry in enumerate(table_data):
        tree.item(tree.get_children()[i], values=(entry['item'], fmt(entry['value'])))
    save_userdata()

def CreateDropdown():
    global selected_currency
    selected_currency = StringVar()
    selected_currency.set(currency_options[0])
    dropdown = ttk.OptionMenu(frm, selected_currency, currency_options[0], *currency_options, command=update_currency)
    dropdown.grid(column=0, row=5, columnspan=2, pady=10, sticky="w")
    dropdown.configure(width=30, style="Custom.TButton")

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
    entry_price = Entry(add_win)
    entry_price.grid(row=1, column=1, padx=10, pady=5)

    def add_to_table():
        item = entry_item.get()
        price = entry_price.get()
        if not item or not price:
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
        try:
            price_int = int(price)
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
        if not item.isalpha():
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
        table_data.append({'item': item, 'value': price_int})
        fmt = currency_formats[selected_currency.get()]
        tree.insert("", "end", values=(item, fmt(price_int)), tags=('filled',))
        save_userdata()
        add_win.destroy()
    add_btn = Button(add_win, text="Add", command=add_to_table, bg="#444444", fg="white")
    add_btn.grid(row=2, column=0, columnspan=2, pady=10)

def delete_selected_item():
    selected = tree.selection()
    if not selected:
        pass
    else:
        idx = tree.index(selected)
        tree.delete(selected)
        if idx < len(table_data):
            del table_data[idx]
        save_userdata()
        print("Deleted Item:", selected)

def edit_selected_item():
    selected = tree.selection()
    if not tree.selection():
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
    else:
        selected = tree.selection()
        values = tree.item(selected, 'values')
        idx = tree.index(selected)
        current_item = values[0]
        # Remove currency symbol for editing
        current_price = values[1]
        # Try to remove any currency symbol or suffix
        for k, v in currency_formats.items():
            fmt_val = v("X").replace("X", "")
            if current_price.startswith(fmt_val):
                current_price = current_price[len(fmt_val):]
            elif current_price.endswith(fmt_val):
                current_price = current_price[:-len(fmt_val)]
        current_price = ''.join(filter(str.isdigit, current_price))

        edit_win = Toplevel(root)
        edit_win.title("Edit Values")
        edit_win.configure(bg="black")
        edit_win.geometry("380x200")
        edit_win.resizable(False, False)

        Label(edit_win, text="Edit Value and Name", bg="black", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=20)
        Label(edit_win, text="Item:", bg="black", fg="white").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        entry_item = Entry(edit_win)
        entry_item.grid(row=1, column=1, padx=10, pady=5)
        entry_item.insert(0, current_item)

        Label(edit_win, text="Price:", bg="black", fg="white").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        entry_price = Entry(edit_win)
        entry_price.grid(row=2, column=1, padx=10, pady=5)
        entry_price.insert(0, current_price)

        def save_edits():
            new_item = entry_item.get()
            new_price = entry_price.get()
            if not new_item or not new_price:
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
            try:
                price_int = int(new_price)
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
            if not new_item.isalpha():
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
            # Update table_data and tree
            table_data[idx] = {'item': new_item, 'value': price_int}
            fmt = currency_formats[selected_currency.get()]
            tree.item(selected, values=(new_item, fmt(price_int)))
            save_userdata()
            edit_win.destroy()

        Button(
            edit_win,
            text="Okay",
            command=save_edits,
            bg="#444444",
            fg="white",
            font=("Arial", 11, "bold"),
            width=12,
            height=2
        ).grid(row=3, column=0, columnspan=2, pady=20)

def CreateButtons():
    global style
    style = ttk.Style()
    style.configure("Custom.TButton",
        background="#444444",
        foreground="white",
        font=("Arial", 11, "bold")
    )
    style.map("Custom.TButton",
        background=[("active", "#666666")],
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
CreateDropdown()
#configure color of the frame
frm.configure(style="Black.TFrame")
style = ttk.Style()
style.configure("Black.TFrame", background="black")

#mainloop (this keeps the window open)
root.mainloop()

#ToDo:logo - currency converter - stück berechnung - monat ausgaben mehr/weniger