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
    # Allow editing and hide the password by default
    entry_password.configure(show="•", state="normal")
    # Store the actual password for viewing later
    entry_password.actual_password = password


# ----------------------
#   VIEW GENERATED PASS
# ----------------------
def view_password():
    current_password = entry_password.get()
    if current_password:
        messagebox.showinfo("Current Password", current_password)
    else:
        messagebox.showerror("Error", "No password entered.")


# ----------------------
#   TOGGLE PASSWORD VISIBILITY
# ----------------------
def toggle_password_visibility():
    if entry_password.cget('show') == '•':
        entry_password.configure(show='')
        btn_toggle_visibility.configure(text="Hide Password")
    else:
        entry_password.configure(show='•')
        btn_toggle_visibility.configure(text="Show Password")


# ----------------------
#   CLEAR PASSWORD FIELD
# ----------------------
def clear_password():
    entry_password.configure(state="normal")
    entry_password.delete(0, tk.END)
    entry_password.configure(show="•", state="normal")
    if hasattr(entry_password, 'actual_password'):
        delattr(entry_password, 'actual_password')


# ----------------------
#   SAVE PASSWORD
# ----------------------
def save_password(username):
    app_name = entry_app.get().strip()
    pwd = entry_password.get()

    if not app_name:
        messagebox.showerror("Error", "Please enter the application name.")
        return

    if not pwd:
        messagebox.showerror("Error", "Please enter or generate a password.")
        return

    # Optional: Add password strength validation
    if len(pwd) < 8:
        response = messagebox.askyesno(
            "Weak Password",
            "The password is less than 8 characters. This may be insecure.\n\nDo you want to save it anyway?"
        )
        if not response:
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

        # Clear fields after successful save
        entry_app.delete(0, tk.END)
        clear_password()

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
    root.geometry("650x600")  # Increased height to accommodate new buttons
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
    frame.pack(pady=10, padx=20, fill="both", expand=True)

    # Application Name
    lbl_app = ctk.CTkLabel(
        frame,
        text="Application Name:",
        font=("Segoe UI", 16),
        anchor="w"
    )
    lbl_app.grid(row=0, column=0, sticky="w", pady=(0, 5))

    global entry_app
    entry_app = ctk.CTkEntry(
        frame,
        font=("Segoe UI", 16),
        width=400,
        height=35,
        placeholder_text="Enter application/service name"
    )
    entry_app.grid(row=1, column=0, pady=(0, 20), sticky="ew")

    # Generated password
    lbl_password = ctk.CTkLabel(
        frame,
        text="Password:",
        font=("Segoe UI", 16),
        anchor="w"
    )
    lbl_password.grid(row=2, column=0, sticky="w", pady=(0, 5))

    # Password entry frame (for entry + action buttons)
    password_frame = ctk.CTkFrame(frame, fg_color="transparent")
    password_frame.grid(row=3, column=0, pady=(0, 10), sticky="ew")

    global entry_password
    entry_password = ctk.CTkEntry(
        password_frame,
        font=("Segoe UI", 16),
        width=400,
        height=35,
        show="•",  # Hide password by default with bullet points
        placeholder_text="Generate or type your password"
    )
    entry_password.pack(side="left", fill="x", expand=True)

    # Password action buttons frame (right side)
    password_actions_frame = ctk.CTkFrame(password_frame, fg_color="transparent")
    password_actions_frame.pack(side="right", padx=(5, 0))

    global btn_toggle_visibility
    btn_toggle_visibility = ctk.CTkButton(
        password_actions_frame,
        text="Show",
        font=("Segoe UI", 12),
        width=60,
        height=30,
        command=toggle_password_visibility
    )
    btn_toggle_visibility.pack(side="top", pady=(0, 2))

    btn_clear = ctk.CTkButton(
        password_actions_frame,
        text="Clear",
        font=("Segoe UI", 12),
        width=60,
        height=30,
        command=clear_password
    )
    btn_clear.pack(side="top", pady=(2, 0))

    # Password info label
    lbl_password_info = ctk.CTkLabel(
        frame,
        text="✓ You can edit the generated password or type your own",
        font=("Segoe UI", 12),
        text_color="lightblue",
        anchor="w"
    )
    lbl_password_info.grid(row=4, column=0, sticky="w", pady=(0, 20))

    # Buttons frame
    buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    buttons_frame.pack(pady=20)

    # Buttons
    btn_generate = ctk.CTkButton(
        buttons_frame,
        text="Generate Strong Password",
        font=("Segoe UI", 16, "bold"),
        width=220,
        height=40,
        command=generate_password
    )
    btn_generate.pack(pady=8)

    btn_view = ctk.CTkButton(
        buttons_frame,
        text="View Password",
        font=("Segoe UI", 16, "bold"),
        width=220,
        height=40,
        command=view_password
    )
    btn_view.pack(pady=8)

    btn_store = ctk.CTkButton(
        buttons_frame,
        text="Store Password",
        font=("Segoe UI", 16, "bold"),
        width=220,
        height=40,
        fg_color="#28a745",
        hover_color="#218838",
        command=lambda: save_password(username)
    )
    btn_store.pack(pady=8)

    # Center the window
    root.update_idletasks()
    root.geometry(CenterWindowToDisplay(root, 650, 600, root._get_window_scaling()))

    root.mainloop()


if __name__ == "__main__":
    main()
