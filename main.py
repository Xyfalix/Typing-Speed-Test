from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import colorchooser
import random

# ---------------------------- CONSTANTS ------------------------------- #
FONT_NAME = "Arial"
chosen_color = 'black'
first_call = True
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Typing Speed Test App")
window.config(bg='#3E3B36', width=1200, height=1200)
# Create 6 rows for window
for i in range(7):
    window.rowconfigure(i, weight=1)

# Create 3 columns for window
for i in range(3):
    window.columnconfigure(i, weight=1)

# ---------------------------- High Score Widget ------------------------------- #
high_score_display = Label(window, text='High Score: 300 WPM', font=(FONT_NAME, 20), fg='white', bg='#3E3B36')
high_score_display.grid(column=1, row=0, pady=20)

# ---------------------------- Time Display Widget ------------------------------- #
time_left_display = Label(window, text='Time Left: 60s', font=(FONT_NAME, 20), fg='white', bg='#3E3B36')
time_left_display.grid(column=1, row=1, pady=20)

def countdown(count):
    # change text in label
    time_left_display['text'] = f'Time Left: {count}s'

    if count > 0:
        # call countdown again after 1000ms (1s)
        window.after(1000, countdown, count - 1)

def start_countdown(event):
    countdown(60)
    # unbind the countdown function from the typing_entry widget after the first keypress
    typing_entry.unbind('<Key>', start_countdown)

# ---------------------------- CPM, WPM displays ------------------------------- #

cpm_display = Label(window, text='Corrected CPM: ', font=(FONT_NAME, 14), fg='white', bg='#3E3B36')
cpm_display.grid(column=0, row=2, pady=20)

wpm_display = Label(window, text='WPM: ', font=(FONT_NAME, 14), fg='white', bg='#3E3B36')
wpm_display.grid(column=1, row=2, pady=20)

# ---------------------------- Restart Button ------------------------------- #
restart_button = Button(window, text="Restart", font=(FONT_NAME, 14), bg="#36393e", fg="white", width=7)
restart_button.grid(column=2, row=2, padx=10, pady=20)

# ---------------------------- Word List ------------------------------- #
word_list = Text(window, height=3.5, width=40, bg='#36393e', font=(FONT_NAME, 30), fg='white',
                 spacing2=13, wrap='word')
word_list.grid(column=0, row=3, columnspan=3, rowspan=2, padx=20, pady=20)

with open('1000_words.txt', 'r') as file:
    words = file.read().splitlines()
    random.shuffle(words)
# Insert the words in the Text widget
for word in words:
    word_list.insert(END, f'{word} ')

# initialize word_list_index as a global variable
word_list_index = 0

# create highlight tag for highlight and remove functions
word_list.tag_config("highlight", background="green")

# create blue character font color change when correct character is typed
word_list.tag_config("blue", foreground="blue")

# create red character font color change when wrong character is typed
word_list.tag_config("red", foreground="red")

def highlight_char(event):
    global word_list_index

    # highlight correct character in blue
    typed_entry = list(typing_entry.get().strip())
    print(f'typed entry is {typed_entry}')

    current_word = words[word_list_index - 1]
    print(f'current_word is {current_word}')

    # get starting index of current word
    start_index_str = word_list.search(current_word, "1.0", stopindex="end")

    # get col from starting index str and convert to int
    start_index_col = int(start_index_str.split(".")[1])

    # iterate through the typed entry and highlight blue or red
    for char in range(len(current_word)):
        if char < len(typed_entry):
            if typed_entry[char] == current_word[char]:
                word_list.tag_remove("red", f"1.{start_index_col + char}")
                word_list.tag_add("blue", f"1.{start_index_col + char}")
            else:
                word_list.tag_remove("blue", f"1.{start_index_col + char}")
                word_list.tag_add("red", f"1.{start_index_col + char}")
        else:
            # Remove both "blue" and "red" tags for characters beyond the typed entry
            word_list.tag_remove("blue", f"1.{start_index_col + char}")
            word_list.tag_remove("red", f"1.{start_index_col + char}")

def highlight_word(event):
    global word_list_index
    global first_call

    # highlight entire word in green background
    start_index_str = word_list.search(words[word_list_index], "1.0", stopindex="end")
    start_index_rol_col = (start_index_str.split("."))

    # convert start_index_rol_col to int
    start_index_rol_col_int = [int(s) for s in start_index_rol_col]

    # add column index by length of word
    end_index_rol_col_int = start_index_rol_col_int
    for i in range(len(end_index_rol_col_int)):
        if i == 1:
            end_index_rol_col_int[i] += len(words[word_list_index])

    # convert end_index_rol_col_int back to str and join the row column indices with a "." between the 2
    end_index_rol_col = [str(s) for s in end_index_rol_col_int]
    end_index_str = ".".join(str(s) for s in end_index_rol_col)

    print(f'highlight_word start index is {start_index_str}')
    print(f'highlight_word end index is {end_index_str}')

    word_list.tag_add("highlight", start_index_str, end_index_str)

    word_list_index += 1

def remove_highlight(event):
    global word_list_index

    start_index_str = word_list.search(words[word_list_index-1], "1.0", stopindex="end")
    start_index_rol_col = (start_index_str.split("."))

    # convert start_index_rol_col to int
    start_index_rol_col_int = [int(s) for s in start_index_rol_col]

    # add column index by length of word
    end_index_rol_col_int = start_index_rol_col_int
    for i in range(len(end_index_rol_col_int)):
        if i == 1:
            end_index_rol_col_int[i] += len(words[word_list_index-1])

    # convert end_index_rol_col_int back to str and join the row column indices with a "." between the 2
    end_index_rol_col = [str(s) for s in end_index_rol_col_int]
    end_index_str = ".".join(str(s) for s in end_index_rol_col)

    print(f'remove_highlight start index is {start_index_str}')
    print(f'remove_highlight end index is {end_index_str}')
    word_list.tag_remove("highlight", start_index_str, end_index_str)

    if typing_entry.get().strip() == words[word_list_index-1]:
        print('Entry typed correctly!')
    else:
        print('Entry typed wrongly!')
        word_list.tag_remove("blue", start_index_str, end_index_str)
        word_list.tag_add("red", start_index_str, end_index_str)

def highlight_and_remove(event):
    remove_highlight(None)
    highlight_word(None)

# ---------------------------- Typing Entry ------------------------------- #
def on_entry_key(event):
    print(typing_entry.get())
    typing_entry.delete(0, END)

    # Start countdown after the first keypress
    countdown(60)

    typing_entry.unbind('<KeyPress>', on_entry_bind)
    typing_entry.unbind('<space>', on_entry_bind_space)

    # Call the function to highlight the initial word
    highlight_word(None)

    # prevent user from spamming the space key when there is no text entry
    typing_entry.bind('<KeyRelease>', validate_space, add="+")

    # highlight character as blue or red typed correctly and wrongly respectively.
    typing_entry.bind('<KeyRelease>', highlight_char)

    # rebind the highlight_and_remove bind
    typing_entry.bind('<KeyRelease-space>', highlight_and_remove)

    # Delete the typed word in text entry when spacebar is pressed
    typing_entry.bind('<KeyRelease-space>', delete_typed_word, add="+")


def delete_typed_word(event):
    typing_entry.delete(0, END)

# prevent user from spamming the space key when there is no text entry
def validate_space(event):
    if event.keysym == 'space':
        current_text = typing_entry.get()
        if current_text.strip() == '':
            return 'break'  # Prevents the space key from being inserted


typing_entry = Entry(window, font=(FONT_NAME, 20), width=58)
typing_entry.insert(0, 'Type text here')  # Add default text
typing_entry.grid(column=0, row=5, columnspan=3, pady=10)

on_entry_bind = typing_entry.bind('<KeyPress>', on_entry_key)
on_entry_bind_space = typing_entry.bind('<space>', on_entry_key)

# prevent user from spamming the space key when there is no text entry
typing_entry.bind('<KeyRelease>', validate_space, add="+")


# ---------------------------- Credits ------------------------------- #
credit_label = Label(window, text='Created by: Nicholas Lim', font=(FONT_NAME, 14), fg='white', bg='#3E3B36')
credit_label.grid(column=0, row=6, columnspan=3, pady=20)


window.mainloop()
# Functionality Checklist
# TODO 1: Timer for 60s countdown.
#  1) Once the timer hits 0s, end the test and show results, and add an option to restart.
#  2) Timer starts counting down once user types the first character.
#  3) Also add a restart button on the main UI in the event user wants a do-over.

# TODO 2: Restart button for resetting the typing speed test.
#  Reset will do the following.
#  1) Reset the timer to 60s.
#  2) Generate a random list of words to type.
#  3) Highlight the first word to type.

# TODO 3: Characters per minute (CPM) and corrected CPM display. WPM display
#  1) Corrected CPM calculated by number of correct characters typed divided by elapsed time, updated after every word.
#  Set initial values to "-"

# TODO 4: Highscore display for WPM.

# TODO 5: Get a random list of words and pull out some of these words to display on the UI, separated by spaces.
#  1) Highlight the word to be typed.
#  2) Correct words are highlighted in green after completion, characters typed correctly are in blue.
#  Wrong words or characters are in red.
#  3) Generate a new line of words after the second to last line has been completed,
#  and move the entire display upwards, hiding the first line and revealing the line underneath.
#  4)

