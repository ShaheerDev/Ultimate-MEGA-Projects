from tkinter import *
from tkinter import filedialog
import time

COLOR = "#cbd5e1"
FONT = "Courier New"
FONT_SIZE = 14
FONT_COLOR = "#334155"

window = Tk()
window.title("Ghost Writer")
window.geometry("900x600")
window.config(bg=COLOR)

title_label = Label(text="Ghost Writer", font=(FONT, 60, "bold"), fg=FONT_COLOR, bg=COLOR, highlightthickness=0)
title_label.pack()
text_box = Text(
    window,
    height=10,
    width=50,
    font=(FONT, FONT_SIZE),
    bg="white",
    fg="black"
)
text_box.pack(padx=20, pady=20)

delete_timer = None
flash_timer = None

def clear_text():
    text_box.delete("1.0", END)
    text_box.config(bg="white")

def flash_warning():
    text_box.config(bg="#fcd34d")
    window.after(300, lambda: text_box.config(bg="white"))

def reset_timer(event=None):
    global flash_timer, delete_timer
    if delete_timer:
        window.after_cancel(delete_timer)
    if flash_timer:
        window.after_cancel(flash_timer)

    flash_timer = window.after(4500, flash_warning)
    delete_timer = window.after(5000, clear_text)

text_box.bind("<Key>", reset_timer)

window.mainloop()