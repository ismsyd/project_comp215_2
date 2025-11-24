# Dashboard.py

import tkinter as tk
from tkinter import messagebox
import subprocess
import sys

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

# ---------- UI Setup (same style as login) ----------
root = tk.Tk()
root.title("SQRITY - PM Dashboard")
root.geometry("450x300")
root.resizable(False, False)

# Colors & fonts – matching login style
BG_COLOR = "#111111"
CARD_COLOR = "#1f2933"
BTN_COLOR = "#2563eb"
BTN_HOVER = "#1d4ed8"
TEXT_COLOR = "#f9fafb"
ENTRY_BG = "#111827"

root.configure(bg=BG_COLOR)

# Center frame like login card
card = tk.Frame(root, bg=CARD_COLOR, bd=0, highlightthickness=0)
card.place(relx=0.5, rely=0.5, anchor="center", width=420, height=260)

# Title
title_label = tk.Label(
    card,
    text="SQRITY - PM Dashboard",
    fg=TEXT_COLOR,
    bg=CARD_COLOR,
    font=("Segoe UI Semibold", 16)
)
title_label.pack(pady=(15, 5))

# Logged-in username
user_label = tk.Label(
    card,
    text=f"Welcome, {current_user}",
    fg="#d1d5db",
    bg=CARD_COLOR,
    font=("Segoe UI", 11)
)
user_label.pack(pady=(0, 20))

# Buttons container
buttons_frame = tk.Frame(card, bg=CARD_COLOR)
buttons_frame.pack(pady=(0, 10))

def style_button(btn: tk.Button):
    btn.configure(
        bg=BTN_COLOR,
        fg="white",
        activebackground=BTN_HOVER,
        activeforeground="white",
        relief="flat",
        bd=0,
        font=("Segoe UI Semibold", 10),
        padx=20,
        pady=6,
        cursor="hand2"
    )

# Password Generator button
generator_btn = tk.Button(
    buttons_frame,
    text="Password Generator",
    command=open_generator
)
style_button(generator_btn)
generator_btn.grid(row=0, column=0, padx=15, pady=10)

# View Vault button
view_btn = tk.Button(
    buttons_frame,
    text="Open Vault",
    command=open_view
)
style_button(view_btn)
view_btn.grid(row=0, column=1, padx=15, pady=10)

# Footer text (optional small hint)
footer = tk.Label(
    card,
    text="Manage your passwords securely.",
    fg="#9ca3af",
    bg=CARD_COLOR,
    font=("Segoe UI", 9)
)
footer.pack(side="bottom", pady=(0, 10))

root.mainloop()
