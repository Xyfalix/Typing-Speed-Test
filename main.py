from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import colorchooser
import random
import time

# ---------------------------- CONSTANTS ------------------------------- #
FONT_NAME = "Arial"
chosen_color = 'black'
correct_characters = 0
words_typed = 0
cpm = 0 # Initialize cpm variable
wpm = 0  # Initialize wpm variable
start_time = 0
first_call = True
high_score = 0
elapsed_time = 0
countdown_id = None
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
high_score_display = Label(window, text=f'High Score: {high_score} WPM', font=(FONT_NAME, 20), fg='white', bg='#3E3B36')
high_score_display.grid(column=1, row=0, pady=20)

# ---------------------------- Time Display Widget ------------------------------- #
time_left_display = Label(window, text=f'Time Left: ', font=(FONT_NAME, 20), fg='white', bg='#3E3B36')
time_left_display.grid(column=1, row=1, pady=20)

def countdown(count):
    global countdown_id
    global wpm
    global cpm
    global high_score
    # change text in label
    time_left_display['text'] = f'Time Left: {count}s'

    if count > 0:
        # call countdown again after 1000ms (1s)
        countdown_id = window.after(1000, countdown, count - 1)

    else:
        # disable further user input into the text entry widget once time is up.
        typing_entry.config(state='disabled')
        typing_entry.unbind_all('<KeyPress>')
        typing_entry.unbind_all('<space>')

        # disable further interaction with the textbox widget.
        word_list.config(state='disabled')

        # Remove focus from all widgets to prevent further user interaction
        window.focus_set()

        # Update high score when time is up if wpm is higher than the current high score.
        if wpm > high_score:
            cpm = correct_characters
            cpm_display['text'] = f'Corrected CPM: {round(cpm)}'
            wpm = words_typed
            wpm_display['text'] = f'WPM: {round(wpm)}'
            high_score_display['text'] = f'High Score: {round(wpm)} WPM'
            high_score = wpm


# ---------------------------- CPM, WPM displays ------------------------------- #
cpm_display = Label(window, text=f'Corrected CPM: {cpm}', font=(FONT_NAME, 14), fg='white', bg='#3E3B36')
cpm_display.grid(column=0, row=2, pady=20)

wpm_display = Label(window, text=f'WPM: {wpm}', font=(FONT_NAME, 14), fg='white', bg='#3E3B36')
wpm_display.grid(column=1, row=2, pady=20)

# ---------------------------- Restart Button ------------------------------- #
def restart():
    global chosen_color, correct_characters, words_typed, cpm, wpm, start_time, first_call, elapsed_time, countdown_id,\
        word_list_index, words, high_score

    # Stop the countdown
    if countdown_id:
        window.after_cancel(countdown_id)
        countdown_id = None

    # Reset all variables to their initial values
    chosen_color = 'black'
    correct_characters = 0
    words_typed = 0
    cpm = 0
    wpm = 0
    start_time = 0
    first_call = True
    elapsed_time = 0
    word_list_index = 0

    # Reset UI elements here
    time_left_display['text'] = 'Time Left: '
    cpm_display['text'] = f'Corrected CPM: {cpm}'
    wpm_display['text'] = f'WPM: {wpm}'
    typing_entry.config(state='normal')
    word_list.config(state='normal')
    word_list.delete('1.0', END)
    typing_entry.delete(0, END)
    typing_entry.insert(0, 'Type text here')  # Add default text

    with open('1000_words.txt', 'r') as file:
        words = file.read().splitlines()
        random.shuffle(words)

    for word in words:
        word_list.insert(END, f'{word} ')

    typing_entry.bind('<KeyPress>', on_entry_key)
    typing_entry.bind('<space>', on_entry_key)


restart_button = Button(window, text="Restart", font=(FONT_NAME, 14), bg="#36393e", fg="white", width=7, command=restart)
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

# Count the number of correct characters typed by the user.
word_list.tag_configure("correct")

# Disable the textbox to prevent the user from interacting with it.
word_list.config(state='disabled')

def highlight_char(event):
    global word_list_index
    global first_call
    global start_time
    global correct_characters
    # highlight correct character in blue
    typed_entry = list(typing_entry.get().strip())

    current_word = words[word_list_index - 1]

    # get starting index of current word
    start_index_str = word_list.search(f"\\m{current_word}\\M", "1.0", stopindex="end", regexp=True)

    # get col from starting index str and convert to int
    start_index_col = int(start_index_str.split(".")[1])

    # iterate through the typed entry and highlight blue or red
    for char in range(len(current_word)):
        if char < len(typed_entry):
            if typed_entry[char] == current_word[char]:
                word_list.tag_remove("red", f"1.{start_index_col + char}")
                word_list.tag_add("blue", f"1.{start_index_col + char}")
                word_list.tag_add("correct", f"1.{start_index_col + char}")
            else:
                word_list.tag_remove("blue", f"1.{start_index_col + char}")
                word_list.tag_remove("correct", f"1.{start_index_col + char}")
                word_list.tag_add("red", f"1.{start_index_col + char}")
        else:
            # Remove both "blue" and "red" tags for characters beyond the typed entry
            word_list.tag_remove("blue", f"1.{start_index_col + char}")
            word_list.tag_remove("red", f"1.{start_index_col + char}")
            word_list.tag_remove("correct", f"1.{start_index_col + char}")

    # Get the ranges of text with the "blue" tag
    correct_ranges = word_list.tag_ranges("correct")

    # Calculate the total number of characters tagged with "blue"
    correct_characters = sum(len(word_list.get(start, end)) for start, end in zip(correct_ranges[0::2],
                                                                                  correct_ranges[1::2]))

    # start the timing when the user starts an input
    if first_call:
        start_time = time.time()
        first_call = False

def highlight_word(event):
    global word_list_index

    # highlight entire word in green background
    start_index_str = word_list.search(f"\\m{words[word_list_index]}\\M", "1.0", stopindex="end", regexp=True)
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

    word_list.tag_add("highlight", start_index_str, end_index_str)

    word_list_index += 1

def remove_highlight(event):
    global word_list_index
    global first_call
    global start_time
    global correct_characters
    global words_typed
    global high_score
    global cpm
    global wpm
    global elapsed_time

    start_index_str = word_list.search(f"\\m{words[word_list_index-1]}\\M", "1.0", stopindex="end", regexp=True)
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
    word_list.tag_remove("highlight", start_index_str, end_index_str)

    # increment words_typed if word typed correctly. Highlight wrong words entirely in red.
    if typing_entry.get().strip() == words[word_list_index-1]:
        words_typed += 1
    else:
        word_list.tag_remove("blue", start_index_str, end_index_str)
        word_list.tag_add("red", start_index_str, end_index_str)

    # scroll down by 1 line if previous and current word has a row difference of at least 1
    index_coordinates = word_list.bbox(start_index_str)
    if index_coordinates[1] > 100:
        word_list.yview_scroll(1, "units")  # Scroll down by 1 line

    elapsed_time = time.time() - start_time
    # Calculate cpm and wpm within the 60s time limit.
    if elapsed_time <= 60:
        cpm = correct_characters / elapsed_time * 60
        cpm_display['text'] = f'Corrected CPM: {round(cpm)}'
        wpm = words_typed / elapsed_time * 60
        wpm_display['text'] = f'WPM: {round(wpm)}'


def highlight_and_remove(event):
    remove_highlight(None)
    highlight_word(None)

# ---------------------------- Typing Entry ------------------------------- #
def on_entry_key(event):
    typing_entry.delete(0, END)

    # Start countdown after the first keypress
    countdown(60)

    typing_entry.unbind('<KeyPress>')
    typing_entry.unbind('<space>')

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

typing_entry.bind('<KeyPress>', on_entry_key)
typing_entry.bind('<space>', on_entry_key)

# prevent user from spamming the space key when there is no text entry
typing_entry.bind('<KeyRelease>', validate_space, add="+")


# ---------------------------- Credits ------------------------------- #
credit_label = Label(window, text='Created by: Nicholas Lim', font=(FONT_NAME, 14), fg='white', bg='#3E3B36')
credit_label.grid(column=0, row=6, columnspan=3, pady=20)

window.mainloop()

