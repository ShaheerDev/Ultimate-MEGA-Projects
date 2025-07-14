from tkinter import *
from tkinter import filedialog
import random
import time

GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"

sentences = [
    "Technology has changed the way we live, work, and communicate. From smartphones to artificial intelligence, the world is evolving faster than ever before.",
    "A good friend is like a four-leaf clover—hard to find, but lucky to have. True friendship is built on trust, laughter, and shared memories.",
    "The sun was setting behind the mountains, painting the sky in shades of orange and pink. Birds flew home, and the cool breeze whispered through the trees.",
    "Python is a beginner-friendly programming language. Its simple syntax makes it a popular choice for building apps, games, and websites.",
    "Reading books opens doors to new worlds, ideas, and adventures. It improves your vocabulary and helps you understand different perspectives."


]
random_sentence = random.choice(sentences)

start_time = 0

window = Tk()
window.title("Typing Test")
window.geometry("900x600")
window.config(padx=50, pady=50, bg=YELLOW)


title_label = Label(text="Typing Test", font=(FONT_NAME, 60, "bold"), fg=GREEN, bg=YELLOW)
title_label.place(x=150, y=0)


canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 112, image=logo_img)
canvas.place(x=300, y=100)

start_test = Button(window, text="Start Test", command= lambda:start())
start_test.place(x=350, y=350)

default_text = "Type Here.."

def start():
    title_label.destroy()
    canvas.destroy()
    enter_text = Text(window, height=3, width=30, font=(FONT_NAME, 30, "bold"), fg=GREEN, bg=YELLOW)
    enter_text.place(x=50, y=350)
    enter_text.insert(END, default_text)

    show_text = Label(text=random_sentence, font=(FONT_NAME, 30, "bold"), fg=GREEN, bg=YELLOW, wraplength=600, justify="center")
    show_text.place(x=120, y=0)

    global start_time
    start_time = time.time()

    submit_btn = Button(window, text="Submit", command= lambda:get_user_input())
    submit_btn.place(x=400, y=500)

    def clear_text(event):
        current_text = enter_text.get("1.0", END)
        if current_text.strip() == default_text:
            enter_text.delete("1.0", END)

    enter_text.bind("<FocusIn>", clear_text)

    def get_user_input():
        typed_text = enter_text.get("1.0", END).strip()
        enter_text.destroy()
        submit_btn.destroy()
        show_text.destroy()
        start_test.destroy()
        canvas.destroy()
        end_time = time.time()
        duration = end_time - start_time
        if duration < 60:
            print(f"Time taken: {duration:.2f} seconds")
            duration_label = Label(text=f"Your Time {duration:.2f}", font=(FONT_NAME, 30, "bold"), fg=GREEN, bg=YELLOW,
                                   wraplength=600, justify="center")
        else:
            minutes = duration / 60
            print(f"Time taken: {minutes:.2f} minutes")
            duration_label = Label(text=f"Your Time {minutes:.2f}", font=(FONT_NAME, 30, "bold"), fg=GREEN, bg=YELLOW,
                                   wraplength=600, justify="center")

        duration_label.place(x=150, y=0)
        print(typed_text)
        word_count = len(typed_text.split())
        if duration > 0:
            wpm = (word_count / duration) * 60
            wpm_label = Label(text=f"Your WPM {wpm:.2f}", font=(FONT_NAME, 30, "bold"), fg=GREEN, bg=YELLOW,
                                   wraplength=600, justify="center")
            wpm_label.place(x=150, y=100)
        else:
            wpm = 0

        target_words = random_sentence.split()
        typed_words = typed_text.split()

        mistakes=0
        for i in range(min(len(target_words), len(typed_words))):
            if target_words[i] != typed_words[i]:
                mistakes += 1

        extra_words = abs(len(target_words) - len(typed_words))
        mistakes += extra_words

        total_words = len(target_words)
        correct_words = total_words - mistakes
        accuracy = (correct_words / total_words) * 100

        mistakes_label = Label(text=f"Mistakes Counter: {mistakes}", font=(FONT_NAME, 30, "bold"), fg=GREEN, bg=YELLOW, wraplength=600, justify="center")
        accuracy_label = Label(text=f"Accuracy in %: {accuracy:.2f}", font=(FONT_NAME, 30, "bold"), fg=GREEN, bg=YELLOW,
                               wraplength=600, justify="center")
        mistakes_label.place(x=150, y=200)
        accuracy_label.place(x=150, y=300)
window.mainloop()