# sqrity_login.py

import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib
import os
import sys
import subprocess


# Issam added this
def check_and_install_ctk():
    try:
        import customtkinter
        print("customtkinter is already installed!")
        return True
    except ImportError:
        print("customtkinter not found.")
        # Ask user for confirmation
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        response = messagebox.askyesno(
            "Install Required Package",
            "customtkinter is required but not installed.\n\n"
            "Do you want to install it now?\n\n"
            "This will run: pip install customtkinter"
        )
        root.destroy()

        if response:
            print("Installing customtkinter...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "customtkinter"])
                print("customtkinter installed successfully!")
                return True
            except subprocess.CalledProcessError:
                messagebox.showerror(
                    "Installation Failed",
                    "Failed to install customtkinter.\n\n"
                    "Please install it manually using:\n"
                    "pip install customtkinter"
                )
                return False
        else:
            messagebox.showinfo(
                "Installation Cancelled",
                "customtkinter is required to run this application.\n\n"
                "Please install it manually using:\n"
                "pip install customtkinter"
            )
            return False


import customtkinter as ctk

DB_PATH = "users.db"  # same database file you already use


# ---------- DB HELPERS ----------

def init_db():
    """Create users table if it does not exist."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS users
                (
                    id
                    INTEGER
                    PRIMARY
                    KEY
                    AUTOINCREMENT,
                    username
                    TEXT
                    NOT
                    NULL
                    UNIQUE,
                    salt
                    BLOB
                    NOT
                    NULL,
                    password_hash
                    BLOB
                    NOT
                    NULL
                )
                """
            )
            conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error initializing DB: {e}")


def hash_password(password: str, salt: bytes | None = None):
    """Return (salt, hash) using PBKDF2-HMAC-SHA256."""
    if salt is None:
        salt = os.urandom(16)
    pwd_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        100_000
    )
    return salt, pwd_hash


def register_user(username: str, password: str):
    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password.")
        return

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()

            # Check if username exists
            cur.execute("SELECT id FROM users WHERE username = ?", (username,))
            if cur.fetchone() is not None:
                messagebox.showerror("Error", "Username already taken.")
                return

            salt, pwd_hash = hash_password(password)

            cur.execute(
                "INSERT INTO users (username, salt, password_hash) VALUES (?, ?, ?)",
                (username, salt, pwd_hash),
            )
            conn.commit()

        messagebox.showinfo("Success", "Registration successful! You can now login.")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error during registration: {e}")


def login_user(username: str, password: str, root: tk.Tk):
    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password.")
        return

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT salt, password_hash FROM users WHERE username = ?",
                (username,),
            )
            row = cur.fetchone()

        if row is None:
            messagebox.showerror("Error", "Invalid username or password.")
            return

        db_salt, db_hash = row
        _, entered_hash = hash_password(password, db_salt)

        if entered_hash == db_hash:
            messagebox.showinfo("Login", "Login successful!")
            open_dashboard(username)
            root.destroy()  # close login window
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error during login: {e}")


def open_dashboard(username: str):
    """
    Open Dashboard.py and pass the username as a command-line argument.
    Dashboard.py must read sys.argv[1] to know who is logged in.
    """
    try:
        subprocess.Popen([sys.executable, "Dashboard.py", username])
    except Exception as e:
        messagebox.showerror("Error", f"Could not open dashboard: {e}")


# Added by Issam
def CenterWindowToDisplay(Screen: ctk.CTk, width: int, height: int, scale_factor: float = 1.0):
    """Centers the window to the main display/monitor"""
    screen_width = Screen.winfo_screenwidth()
    screen_height = Screen.winfo_screenheight()
    x = int(((screen_width / 2) - (width / 2)) * scale_factor)
    y = int(((screen_height / 2) - (height / 1.5)) * scale_factor)
    return f"{width}x{height}+{x}+{y}"


def show_loading_screen():
    """Show a loading screen for 5 seconds"""
    loading = ctk.CTk()
    loading.title("SQRITY - Loading")
    loading.geometry("400x200")
    loading.resizable(False, False)

    # Center the loading screen
    loading.update_idletasks()
    loading.eval('tk::PlaceWindow . center')

    # Loading content
    loading_label = ctk.CTkLabel(
        loading,
        text="SQRITY - Password Manager",
        font=("Segoe UI", 20, "bold")
    )
    loading_label.pack(pady=30)

    progress_bar = ctk.CTkProgressBar(loading, width=300, height=20)
    progress_bar.pack(pady=20)
    progress_bar.set(0)

    status_label = ctk.CTkLabel(
        loading,
        text="Initializing secure environment...",
        font=("Segoe UI", 12)
    )
    status_label.pack(pady=10)

    loading.update()

    # Animate progress bar over 5 seconds
    for i in range(101):
        progress_bar.set(i / 100)
        if i < 25:
            status_label.configure(text="Initializing secure environment...")
        elif i < 50:
            status_label.configure(text="Loading encryption modules...")
        elif i < 75:
            status_label.configure(text="Setting up database...")
        else:
            status_label.configure(text="Almost ready...")
        loading.update()
        loading.after(50)  # 50ms * 100 steps = 5 seconds

    loading.destroy()


# ---------- UI ----------

def main():
    check_and_install_ctk()
    # Show loading screen first
    # show_loading_screen()
    init_db()

    # Configure customtkinter theme
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("SQRITY - PM Login")
    root.geometry("450x260")
    root.resizable(False, False)

    # Create all widgets FIRST
    title_label = ctk.CTkLabel(
        root,
        text="Welcome To SQRITY - PM",
        font=("Segoe UI", 25, "bold")
    )
    title_label.pack(pady=(15, 20))

    # Create form frame
    form_frame = ctk.CTkFrame(root, fg_color="transparent")
    form_frame.pack(pady=5)

    # Username section
    username_label = ctk.CTkLabel(
        form_frame,
        text="Username",
        font=("Segoe UI", 20, 'bold'),
        anchor="w"
    )
    username_label.grid(row=0, column=0, sticky="w")

    username_entry = ctk.CTkEntry(
        form_frame,
        font=("Segoe UI", 15),
        width=400,
        height=35
    )
    username_entry.grid(row=1, column=0, pady=(2, 12), sticky="w")

    # Password section
    password_label = ctk.CTkLabel(
        form_frame,
        text="Password",
        font=("Segoe UI", 20, 'bold'),
        anchor="w"
    )
    password_label.grid(row=2, column=0, sticky="w")

    # Password entry - make it shorter
    password_entry = ctk.CTkEntry(
        form_frame,
        font=("Segoe UI", 15),
        width=400,
        height=35,
        show="*"
    )
    password_entry.grid(row=3, column=0, pady=(2, 12), sticky="w")

    def toggle_password():
        if password_entry.cget("show") == "":
            password_entry.configure(show="*")
            show_btn.configure(text="Hide")
            show_btn.configure(text="🙈")
        else:
            password_entry.configure(show="")
            show_btn.configure(text="Show")
            show_btn.configure(text="🙉")

    show_btn = ctk.CTkButton(
        form_frame,
        text="🙈",
        command=toggle_password,
        font=("Segoe UI", 20),
        width=60,
        height=35,
        fg_color="#374151",
        hover_color="#4B5563"
    )
    # Position show button in the SAME ROW but use sticky="n" to align to top
    show_btn.grid(row=3, column=1, padx=(10, 0), pady=(3, 0), sticky="n")

    # Buttons
    buttons_frame = ctk.CTkFrame(root, fg_color="transparent")
    buttons_frame.pack(pady=(10, 5))

    def on_register():
        username = username_entry.get().strip()
        password = password_entry.get()
        register_user(username, password)

    def on_login():
        username = username_entry.get().strip()
        password = password_entry.get()
        login_user(username, password, root)

    register_btn = ctk.CTkButton(
        buttons_frame,
        fg_color="#1f59ab",
        text="Register",
        font=("Segoe UI", 20),
        command=on_register,
        width=100,
        height=40
    )
    register_btn.pack(side="left", padx=15)

    login_btn = ctk.CTkButton(
        buttons_frame,
        fg_color="#1f59ab",
        text="Login",
        font=("Segoe UI", 20),
        command=on_login,
        width=100,
        height=40
    )
    login_btn.pack(side="left", padx=15)

    # CENTER THE WINDOW AFTER ALL WIDGETS ARE CREATED
    root.update_idletasks()

    root.geometry(CenterWindowToDisplay(root, 650, 350, root._get_window_scaling()))

    root.mainloop()


if __name__ == "__main__":
    main()
