# Library imports
import sqlite3
import os
import tkinter as tk
import time
from tkinter import ttk
from typing import List

from colorama import Style

button_list = []
adding_hotkeys = False
application_ids = []
z2 = []
# Database creation
connection1 = sqlite3.connect("user_data.db")
cursor1 = connection1.cursor()

# navigates to desktop directory at program start and creates a list of applications
os.chdir(r"C:\Users\CJcab\OneDrive\Desktop")
applications = os.listdir()

# Creates and edits windows
# Root Window creation
root = tk.Tk()
main_column_number = 10
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = screen_width
window_height = screen_height
screen_centerX = int(screen_width / 2 - window_width / 2)
screen_centerY = int(screen_height / 2 - window_height / 2)
root.geometry(
    f"{window_width}x{window_height}+{screen_centerX}+{screen_centerY}")
root.state("zoomed")
root.configure(bg="black")
root.title("My Hotkeys")
x5 = 0
for num in range(main_column_number):
    root.columnconfigure(x5, weight=0)
    x5 += 1

# ttk style
style = ttk.Style(root)
style.theme_names()
style.theme_use("alt")





#Command performed when "+" button is clicked
k = 0
def add_hotkey():
    global k
    global x3
    global adding_hotkeys
    global button_list
    adding_hotkeys = not adding_hotkeys
    if adding_hotkeys == False:
        hotkey_name = T.get("1.0","end")
        create_shortcut(button_list, hotkey_name)
        T.delete("1.0","end")
        add_hotkey_button.config(text="+")
        T.grid_forget()
        button_list[k].append(hotkey_name)
        k += 1
    else:
        button_list.append([])
        add_hotkey_button.config(text="Add Hotkey")
        T.grid(column=column_pos+2, row=1)

        
    


# Command performed when shortcut is clicked

def button_clicked(button_name):
    global k
    global column_pos
    print(button_name)
    if adding_hotkeys == False:
        if isinstance(button_name, list):
            for file in button_name:
                if isinstance(file, list):
                    for file2 in file:
                        if isinstance(file, str):
                            print("0")
                        else:
                            os.startfile(applications[file2])
                else:
                    if isinstance(file, str):
                        print("0")
                    else:
                        os.startfile(applications[file])
        else:
            for file in button_name:
                os.startfile(file)
    else:
        if isinstance(button_name, list):
            for file in button_name:
                button_list[k].append(applications.index(applications[file]))
        else:
            button_list[k].append(applications.index(button_name))


# Creates the default set of hotkeys for all the applications shown upon the desktop
x2 = 0
x3 = 0
column_pos = 0
button = []
frame = []
for item in applications:
    if x3 >= 8:
        column_pos += 1
        x3 = 0
    button.append(
        tk.Button(
            root,
            borderwidth="2",
            relief="ridge",
            text=applications[x2],
            font=("Arial", 10),
            bg="green",
            fg="yellow",
            width=20,
            height=1,
            anchor="w",
            command=lambda i=item: button_clicked(i),
        ).grid(column=column_pos, row=x3, padx=2, pady=1)
    )
    x2 += 1
    x3 += 1



column_pos2 = -1
def create_shortcut(applications_ids, name):
    global column_pos2
    column_pos2 += 1
    button.append(
        tk.Button(
            root,
            borderwidth="2",
            relief="ridge",
            text=name,
            font=("Arial", 10),
            bg="red",
            fg="yellow",
            width=20,
            height=1,
            anchor="w",
            command=lambda: button_clicked(applications_ids),
        ).grid(column=column_pos2, row=9, padx=2, pady=1)
    )

# Creates the "add hotkey" button
add_hotkey_button = tk.Button(
    root, text="+", font=("Arial", 10), bg="green", width=20, command=lambda: add_hotkey()
)
add_hotkey_button.grid(column=column_pos+2, row=0)

T = tk.Text(root, bg = "green", font=("Arial", 10), width = 10, height = 1)

try:
    query_result = cursor1.execute('SELECT hotkey_data FROM hotkeys')
    for z1 in query_result.fetchall():
        z2.append(str(z1))
    z3 = "".join(z2)
    z3 = z3.replace(" ", "")
    z3 = z3.replace("[", "")
    z3 = z3.replace("]", "")
    z3 = z3.replace("(", "")
    z3 = z3.replace(")", "")
    z3 = z3.replace("'", "")
    z3 = z3.replace('"', '')
    z3 = z3.replace("\\n", "")
    z3 = z3.replace("\\", "")
    z3 = z3.split(",")
    z3.pop()
    print(z3)
    for z4 in z3:
        if z4.isnumeric():
            application_ids.append(int(z4))
        else:
            name = z4
            create_shortcut(application_ids, name)
            application_ids = []

except:
    cursor1.execute('''CREATE TABLE hotkeys
                                    (hotkey_data TEXT)''')

def root_close():
    global hotkey_data
    for z in button_list:
        z = " ".join(str(z))
        cursor1.execute('INSERT INTO hotkeys VALUES (?)', (z,))
    connection1.commit()
    connection1.close()
    print("eh")
    root.destroy()


root.protocol("WM_DELETE_WINDOW", root_close)
root.mainloop()
print(button_list)
