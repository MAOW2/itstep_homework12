import tkinter as tk


ROWS = 6
COLUMNS = 7
CELL_SIZE = 80

EMPTY = 0
RED = 1
YELLOW = 2

board = [[EMPTY for _ in range(COLUMNS)] for _ in range(ROWS)]
current_player = RED
game_over = False


def get_color(player):
    if player == RED:
        return "red"
    if player == YELLOW:
        return "yellow"
    return "white"


def draw_board():
    canvas.delete("all")

    for row in range(ROWS):
        for column in range(COLUMNS):
            x1 = column * CELL_SIZE
            y1 = row * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE

            canvas.create_rectangle(x1, y1, x2, y2, fill="blue")

            color = get_color(board[row][column])
            canvas.create_oval(
                x1 + 10,
                y1 + 10,
                x2 - 10,
                y2 - 10,
                fill=color
            )


def find_free_row(column):
    for row in range(ROWS - 1, -1, -1):
        if board[row][column] == EMPTY:
            return row
    return None


def check_winner(player):
    for row in range(ROWS):
        for column in range(COLUMNS - 3):
            if (
                board[row][column] == player and
                board[row][column + 1] == player and
                board[row][column + 2] == player and
                board[row][column + 3] == player
            ):
                return True

    for row in range(ROWS - 3):
        for column in range(COLUMNS):
            if (
                board[row][column] == player and
                board[row + 1][column] == player and
                board[row + 2][column] == player and
                board[row + 3][column] == player
            ):
                return True

    for row in range(ROWS - 3):
        for column in range(COLUMNS - 3):
            if (
                board[row][column] == player and
                board[row + 1][column + 1] == player and
                board[row + 2][column + 2] == player and
                board[row + 3][column + 3] == player
            ):
                return True

    for row in range(3, ROWS):
        for column in range(COLUMNS - 3):
            if (
                board[row][column] == player and
                board[row - 1][column + 1] == player and
                board[row - 2][column + 2] == player and
                board[row - 3][column + 3] == player
            ):
                return True

    return False


def is_board_full():
    for column in range(COLUMNS):
        if board[0][column] == EMPTY:
            return False
    return True


def click(event):
    global current_player, game_over

    if game_over:
        return

    column = event.x // CELL_SIZE

    if column < 0 or column >= COLUMNS:
        return

    row = find_free_row(column)

    if row is None:
        return

    board[row][column] = current_player
    draw_board()

    if check_winner(current_player):
        label.config(text=f"Переміг гравець: {get_color(current_player)}")
        game_over = True
        return

    if is_board_full():
        label.config(text="Нічия")
        game_over = True
        return

    if current_player == RED:
        current_player = YELLOW
    else:
        current_player = RED

    label.config(text=f"Хід гравця: {get_color(current_player)}")


def restart_game():
    global board, current_player, game_over

    board = [[EMPTY for _ in range(COLUMNS)] for _ in range(ROWS)]
    current_player = RED
    game_over = False
    label.config(text="Хід гравця: red")
    draw_board()


window = tk.Tk()
window.title("Connect 4")

label = tk.Label(window, text="Хід гравця: red", font=("Arial", 16))
label.pack()

canvas = tk.Canvas(
    window,
    width=COLUMNS * CELL_SIZE,
    height=ROWS * CELL_SIZE
)
canvas.pack()

button = tk.Button(window, text="Нова гра", command=restart_game)
button.pack()

canvas.bind("<Button-1>", click)

draw_board()
window.mainloop()