import tkinter as tk
import random
import time

# --- Game State Variables ---
score = 0
time_left = 30
game_active = False
game_paused = False

# --- Functions ---
def move_rabbit():
    """Moves the rabbit button to a random location."""
    global rabbit_button, game_active, game_paused
    if game_active and not game_paused:
        window_width = window.winfo_width()
        window_height = window.winfo_height()
        button_width = rabbit_button.winfo_width()
        button_height = rabbit_button.winfo_height()
        max_x = window_width - button_width
        max_y = window_height - button_height
        new_x = random.randint(0, max_x)
        new_y = random.randint(0, max_y)
        rabbit_button.place(x=new_x, y=new_y)

def catch_rabbit():
    """Increments the score, adds time, and triggers the rabbit to move."""
    global score, score_label, time_left, game_active, game_paused
    if game_active and not game_paused:
        score += 1
        score_label.config(text=f"Score: {score}")
        time_left += 5
        timer_label.config(text=f"Time: {time_left}")
        move_rabbit() # Move the rabbit immediately after being caught

def update_timer():
    """Updates the timer display and ends the game if time runs out."""
    global time_left, timer_label, game_active, game_paused, rabbit_button
    if game_active and not game_paused:
        if time_left > 0:
            timer_label.config(text=f"Time: {time_left}")
            time_left -= 1
            window.after(1000, update_timer)
        elif time_left == 0:
            game_active = False
            if rabbit_button.winfo_ismapped(): # Check if button is currently visible
                rabbit_button.pack_forget()
            timer_label.config(text="Time's Up!")
            show_start_menu() # Go back to start menu when game ends

def start_rabbit_movement():
    """Starts the continuous movement of the rabbit."""
    global game_active, game_paused
    if game_active and not game_paused:
        move_rabbit()
        window.after(2500, start_rabbit_movement)
    elif not game_active or game_paused:
        pass

def pause_game():
    """Toggles the pause state of the game."""
    global game_paused, pause_button, game_active
    if not game_active:
        return
    game_paused = not game_paused
    if game_paused:
        pause_button.config(text="Resume")
    else:
        pause_button.config(text="Pause")
        start_rabbit_movement()
        update_timer()

def quit_game():
    """Returns to the start menu."""
    global game_active, score_label, timer_label, rabbit_button, pause_button, quit_button, score, time_left, game_paused
    game_active = False
    game_paused = False
    score = 0
    time_left = 30

    # Hide game elements
    score_label.pack_forget()
    timer_label.pack_forget()
    if rabbit_button.winfo_ismapped(): # Check if button is currently visible
        rabbit_button.pack_forget()
    pause_button.place_forget()
    quit_button.place_forget()

    # Show start menu elements
    game_title_label.pack(pady=50)
    start_button.pack(pady=20)
    exit_button.pack()

def exit_game():
    """Closes the game window."""
    window.destroy()

def start_game():
    """Starts the main game by hiding the start menu and showing game elements."""
    global game_active, score, time_left, rabbit_button
    start_button.pack_forget()
    game_title_label.pack_forget()
    exit_button.pack_forget()

    score = 0
    time_left = 30
    game_active = True

    score_label.pack(pady=10)
    timer_label.pack()
    rabbit_button.pack(pady=10) # Show rabbit when game starts
    pause_button.place(relx=1.0, rely=1.0, anchor=tk.SE, x=-10, y=-10)
    quit_button.place(relx=1.0, rely=1.0, anchor=tk.SE, x=-80, y=-10)

    # Initial rabbit placement
    move_rabbit()
    start_rabbit_movement()
    update_timer()

def show_start_menu():
    """Shows the start menu elements and ensures game elements are hidden."""
    game_title_label.pack(pady=50)
    start_button.pack(pady=20)
    exit_button.pack()
    if rabbit_button.winfo_ismapped(): # Check if button is currently visible
        rabbit_button.pack_forget()

# --- Main Window Setup ---
window = tk.Tk()
window.title("Catch the Rabbit!")
window.geometry("400x350")

# --- Start Menu Elements ---
game_title_label = tk.Label(window, text="Catch the Rabbit!", font=("Arial", 24))
start_button = tk.Button(window, text="Start Game", font=("Arial", 16), command=start_game)
exit_button = tk.Button(window, text="Exit Game", font=("Arial", 16), command=exit_game)

# --- Game Elements (Initially Hidden) ---
score_label = tk.Label(window, text=f"Score: {score}", font=("Arial", 16))
timer_label = tk.Label(window, text=f"Time: {time_left}", font=("Arial", 16))
rabbit_button = tk.Button(window, text="🐇", font=("Arial", 24), command=catch_rabbit)
pause_button = tk.Button(window, text="Pause", font=("Arial", 12), command=pause_game)
quit_button = tk.Button(window, text="Return to Menu", font=("Arial", 12), command=quit_game)

# --- Initial Start Menu Display ---
show_start_menu()

# --- Start the Tkinter Event Loop ---
window.mainloop()
