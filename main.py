import math
from text import text
from tkinter import *

LIGHT_GREEN = "#9FE6A0"
RED = "#F55C47"
VIOLET = "#564A4A"
DARK_GREEN = "#4AA96C"

#----------------------------------LOGIC-----------------------------------------#

# --------------------------------TESTING----------------------------------------#

correct_words = 0
current_word = ""
index_of_word_in_list = 0

# Chars to be highlighted in the text
ch_start = 0
ch_finish = len(text[0])


def start_test(_):
    window.unbind("<Key>")
    window.bind("<space>", check_word)
    count_down(_)


def check_word(_):
    global correct_words
    global current_word
    global index_of_word_in_list
    global ch_start
    global ch_finish

    user_word = input.get()
    user_word = user_word[:-1]

    if user_word == current_word:
        correct_words +=1
    else:
        text_to_type.tag_add('highlightred', f'1.0 + {ch_start} chars', f'1.0 + {ch_finish} chars')
        text_to_type.tag_configure('highlightred', foreground=RED)

    input.delete(0, "end")
    ch_start += len(current_word) + 1
    index_of_word_in_list += 1
    ch_finish = ch_finish + len(text[index_of_word_in_list]) + 1
    ch_finish = int(ch_finish)
    input.delete(0, 'end')
    type_word()


def type_word():
    global current_word
    global index_of_word_in_list
    global ch_start
    global ch_finish
    text_to_type.tag_delete('highlightline', 1.0)
    current_word = text[index_of_word_in_list]
    text_to_type.tag_add('highlightline', f'1.0 + {ch_start} chars', f'1.0 + {ch_finish} chars')
    text_to_type.tag_configure('highlightline', background=LIGHT_GREEN)

def new_test():
    pop.destroy()
    input.config(state="normal")
    input.focus()
    window.bind("<Key>", start_test)
    type_word()


# --------------------------------TIMER COUNTDOWN---------------------------------------#
count = 60

def count_down(_):
    global count
    global index_of_word_in_list
    global ch_start
    global ch_finish
    if count < 0:
        count = 60
        index_of_word_in_list = 0
        ch_start = 0
        ch_finish = len(text[0])
        text_to_type.tag_delete('highlightred', 1.0)
        input.delete(0, 'end')
        show_result()
        return
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    time_text.config(text=f"{count_min}:{count_sec}")
    count -= 1
    window.after(1000, count_down, "_")


# --------------------------------SHOW RESULT---------------------------------------#

def show_result():
    global correct_words
    global pop
    window.unbind("<space>")
    input.delete(0, "end")
    input.config(state='disabled')

    # custom dialog which does not respond to keyboard presses (user will not accidentally close dialog while typing)
    pop = Toplevel()
    pop.title("Test is completed")
    pop.geometry("530x150")
    pop.config(bg=VIOLET, padx=20, pady=20)

    frame = Frame(pop, bg=VIOLET)
    frame.pack()
    pop_text = Label(frame, text=f"Your result is {correct_words} words per minute.\nThe average typing speed is 40 words per minute.",
                      fg="white", font="Open-Sans 15 bold", bg=VIOLET)
    pop_text.pack(pady=10)
    ok_button = Button(frame, text="OK", command=new_test, bg="white", fg=VIOLET)
    ok_button.pack()


#----------------------------------UI--------------------------------------#

# -----------------------------WINDOW CONFIGURATION------------------------#
window = Tk()
window.title("Typing Speed Test")
window.config(padx=45, pady=50, bg=DARK_GREEN)
window.geometry("1300x750")

# --------------------------------CLOCK UI----------------------------------#
canvas = Canvas(width=300, height=128, bg=DARK_GREEN, highlightthickness=0)
clock_img = PhotoImage(file="clock.png")
canvas.create_image(64, 64, image=clock_img)
canvas.place(relx=0.132, rely=0.1, anchor=CENTER)

# ---------------------------------CLOCK TEXT------------------------------#

time_text = Label(text="1:00", font="Open-Sans 20 bold", bg=DARK_GREEN, fg=VIOLET)
time_text.place(relx=0.126, rely=0.1, anchor=CENTER)

# ---------------------------------- HEADING-------------------- #

title = Label(text="Type highlighted word", bg=DARK_GREEN, fg=VIOLET, font=("Open-Sans", "24", "bold"))
title.place(relx=0.5, rely=0.1, anchor=CENTER)

# ---------------------------------TEXT------------------------------------#
text_to_type = Text(window, font=('Open-Sans 20 bold'), padx=15, pady=20, width=75, height=10, wrap="word")
text_to_type.insert(1.0, text)
text_to_type.config(state=DISABLED)
text_to_type.place(relx=0.5, rely=0.5, anchor=CENTER)

# ---------------------------------USER INPUT------------------------------------#
input = Entry(width=50)
input.focus()
input.place(relx=0.5, rely=0.85, anchor=CENTER)


# Start testing when user presses key
window.bind("<Key>", start_test)
type_word()

window.mainloop()
