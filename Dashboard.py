# Dashboard.py

import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import customtkinter as ctk

# ---------- Get Logged-in Username ----------
if len(sys.argv) < 2:
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Error", "No username provided to Dashboard.\nOpen this window from the login page.")
    sys.exit(1)

current_user = sys.argv[1]

# ---------- Call Other Windows ----------
def open_generator():
    try:
        subprocess.Popen([sys.executable, "generator.py", current_user])
    except Exception as e:
        messagebox.showerror("Error", f"Could not open password generator.\n\n{e}")

def open_view():
    try:
        subprocess.Popen([sys.executable, "view.py", current_user])
    except Exception as e:
        messagebox.showerror("Error", f"Could not open vault viewer.\n\n{e}")

# ---------- LOGOUT FUNCTION (FULLY FIXED) ----------
def logout():
    try:
        subprocess.Popen([sys.executable, "sqrity_login.py"])
    except Exception as e:
        messagebox.showerror("Error", f"Could not return to login page.\n\n{e}")
        return

    root.destroy()   # close dashboard ONLY, not the app

# ---------- Center Window ----------
def CenterWindowToDisplay(Screen: ctk.CTk, width: int, height: int, scale_factor: float = 1.0):
    screen_width = Screen.winfo_screenwidth()
    screen_height = Screen.winfo_screenheight()
    x = int(((screen_width / 2) - (width / 2)) * scale_factor)
    y = int(((screen_height / 2) - (height / 2)) * scale_factor)
    return f"{width}x{height}+{x}+{y}"

# ---------- UI Setup ----------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("SQRITY - PM Dashboard")
root.geometry("650x350")
root.resizable(False, False)

main_frame = ctk.CTkFrame(root, fg_color="#1f2933", corner_radius=10)
main_frame.pack(expand=True, fill="both")

center_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
center_frame.place(relx=0.5, rely=0.5, anchor="center")

title_label = ctk.CTkLabel(
    center_frame,
    text="SQRITY - PM Dashboard",
    text_color="#f9fafb",
    font=("Segoe UI", 20, "bold")
)
title_label.pack(pady=(0, 10))

user_label = ctk.CTkLabel(
    center_frame,
    text=f"Welcome, {current_user}",
    text_color="#d1d5db",
    font=("Segoe UI", 18)
)
user_label.pack(pady=(0, 30))

buttons_frame = ctk.CTkFrame(center_frame, fg_color="transparent")
buttons_frame.pack(pady=(0, 30))

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

# ---------- LOGOUT BUTTON (NEW) ----------
logout_btn = ctk.CTkButton(
    center_frame,
    text="Logout",
    command=logout,
    width=150,
    height=45,
    fg_color="#ef4444",
    hover_color="#b91c1c",
    font=("Segoe UI", 16, "bold")
)
logout_btn.pack(pady=10)

footer = ctk.CTkLabel(
    center_frame,
    text="Manage your passwords securely.",
    text_color="#9ca3af",
    font=("Segoe UI", 16)
)
footer.pack(pady=20)

root.update_idletasks()
root.geometry(CenterWindowToDisplay(root, 650, 350, root._get_window_scaling()))

root.mainloop()
