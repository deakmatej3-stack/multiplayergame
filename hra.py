import tkinter as tk
import copy

CELL_SIZE = 50

LEVELS = [
    [
        [1,1,1,1,1,1,1],
        [1,0,0,1,0,"K",1],
        [1,0,1,1,1,0,1],
        [1,0,0,0,1,0,1],
        [1,1,1,0,1,0,1],
        [1,0,0,0,0,"E",1],
        [1,1,1,1,1,1,1]
    ],
    [
        [1,1,1,1,1,1,1],
        [1,0,0,0,1,0,1],
        [1,0,1,0,1,"K",1],
        [1,0,1,0,0,0,1],
        [1,0,1,1,1,0,1],
        [1,0,0,0,0,"E",1],
        [1,1,1,1,1,1,1]
    ],
    [
        [1,1,1,1,1,1,1],
        [1,"K",0,"P",1,0,1],
        [1,0,1,0,1,0,1],
        [1,0,1,0,0,0,1],
        [1,0,1,1,1,0,"E"],
        [1,0,0,0,0,0,1],
        [1,1,1,1,1,1,1]
    ]
]

player_x = 1
player_y = 1
has_key = False
current_level = 0
score = 0
maze = copy.deepcopy(LEVELS[current_level])

root = tk.Tk()
root.title("Maze Game")
canvas = tk.Canvas(root, width=CELL_SIZE*7, height=CELL_SIZE*7)
canvas.pack()

def draw_maze():
    canvas.delete("all")
    for row_index, row in enumerate(maze):
        for col_index, tile in enumerate(row):
            color = "white"
            if tile == 1:
                color = "black"
            elif tile == "K":
                color = "yellow"
            elif tile == "E":
                color = "green"
            elif tile == "P":
                color = "red"
            canvas.create_rectangle(
                col_index*CELL_SIZE, row_index*CELL_SIZE,
                (col_index+1)*CELL_SIZE, (row_index+1)*CELL_SIZE,
                fill=color
            )
    canvas.create_rectangle(
        player_x*CELL_SIZE, player_y*CELL_SIZE,
        (player_x+1)*CELL_SIZE, (player_y+1)*CELL_SIZE,
        fill="blue"
    )
    canvas.create_text(60, 10, text=f"Level {current_level+1}", font=("Arial", 12))
    canvas.create_text(300, 10, text=f"Score: {score}", font=("Arial", 12), fill="purple")

def game_over_screen():
    canvas.delete("all")
    canvas.create_text(175, 150, text="GAME OVER!", font=("Arial", 30), fill="red")
    canvas.create_text(175, 200, text=f"Score: {score}", font=("Arial", 18), fill="purple")
    restart_button = tk.Button(root, text="Try Again", font=("Arial", 14), command=restart_game)
    canvas.create_window(175, 250, window=restart_button)

def winning_screen():
    canvas.delete("all")
    canvas.create_text(175, 150, text="YOU WON!", font=("Arial", 30), fill="green")
    canvas.create_text(175, 200, text=f"Score: {score}", font=("Arial", 18), fill="purple")
    restart_button = tk.Button(root, text="Play Again", font=("Arial", 14), command=restart_game)
    canvas.create_window(175, 250, window=restart_button)

def restart_game():
    global current_level, maze, player_x, player_y, has_key, score
    current_level = 0
    maze = copy.deepcopy(LEVELS[current_level])
    player_x, player_y = 1, 1
    has_key = False
    score = 0
    draw_maze()

def move_player(event):
    global player_x, player_y, has_key, maze, current_level, score

    new_x, new_y = player_x, player_y
    if event.keysym == "Up": new_y -= 1
    elif event.keysym == "Down": new_y += 1
    elif event.keysym == "Left": new_x -= 1
    elif event.keysym == "Right": new_x += 1

    if 0 <= new_y < len(maze) and 0 <= new_x < len(maze[0]):
        if maze[new_y][new_x] != 1:
            player_x, player_y = new_x, new_y

    current_tile = maze[player_y][player_x]

    if current_tile == "K":
        has_key = True
        maze[player_y][player_x] = 0
        score += 10  # body za kľúč
    elif current_tile == "E":
        if has_key:
            if current_level < len(LEVELS)-1:
                current_level += 1
                maze = copy.deepcopy(LEVELS[current_level])
                player_x, player_y = 1, 1
                has_key = False
            else:
                winning_screen()
                return
        else:
            canvas.create_text(175, 175, text="Find the key!", fill="red", font=("Arial", 18))
    elif current_tile == "P":
        score -= 5  # mínus body za portál
        game_over_screen()
        return

    draw_maze()

draw_maze()
root.bind("<KeyPress>", move_player)
root.focus_set()
root.mainloop()