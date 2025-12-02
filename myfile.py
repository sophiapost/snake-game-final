import tkinter
import random
import os

#  CONSTANTS 
ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * ROWS
WINDOW_HEIGHT = TILE_SIZE * COLS

HIGHSCORE_FILE = "highscore.txt"

# TILE CLASS (creates tile for x and y values)
class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# HIGH SCORE FUNCTIONS 
def load_high_score():
    if os.path.exists(HIGHSCORE_FILE):
        try:
            with open(HIGHSCORE_FILE, "r") as f:
                return int(f.read())
        except ValueError:
            return 0
    return 0

def save_high_score(score):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(score))

# INITIAL VARIABLES 
snake = None
food = None
snake_body = []
velocity_x = 0
velocity_y = 0
game_over = False
score = 0
level = 1
starting_speed = 150
speed = starting_speed
difficulty_selected = False
paused = False
high_score = load_high_score()

# INITIALIZE WINDOW 
window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)

canvas = tkinter.Canvas(window,bg="black",width=WINDOW_WIDTH,height=WINDOW_HEIGHT,highlightthickness=0)
canvas.pack()
window.update()

# MENU 
menu_frame = tkinter.Frame(window, bg="black")
menu_frame.place(relx=0.5, rely=0.5, anchor="center")

title_label = tkinter.Label(menu_frame,text="Select Difficulty",fg="white",bg="black",font=("Arial", 28))
title_label.pack(pady=10)

def choose_easy():
    global starting_speed, difficulty_selected
    starting_speed = 180
    difficulty_selected = True
    menu_frame.place_forget()
    reset_game()

def choose_medium():
    global starting_speed, difficulty_selected
    starting_speed = 120
    difficulty_selected = True
    menu_frame.place_forget()
    reset_game()

def choose_hard():
    global starting_speed, difficulty_selected
    starting_speed = 70
    difficulty_selected = True
    menu_frame.place_forget()
    reset_game()
#what the buttons look like
easy_button = tkinter.Button(menu_frame, text="Easy", width=12, height=2, command=choose_easy)
easy_button.pack(pady=5)

medium_button = tkinter.Button(menu_frame, text="Medium", width=12, height=2, command=choose_medium)
medium_button.pack(pady=5)

hard_button = tkinter.Button(menu_frame, text="Hard", width=12, height=2, command=choose_hard)
hard_button.pack(pady=5)

# Restart button
restart_button = tkinter.Button(window, text="Restart", width=12, height=2)

# GAME FUNCTIONS 
def reset_game():
    #Reset the snake game 
    global snake, food, snake_body, velocity_x, velocity_y
    global game_over, score, level, speed, paused

    snake = Tile(5 * TILE_SIZE, 5 * TILE_SIZE)
    food = Tile(10 * TILE_SIZE, 10 * TILE_SIZE)

    snake_body.clear()
    velocity_x = 0
    velocity_y = 0

    game_over = False
    score = 0
    level = 1
    speed = starting_speed
    paused = False

    restart_button.place_forget()

def restart_action():
    #Show the difficulty menu 
    global difficulty_selected, paused
    difficulty_selected = False
    paused = False
    restart_button.place_forget()
    menu_frame.place(relx=0.5, rely=0.5, anchor="center")

def toggle_pause(event=None):
    #Pause or resume with space bar
    global paused
    if not difficulty_selected or game_over:
        return
    paused = not paused
#update level and speed 
def update_level_and_speed():
    global level, speed
    level += 1
    speed = max(40, speed - 8)

def change_direction(event):
    global velocity_x, velocity_y

    if game_over or paused:
        return
# keys to move the snake 
    if event.keysym == "Up" and velocity_y != 1:
        velocity_x = 0
        velocity_y = -1
    elif event.keysym == "Down" and velocity_y != -1:
        velocity_x = 0
        velocity_y = 1
    elif event.keysym == "Left" and velocity_x != 1:
        velocity_x = -1
        velocity_y = 0
    elif event.keysym == "Right" and velocity_x != -1:
        velocity_x = 1
        velocity_y = 0

def move_snake():
    global snake, food, snake_body, score, game_over, high_score

    if game_over or paused or not difficulty_selected:
        return

    # Move body
    for i in range(len(snake_body) - 1, 0, -1):
        snake_body[i].x = snake_body[i - 1].x
        snake_body[i].y = snake_body[i - 1].y

    if snake_body:
        snake_body[0].x = snake.x
        snake_body[0].y = snake.y

    # Move head
    snake.x += velocity_x * TILE_SIZE
    snake.y += velocity_y * TILE_SIZE

    # Wall collision
    if snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT:
        game_over = True
        check_high_score()
        return

    # Self collision
    for tile in snake_body:
        if snake.x == tile.x and snake.y == tile.y:
            game_over = True
            check_high_score()
            return

    # Food collision
    if snake.x == food.x and snake.y == food.y:
        snake_body.append(Tile(food.x, food.y))
        food.x = random.randint(0, COLS - 1) * TILE_SIZE
        food.y = random.randint(0, ROWS - 1) * TILE_SIZE
        global score
        score += 1
        update_level_and_speed()
#high score checking 
def check_high_score():
    global score, high_score
    if score > high_score:
        high_score = score
        save_high_score(high_score)

def draw():
    canvas.delete("all")

    if not difficulty_selected:
        window.after(50, draw)
        return

    move_snake()

    # Draw food
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill="red")

    # Draw snake what it looks like 
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill="blue")
    for t in snake_body:
        canvas.create_rectangle(t.x, t.y, t.x + TILE_SIZE, t.y + TILE_SIZE, fill="blue")

    # Game Over what the button looks like 
    if game_over:
        canvas.create_text(
            WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 60,font="Arial 22",fill="white",text=f"GAME OVER\nScore: {score}\nLevel: {level}\nHigh Score: {high_score}")
        restart_button.place(relx=0.5, rely=0.6, anchor="center")
    else:
        canvas.create_text(
            110, 20, font="Arial 12",text=f"Score: {score}  Level: {level}  High Score: {high_score}" + ("  [PAUSED]" if paused else ""),fill="white")

    window.after(speed, draw)

#  BUTTON COMMANDS 
restart_button.config(command=restart_action)

# KEYBINDINGS 
window.bind("<KeyRelease>", change_direction)
window.bind("<space>", toggle_pause)  # Space bar to pause/resume

# START GAME 
draw()
window.mainloop()