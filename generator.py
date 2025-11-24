# generator.py

import tkinter as tk
from tkinter import messagebox
import random
import string
import sqlite3
import sys
import customtkinter as ctk


def CenterWindowToDisplay(Screen: ctk.CTk, width: int, height: int, scale_factor: float = 1.0):
    """Centers the window to the main display/monitor"""
    screen_width = Screen.winfo_screenwidth()
    screen_height = Screen.winfo_screenheight()
    x = int(((screen_width / 2) - (width / 2)) * scale_factor)
    y = int(((screen_height / 2) - (height / 1.5)) * scale_factor)
    return f"{width}x{height}+{x}+{y}"


# ----------------------
#   INIT DATABASE
# ----------------------
def init_vault_db():
    with sqlite3.connect("vault.db") as conn:
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
    entry_password.configure(state="normal")
    entry_password.delete(0, tk.END)
    entry_password.insert(0, password)
    # Hide the password by default
    entry_password.configure(show="•", state="readonly")
    # Store the actual password for viewing later
    entry_password.actual_password = password


# ----------------------
#   VIEW GENERATED PASS
# ----------------------
def view_password():
    if hasattr(entry_password, 'actual_password'):
        pwd = entry_password.actual_password
        messagebox.showinfo("Generated Password", pwd)
    else:
        messagebox.showerror("Error", "No password generated yet.")


# ----------------------
#   SAVE PASSWORD
# ----------------------
def save_password(username):
    app_name = entry_app.get().strip()

    if not hasattr(entry_password, 'actual_password'):
        messagebox.showerror("Error", "Generate a password first.")
        return

    pwd = entry_password.actual_password

    if not app_name:
        messagebox.showerror("Error", "Please enter the application name.")
        return

    try:
        with sqlite3.connect("vault.db") as conn:
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

    # Configure customtkinter
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("SQRITY - Password Generator")
    root.geometry("600x450")
    root.resizable(False, False)

    # Main container
    main_frame = ctk.CTkFrame(root, fg_color="#1f2933", corner_radius=10)
    main_frame.pack(expand=True, fill="both")

    # Title
    lbl_title = ctk.CTkLabel(
        main_frame,
        text=f"Password Generator ({username})",
        font=("Segoe UI", 22, "bold"),
        text_color="#ffffff"
    )
    lbl_title.pack(pady=20)

    # Form frame
    frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    frame.pack(pady=10)

    # Application Name
    lbl_app = ctk.CTkLabel(
        frame,
        text="Application Name:",
        font=("Segoe UI", 16),
        anchor="w"
    )
    lbl_app.grid(row=0, column=0, sticky="w")

    global entry_app
    entry_app = ctk.CTkEntry(
        frame,
        font=("Segoe UI", 16),
        width=300,
        height=35
    )
    entry_app.grid(row=1, column=0, pady=(0, 20))

    # Generated password
    lbl_password = ctk.CTkLabel(
        frame,
        text="Generated Password:",
        font=("Segoe UI", 16),
        anchor="w"
    )
    lbl_password.grid(row=2, column=0, sticky="w")

    # Password entry frame (for entry + show button)
    password_frame = ctk.CTkFrame(frame, fg_color="transparent")
    password_frame.grid(row=3, column=0, pady=(0, 20), sticky="ew")

    global entry_password
    entry_password = ctk.CTkEntry(
        password_frame,
        font=("Segoe UI", 16),
        width=300,
        height=35,
        state="readonly",
        show=""  # Hide password by default with bullet points
    )
    entry_password.pack(side="left")
    entry_password.configure(state='readonly')
    # Buttons frame
    buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    buttons_frame.pack(pady=10)

    # Buttons
    btn_generate = ctk.CTkButton(
        buttons_frame,
        text="Generate Password",
        font=("Segoe UI", 16, "bold"),
        width=180,
        height=35,
        command=generate_password
    )
    btn_generate.pack(pady=5)

    btn_view = ctk.CTkButton(
        buttons_frame,
        text="View Password",
        font=("Segoe UI", 16, "bold"),
        width=180,
        height=35,
        command=view_password
    )
    btn_view.pack(pady=5)

    btn_store = ctk.CTkButton(
        buttons_frame,
        text="Store Password",
        font=("Segoe UI", 16, "bold"),
        width=180,
        height=35,
        command=lambda: save_password(username)
    )
    btn_store.pack(pady=10)

    # Center the window
    root.update_idletasks()
    root.geometry(CenterWindowToDisplay(root, 650, 450, root._get_window_scaling()))

    root.mainloop()


if __name__ == "__main__":
    main()
