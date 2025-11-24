# Dashboard.py

import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import customtkinter as ctk


# ---------- Logout and reopen Login window ----------
def logout(window):
    """Logout and return to login window."""
    messagebox.showinfo("Logout", "You have been logged out.")
    window.destroy()
    subprocess.Popen([sys.executable, "login.py"], shell=True)


# ---------- Get Logged-in Username ----------
if len(sys.argv) < 2:
    # If someone runs this file directly without going through login.py
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Error", "No username provided to Dashboard.\nOpen this window from the login page.")
    sys.exit(1)

current_user = sys.argv[1]


# ---------- Call Other Windows ----------
def open_generator():
    """Open generator.py and pass the current username."""
    try:
        subprocess.Popen([sys.executable, "generator.py", current_user])
    except Exception as e:
        messagebox.showerror("Error", f"Could not open password generator.\n\n{e}")


def open_view():
    """Open view.py and pass the current username."""
    try:
        subprocess.Popen([sys.executable, "view.py", current_user])
    except Exception as e:
        messagebox.showerror("Error", f"Could not open vault viewer.\n\n{e}")


def CenterWindowToDisplay(Screen: ctk.CTk, width: int, height: int, scale_factor: float = 1.0):
    """Centers the window to the main display/monitor"""
    screen_width = Screen.winfo_screenwidth()
    screen_height = Screen.winfo_screenheight()
    x = int(((screen_width / 2) - (width / 2)) * scale_factor)
    y = int(((screen_height / 2) - (height / 2)) * scale_factor)
    return f"{width}x{height}+{x}+{y}"


# ---------- UI Setup with customtkinter ----------
# ---------- UI Setup with customtkinter ----------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("SQRITY - PM Dashboard")
root.geometry("650x350")
root.resizable(False, False)

# Main container frame
main_frame = ctk.CTkFrame(
    root,
    fg_color="#1f2933",
    corner_radius=10
)
main_frame.pack(expand=True, fill="both")

# Center container for all content
center_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
center_frame.place(relx=0.5, rely=0.5, anchor="center")

# Title
title_label = ctk.CTkLabel(
    center_frame,
    text="SQRITY - PM Dashboard",
    text_color="#f9fafb",
    font=("Segoe UI", 20, "bold")
)
title_label.pack(pady=(0, 10))

# Logged-in username
user_label = ctk.CTkLabel(
    center_frame,
    text=f"Welcome, {current_user}",
    text_color="#d1d5db",
    font=("Segoe UI", 18)
)
user_label.pack(pady=(0, 30))

# Buttons container
buttons_frame = ctk.CTkFrame(center_frame, fg_color="transparent")
buttons_frame.pack(pady=(0, 30))
btn_frm = tk.Frame(center_frame, bg="#1f2933")
btn_frm.pack(pady=(5, 10))

# Password Generator button
generator_btn = ctk.CTkButton(
    buttons_frame,
    text="Password Generator",
    command=open_generator,
    width=200,
    height=80,
    font=("Segoe UI", 18, "bold"),
    hover_color="#1d4ed8"
)
generator_btn.pack(side="left", padx=15)

# View Vault button
view_btn = ctk.CTkButton(
    buttons_frame,
    text="Open Vault",
    command=open_view,
    width=200,
    height=80,
    font=("Segoe UI", 18, "bold"),
    hover_color="#1d4ed8"
)
view_btn.pack(side="left", padx=15)

logout_btn = ctk.CTkButton(
    btn_frm,
    text="Logout",
    command=lambda: logout(root),
    width=120,
    height=40,
    fg_color="#b91c1c",
    hover_color="#991b1b",
    font=("Segoe UI", 14, "bold")
)
logout_btn.grid(row=0, column=1, padx=15, pady=10)


# Footer text
footer = ctk.CTkLabel(
    center_frame,
    text="Manage your passwords securely.",
    text_color="#9ca3af",
    font=("Segoe UI", 16)
)
footer.pack(pady=20)

# CENTER THE WINDOW
root.update_idletasks()
root.geometry(CenterWindowToDisplay(root, 650, 350, root._get_window_scaling()))

root.mainloop()
