from tkinter import *
from tkinter import messagebox
import tkinter
from PIL import Image, ImageTk
from tkinter_custom_button import TkinterCustomButton
from text_sample import sample


timer = None
start = False
text_to_show = sample[:1400]


def reset_timer():
    global start, timer
    typing_field.delete("1.0", "end")
    start = False
    timer_text['fg'] = 'blue'
    timer_text['text'] = 'Timer Ready!'
    typing_field['state'] = 'disabled'
    window.after_cancel(timer)


def start_timer():
    global start, timer
    if not start:
        start = True
        typing_field.delete("1.0", "end")
        typing_field['state'] = 'normal'
        count_down(61)
    else:
        reset_timer()


def count_down(secs):
    global timer, start
    if start:
        timer_text['text'] = secs
        if secs > 0:
            timer = window.after(1000, count_down, secs - 1)
            if secs <= 10:
                timer_text['fg'] = "red"
        else:
            timer_text['fg'] = "red"
            timer_text["text"] = "Time Out!"
            typing_field['state'] = 'disabled'
            calculate_typing_speed()


def calculate_typing_speed():
    text_list = text_to_show.strip().split()
    typed_list = typing_field.get("1.0", "end").strip().split()

    wpm = 0
    valid_words = 0

    for i in range(len(typed_list)):
        if text_list[i] == typed_list[i]:
            wpm += 1
        if typed_list[i] in text_list:
            valid_words += 1

    accuracy_percentage = round(valid_words / len(typed_list) * 100, 2)

    messagebox.showinfo(
        title="Results"
        , message=f"""Word Per Minute(WPM): {wpm}
        \nTotal words typed: {len(typed_list)}
        \nAccuracy Percentage: {accuracy_percentage}%""")


window = Tk()
window.title("Typing Speed Test")
window.config(bg="#f7f5dd")

BG_COLOR = "#f7f5dd"

canvas = Canvas(width=700, height=750)

image = Image.open("images/card_back.png")

resized_image = image.resize((680, 680))

card_image = ImageTk.PhotoImage(resized_image)
text_card_background = canvas.create_image(350, 400, image=card_image)
canvas.create_text(350, 380, text=text_to_show, font=("Ariel", 15), width=600)
canvas.config(bg=BG_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, padx=50, rowspan=4)

start_btn = TkinterCustomButton(text="START/STOP", corner_radius=10, command=start_timer)
start_btn.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
start_btn.grid(row=0, column=1, rowspan=1)

l1 = Label(text="Click START/STOP to enable/disable the typing field.", bg=BG_COLOR, font=("Arial", 20))
l1.grid(row=1, column=1, rowspan=1)

timer_text = Label(text="Timer Ready!", bg=BG_COLOR, font=("Arial", 25), fg="blue")
timer_text.grid(row=2, column=1, rowspan=1)

typing_field = Text(width=60, height=20, padx=35, pady=35, font=("Arial", 13))
typing_field['state'] = 'disabled'
typing_field.grid(row=3, column=1, rowspan=1)

window.mainloop()
