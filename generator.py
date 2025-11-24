# generator.py

import tkinter as tk
from tkinter import messagebox
import random
import string
import sqlite3
import sys

# ----------------------
#   STYLE CONSTANTS
# ----------------------
BG_COLOR = "#111827"
FG_COLOR = "#ffffff"
ENTRY_BG = "#1f2933"
BTN_BG = "#2563eb"
BTN_FG = "#ffffff"

VAULT_DB = "vault.db"   # database where passwords will be stored


# ----------------------
#   INIT DATABASE
# ----------------------
def init_vault_db():
    with sqlite3.connect(VAULT_DB) as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS vault (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                owner_username TEXT NOT NULL,
                app_name TEXT NOT NULL,
                password TEXT NOT NULL
            )
        """)
        conn.commit()


# ----------------------
#   PASSWORD GENERATOR
# ----------------------
def generate_password():
    characters = (
        string.ascii_uppercase +
        string.ascii_lowercase +
        string.digits +
        "!@#$%^&*()_+-={}[]|:;<>,.?/"
    )

    # length MUST be >= 12
    length = 14

    password = "".join(random.choice(characters) for _ in range(length))
    entry_password.config(state="normal")
    entry_password.delete(0, tk.END)
    entry_password.insert(0, password)
    entry_password.config(state="readonly")


# ----------------------
#   VIEW GENERATED PASS
# ----------------------
def view_password():
    pwd = entry_password.get().strip()
    if not pwd:
        messagebox.showerror("Error", "No password generated yet.")
        return
    messagebox.showinfo("Generated Password", pwd)


# ----------------------
#   SAVE PASSWORD
# ----------------------
def save_password(username):
    app_name = entry_app.get().strip()
    pwd = entry_password.get().strip()

    if not app_name:
        messagebox.showerror("Error", "Please enter the application name.")
        return
    if not pwd:
        messagebox.showerror("Error", "Generate a password first.")
        return

    try:
        with sqlite3.connect(VAULT_DB) as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO vault (owner_username, app_name, password) VALUES (?, ?, ?)",
                (username, app_name, pwd)
            )
            conn.commit()

        messagebox.showinfo("Success", f"Password saved for {app_name}!")

    except Exception as e:
        messagebox.showerror("Database Error", f"Could not save password:\n\n{e}")


# ----------------------
#            MAIN
# ----------------------
def main():

    # Get username sent from Dashboard
    if len(sys.argv) < 2:
        messagebox.showerror("Error", "No username provided to generator.py")
        return

    username = sys.argv[1]

    init_vault_db()

    root = tk.Tk()
    root.title("SQRITY - Password Generator")
    root.geometry("500x350")
    root.resizable(False, False)
    root.configure(bg=BG_COLOR)

    # Title
    lbl_title = tk.Label(
        root,
        text=f"Password Generator ({username})",
        font=("Segoe UI", 16, "bold"),
        bg=BG_COLOR,
        fg=FG_COLOR
    )
    lbl_title.pack(pady=20)

    # Frame
    frame = tk.Frame(root, bg=BG_COLOR)
    frame.pack(pady=10)

    # Application Name
    lbl_app = tk.Label(
        frame,
        text="Application Name:",
        font=("Segoe UI", 10),
        bg=BG_COLOR,
        fg=FG_COLOR
    )
    lbl_app.grid(row=0, column=0, sticky="w")

    global entry_app
    entry_app = tk.Entry(
        frame,
        font=("Segoe UI", 10),
        bg=ENTRY_BG,
        fg=FG_COLOR,
        insertbackground=FG_COLOR,
        relief="flat",
        width=35
    )
    entry_app.grid(row=1, column=0, pady=(0, 15))

    # Generated password
    lbl_password = tk.Label(
        frame,
        text="Generated Password:",
        font=("Segoe UI", 10),
        bg=BG_COLOR,
        fg=FG_COLOR
    )
    lbl_password.grid(row=2, column=0, sticky="w")

    global entry_password
    entry_password = tk.Entry(
        frame,
        font=("Segoe UI", 10),
        bg=ENTRY_BG,
        fg=FG_COLOR,
        insertbackground=FG_COLOR,
        width=35,
        relief="flat",
        state="readonly"
    )
    entry_password.grid(row=3, column=0, pady=(0, 20))

    # Buttons
    btn_generate = tk.Button(
        root,
        text="Generate Password",
        font=("Segoe UI", 10, "bold"),
        bg=BTN_BG,
        fg=BTN_FG,
        relief="flat",
        width=20,
        command=generate_password
    )
    btn_generate.pack(pady=5)

    btn_view = tk.Button(
        root,
        text="View Password",
        font=("Segoe UI", 10, "bold"),
        bg=BTN_BG,
        fg=BTN_FG,
        relief="flat",
        width=20,
        command=view_password
    )
    btn_view.pack(pady=5)

    btn_store = tk.Button(
        root,
        text="Store Password",
        font=("Segoe UI", 10, "bold"),
        bg=BTN_BG,
        fg=BTN_FG,
        relief="flat",
        width=20,
        command=lambda: save_password(username)
    )
    btn_store.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
