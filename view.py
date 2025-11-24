# view.py
import sys
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# ---------- Get username from command-line ----------
if len(sys.argv) < 2:
    messagebox.showerror("Error", "No username provided to view.py")
    sys.exit(1)

current_user = sys.argv[1]

# ---------- Database helper ----------
def fetch_passwords_for_user(username):
    # 🔴 IMPORTANT: Here we use vault.db instead of users.db
    conn = sqlite3.connect("vault.db")
    cur = conn.cursor()

    # Adjust table / column names to match your vault.db schema
    # Example schema: vault(owner_username TEXT, app_name TEXT, password TEXT)
    cur.execute("""
        SELECT app_name, password
        FROM vault
        WHERE owner_username = ?
    """, (username,))

    rows = cur.fetchall()
    conn.close()
    return rows

# ---------- GUI ----------
root = tk.Tk()
root.title("SQRITY - Password Vault")

# Same style as login page (dark background, accent buttons, etc.)
root.configure(bg="#121212")
root.geometry("600x400")
root.resizable(False, False)

title_label = tk.Label(
    root,
    text=f"Stored Passwords for {current_user}",
    font=("Segoe UI", 18, "bold"),
    bg="#121212",
    fg="#00FFF0"
)
title_label.pack(pady=20)

frame = tk.Frame(root, bg="#1E1E1E")
frame.pack(padx=20, pady=10, fill="both", expand=True)

columns = ("app", "password")
tree = ttk.Treeview(frame, columns=columns, show="headings", height=10)
tree.heading("app", text="Application")
tree.heading("password", text="Password")

tree.column("app", width=200, anchor="center")
tree.column("password", width=300, anchor="center")

# Scrollbar
vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=vsb.set)

tree.grid(row=0, column=0, sticky="nsew")
vsb.grid(row=0, column=1, sticky="ns")

frame.grid_columnconfigure(0, weight=1)
frame.grid_rowconfigure(0, weight=1)

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

# Close button
close_btn = tk.Button(
    root,
    text="Close",
    font=("Segoe UI", 11, "bold"),
    bg="#00FFF0",
    fg="#000000",
    activebackground="#00D4C7",
    activeforeground="#000000",
    relief="flat",
    padx=20,
    pady=5,
    command=root.destroy
)
close_btn.pack(pady=10)

root.mainloop()
