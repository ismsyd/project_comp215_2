# view.py
import sys
import sqlite3
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import customtkinter as ctk

def CenterWindowToDisplay(Screen: ctk.CTk, width: int, height: int, scale_factor: float = 1.0):
    """Centers the window to the main display/monitor"""
    screen_width = Screen.winfo_screenwidth()
    screen_height = Screen.winfo_screenheight()
    x = int(((screen_width/2) - (width/2)) * scale_factor)
    y = int(((screen_height/2) - (height/1.5)) * scale_factor)
    return f"{width}x{height}+{x}+{y}"




# ---------- Get username from command-line ----------
if len(sys.argv) < 2:
    messagebox.showerror("Error", "No username provided to view.py")
    sys.exit(1)

current_user = sys.argv[1]

# ---------- Database helper ----------
def fetch_passwords_for_user(username):
    conn = sqlite3.connect("vault.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT app_name, password
        FROM vault
        WHERE owner_username = ?
    """, (username,))

    rows = cur.fetchall()
    conn.close()
    return rows

# ---------- GUI with customtkinter ----------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("SQRITY - Password Vault")
root.geometry("650x400")
root.resizable(False, False)

# Main container
main_frame = ctk.CTkFrame(root, fg_color="#2b2b2b", corner_radius=10)
main_frame.pack(expand=True, fill="both")

# Title
title_label = ctk.CTkLabel(
    main_frame,
    text=f"Stored Passwords for {current_user}",
    font=("Segoe UI", 20, "bold"),
    text_color="#ffffff"
)
title_label.pack(pady=20)

# Treeview frame
tree_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
tree_frame.pack(expand=True, fill="both", padx=20, pady=10)

# Create treeview using tkinter (ctk doesn't have native treeview)
columns = ("app", "password")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12)
tree.heading("app", text="Application")
tree.heading("password", text="Password")

tree.column("app", width=250, anchor="center")
tree.column("password", width=350, anchor="center")

# Style the treeview to match dark theme
style = ttk.Style()
style.theme_use("default")
style.configure("Treeview",
                background="#454545",
                foreground="white",
                fieldbackground="#454545",
                borderwidth=0,
                font=("Segoe UI", 16),
                rowheight=45)
style.configure("Treeview.Heading",
                background="#1b1b1b",
                foreground="#ffffff",
                relief="flat",
                font=("Segoe UI", 16,'bold'))
style.map("Treeview", background=[('selected', '#2563eb')])

# Scrollbar
vsb = ctk.CTkScrollbar(tree_frame, orientation="vertical", command=tree.yview)
tree.configure(yscrollcommand=vsb.set)

# Pack treeview and scrollbar
tree.pack(side="left", fill="both", expand=True)
vsb.pack(side="right", fill="y")

# Load data
try:
    data = fetch_passwords_for_user(current_user)
    if not data:
        messagebox.showinfo("Info", "No passwords stored yet for this user.")
    else:
        for app, pwd in data:
            tree.insert("", "end", values=(app, pwd))
except Exception as e:
    messagebox.showerror("Database Error", str(e))


# ---------- Copy password from selection ----------
def copy_selected_password(event=None):
    selected = tree.focus()  # get selected row ID
    if not selected:
        return

    values = tree.item(selected, "values")  # (app_name, password)
    if not values or len(values) < 2:
        return

    password = values[1]

    # Copy to clipboard
    root.clipboard_clear()
    root.clipboard_append(password)
    root.update()

    messagebox.showinfo("Copied", "Password copied to clipboard!")
tree.bind("<Double-1>", copy_selected_password)




# Center the window
root.update_idletasks()

root.geometry(CenterWindowToDisplay(root, 650, 400, root._get_window_scaling()))



root.mainloop()
