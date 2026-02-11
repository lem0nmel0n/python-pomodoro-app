from tkinter import *
import platform
import os
if platform.system() == "Windows":
    import winsound

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#f1583f"
GREEN = "#359b44"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25  # Return to 25 once done debugging
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

sequence = [WORK_MIN, SHORT_BREAK_MIN, WORK_MIN, SHORT_BREAK_MIN, WORK_MIN, SHORT_BREAK_MIN, WORK_MIN, LONG_BREAK_MIN]
session_index = 0
work_sessions_completed = 0
timer = None
paused = False
remaining_time = 0


# ---------------------------- TIMER RESET ------------------------------- #

def reset_timer():
    global session_index, work_sessions_completed, paused, remaining_time
    remaining_time = 0
    start_btn.config(state="normal")
    paused = False
    if timer:
        window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    session_index = 0
    work_sessions_completed = 0
    num_checks = ""
    tick_label.config(text=num_checks)
    timer_label_text = "Timer"
    colour = GREEN
    timer_label.config(text=timer_label_text, fg=colour)


# ---------------------------- PAUSE AND UNPAUSE ----------------------------- #

def pause():
    global paused, timer, remaining_time
    paused = not paused
    if paused and timer:
        pause_unpause_btn.config(text="Unpause", fg="#359b44")
        window.after_cancel(timer)
    else:
        pause_unpause_btn.config(text="Pause", fg="#f36848")
        # Resume countdown with the remaining time by getting the existing time on screen
        
        if remaining_time != 0:
            count_down(remaining_time)


# ---------------------------- TIMER MECHANISM ------------------------------- #


def start_timer():
    global session_index, work_sessions_completed, paused
    play_sound()
    start_btn.config(state="disabled") #added this so you can't press start multiple times :)
    if session_index % 2 == 1:
        """Updates the number of tick marks below"""
        work_sessions_completed += 1
        num_checks = "✔" * work_sessions_completed
        tick_label.config(text=num_checks)
        """Updates the text above whether BREAK or TIMER"""
        timer_label_text = "Break"
        colour = PINK
        if session_index == len(sequence) - 1:
            colour = RED
    elif session_index % 2 == 0:
        """Updates the text above whether BREAK or TIMER"""
        timer_label_text = "Timer"
        colour = GREEN
    timer_label.config(text=timer_label_text, fg=colour)
    count_down(sequence[session_index] * 60)  # Add the *60 to session index once done debugging


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global session_index, timer, remaining_time
    remaining_time = count
    minutes = int(count // 60)
    seconds = int(count % 60)
    """Reflects the timer countdown on the widget"""
    canvas.itemconfig(timer_text, text=f"{minutes:02d}:{seconds:02d}") #simplified the formatting logic

    if count > 0 and not paused:
        """Keeps the timer running"""
        timer = window.after(1000, count_down, count - 1)  # Use 1000 for 1 second interval
    elif count == 0:
        play_sound()
        session_index += 1
        if session_index < len(sequence):
            start_timer()
# ---------------------------- PLAY SOUND ------------------------------- #
#
def play_sound():
    system = platform.system()
    if system.lower() == "windows":
        winsound.PlaySound("session_end.wav", winsound.SND_FILENAME)
    else:
        os.system("aplay session_end.wav &")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
img = PhotoImage(file="./tomato.png")
canvas.create_image(100, 112, image=img)
timer_text = canvas.create_text(103, 132, text="00:00", font=(FONT_NAME, 36, "bold"), fill="White")
canvas.grid(column=1, row=1)

timer_label = Label(text="Timer", font=(FONT_NAME, 48))
timer_label.config(padx=0, pady=0, fg=GREEN, bg=YELLOW)
timer_label.grid(column=1, row=0)

spacing_label = Label(window, bg=YELLOW)
spacing_label.grid(column=1, row=2)

start_btn = Button(text="Start", highlightbackground=YELLOW, fg="#359b44", command=start_timer)
start_btn.grid(column=0, row=3)

reset_btn = Button(text="Reset", highlightbackground=YELLOW, fg="#f1583f", command=reset_timer)
reset_btn.grid(column=2, row=3)

pause_unpause_btn = Button(text="Pause", highlightbackground=YELLOW, fg="#f36848", command=pause)
pause_unpause_btn.grid(column=1, row=3)

tick_label = Label(bg=YELLOW, fg=GREEN, font=(FONT_NAME, 50))
tick_label.grid(column=1, row=4)

window.mainloop()
