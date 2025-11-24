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
    # Get user preferences from the GUI
    try:
        length = int(entry_length.get())
        if length < 4:
            messagebox.showwarning("Warning",
                                   "Password length must be at least 4 characters. Using default length of 12.")
            length = 12
            entry_length.delete(0, tk.END)
            entry_length.insert(0, "12")
    except ValueError:
        messagebox.showwarning("Warning", "Invalid length entered. Using default length of 12.")
        length = 12
        entry_length.delete(0, tk.END)
        entry_length.insert(0, "12")

    # Get character type preferences from checkboxes
    uppercase = var_uppercase.get()
    lowercase = var_lowercase.get()
    numbers = var_numbers.get()
    symbols = var_symbols.get()

    # Build character set based on user preferences
    characters = ""
    if uppercase:
        characters += string.ascii_uppercase
    if lowercase:
        characters += string.ascii_lowercase
    if numbers:
        characters += string.digits
    if symbols:
        characters += "!@#$%^&*()_+-={}[]|:;<>,.?/"

    # Validate that at least one character type is selected
    if characters == "":
        messagebox.showerror("Error", "Select at least one character type!")
        return

    # Generate password
    password = "".join(random.choice(characters) for _ in range(length))

    # Display password in entry field
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
        btn_toggle_visibility.configure(text="🙈")  # Hide emoji
    else:
        entry_password.configure(show='•')
        btn_toggle_visibility.configure(text="🙉")  # Show emoji


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
def save_password():
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
    global username, entry_app, entry_length, var_uppercase, var_lowercase, var_numbers, var_symbols
    global entry_password, btn_toggle_visibility

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
    root.geometry("650x700")  # Increased height to accommodate new options
    root.resizable(False, False)

    # Main container
    main_frame = ctk.CTkFrame(root, fg_color="#2b2b2b", corner_radius=10)
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
    frame.grid_columnconfigure(0, weight=1)
    # Application Name
    lbl_app = ctk.CTkLabel(
        frame,
        text="Application Name:",
        font=("Segoe UI", 16),
        anchor="w"
    )
    lbl_app.grid(row=0, column=0, sticky="w", pady=(0, 5))

    entry_app = ctk.CTkEntry(
        frame,
        fg_color="#404040",
        font=("Segoe UI", 16),
        width=400,
        height=35,
        placeholder_text="Enter application/service name"
    )
    entry_app.grid(row=1, column=0, pady=(0, 20), sticky="ew")

    # Password Options Frame
    options_frame = ctk.CTkFrame(frame, fg_color="transparent")
    options_frame.grid(row=2, column=0, pady=(0, 20), sticky="ew")

    # Password Length
    lbl_length = ctk.CTkLabel(
        options_frame,
        text="Password Length:",
        font=("Segoe UI", 14),
        anchor="w"
    )
    lbl_length.grid(row=0, column=0, sticky="w", pady=(0, 5))

    entry_length = ctk.CTkEntry(
        options_frame,
        fg_color="#404040",
        font=("Segoe UI", 14),
        width=80,
        height=30,
        placeholder_text="12"
    )
    entry_length.insert(0, "14")  # Default length
    entry_length.grid(row=0, column=1, sticky="w", pady=(0, 5))

    # Character Type Options
    lbl_options = ctk.CTkLabel(
        options_frame,
        text="Character Types:",
        font=("Segoe UI", 14),
        anchor="w"
    )
    lbl_options.grid(row=1, column=0, sticky="w", pady=(10, 5))

    # Checkboxes frame
    checkboxes_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
    checkboxes_frame.grid(row=2, column=0, columnspan=2, sticky="w", pady=(0, 10))

    var_uppercase = ctk.BooleanVar(value=True)
    var_lowercase = ctk.BooleanVar(value=True)
    var_numbers = ctk.BooleanVar(value=True)
    var_symbols = ctk.BooleanVar(value=True)

    chk_uppercase = ctk.CTkCheckBox(
        checkboxes_frame,
        fg_color="#1f59ab",
        text="Uppercase Letters (A-Z)",
        variable=var_uppercase,
        font=("Segoe UI", 12)
    )
    chk_uppercase.grid(row=0, column=0, sticky="w", padx=(0, 20))

    chk_lowercase = ctk.CTkCheckBox(
        checkboxes_frame,
        fg_color="#1f59ab",
        text="Lowercase Letters (a-z)",
        variable=var_lowercase,
        font=("Segoe UI", 12)
    )
    chk_lowercase.grid(row=0, column=1, sticky="w")

    chk_numbers = ctk.CTkCheckBox(
        checkboxes_frame,
        fg_color="#1f59ab",
        text="Numbers (0-9)",
        variable=var_numbers,
        font=("Segoe UI", 12)
    )
    chk_numbers.grid(row=1, column=0, sticky="w", padx=(0, 20), pady=(10, 0))

    chk_symbols = ctk.CTkCheckBox(
        checkboxes_frame,
        fg_color="#1f59ab",
        text="Symbols (!@#$%...)",
        variable=var_symbols,
        font=("Segoe UI", 12)
    )
    chk_symbols.grid(row=1, column=1, sticky="w", pady=(10, 0))

    # Generated password
    lbl_password = ctk.CTkLabel(
        frame,
        text="Password:",
        font=("Segoe UI", 16),
        anchor="w"
    )
    lbl_password.grid(row=3, column=0, sticky="w", pady=(0, 5))

    # Password entry frame (for entry + action buttons)
    password_frame = ctk.CTkFrame(frame, fg_color="transparent")
    password_frame.grid(row=4, column=0, pady=(0, 10), sticky="ew")

    entry_password = ctk.CTkEntry(
        password_frame,
        fg_color="#404040",
        font=("Segoe UI", 16),
        width=400,
        height=35,
        show="•",  # Hide password by default with bullet points
        placeholder_text="Generate or type your password"
    )
    entry_password.pack(side="left", fill="x", expand=True)

    # Single toggle button (replaces both show and clear buttons)
    btn_toggle_visibility = ctk.CTkButton(
        password_frame,
        text="🙉",  # Default show emoji
        font=("Segoe UI", 20),
        width=60,
        height=35,
        fg_color="#374151",
        hover_color="#4B5563",
        command=toggle_password_visibility
    )
    btn_toggle_visibility.pack(side="right", padx=(5, 0))

    # Password info label
    lbl_password_info = ctk.CTkLabel(
        frame,
        text="✓ You can edit the generated password or type your own",
        font=("Segoe UI", 12),
        text_color="#ffffff",
        anchor="w"
    )
    lbl_password_info.grid(row=5, column=0, sticky="w", pady=(0, 20))

    # Buttons frame
    buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    buttons_frame.pack(pady=20)

    # Buttons
    btn_generate = ctk.CTkButton(
        buttons_frame,
        fg_color="#1f59ab",
        text="Generate Custom Password",
        font=("Segoe UI", 16, "bold"),
        width=220,
        height=40,
        command=generate_password
    )
    btn_generate.pack(pady=8)

    btn_view = ctk.CTkButton(
        buttons_frame,
        fg_color="#1f59ab",
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
        command=save_password
    )
    btn_store.pack(pady=8)

    # Center the window
    root.update_idletasks()
    root.geometry('650x680')

    root.mainloop()


if __name__ == "__main__":
    main()
