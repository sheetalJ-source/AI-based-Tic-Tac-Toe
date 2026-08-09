import pygame as pg
from sys import exit
pg.init()

width=700
height=700

win=pg.display.set_mode((width, height))

pg.display.set_caption("Tic Tac Toe")

title_font = pg.font.SysFont("Arial", 55, bold=True)
result_font = pg.font.SysFont("Arial", 40, bold=True)

board = [
    ["", "", ""],
    ["", "", ""],
    ["", "", ""],
]

current_player = "X"

winner = None
game_over = False

def check_winner():

    # Check rows
    for row in range(3):
        if board[row][0] != "" and board[row][0] == board[row][1] == board[row][2]:
            return board[row][0]

    # Check columns
    for col in range(3):
        if board[0][col] != "" and board[0][col] == board[1][col] == board[2][col]:
            return board[0][col]

    # Main diagonal
    if board[0][0] != "" and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]

    # Other diagonal
    if board[0][2] != "" and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]

    return None

def check_draw():

    if check_winner() is not None:
        return False

    for row in board:
        if "" in row:
            return False
    return True  

def restart_game():

    global board
    global current_player
    global winner
    global game_over

    board = [
        ["", "", ""],
        ["", "", ""],
        ["", "", ""],
        ["", "", ""]
    ]

    current_player = "X"
    winner = None
    game_over = False

def is_moves_left():

    for row in range(3):
        for col in range(3):

            if board[row][col] == "":
                return True

    return False

def minimax(depth, is_max):

    winner = check_winner()

    # AI wins
    if winner == "O":
        return 10 - depth

    # Player wins
    if winner == "X":
        return depth - 10

    # Draw
    if not is_moves_left():
        return 0

    # AI's turn (maximize score)
    if is_max:

        best = -1000

        for row in range(3):
            for col in range(3):

                if board[row][col] == "":

                    board[row][col] = "O"

                    score = minimax(depth + 1, False)

                    board[row][col] = ""

                    best = max(best, score)

        return best

    # Player's turn (minimize score)
    else:

        best = 1000

        for row in range(3):
            for col in range(3):

                if board[row][col] == "":

                    board[row][col] = "X"

                    score = minimax(depth + 1, True)

                    board[row][col] = ""

                    best = min(best, score)

        return best
    
def best_move():

    global current_player
    global winner
    global game_over

    best_score = -1000
    move = (-1, -1)
    
    for row in range(3):
        for col in range(3):

            if board[row][col] == "":

                board[row][col] = "O"

                score = minimax(0, False)

                board[row][col] = ""

                if score > best_score:
                    best_score = score
                    move = (row, col)

    row, col = move
    board[row][col] = "O"

    winner = check_winner()

    if winner is not None:
        game_over = True

    elif check_draw():
        winner = "DRAW"
        game_over = True

    else:
        current_player = "X"    

ai_turn = False

while True:

    board_size = 450
    cell = board_size // 3

    board_x = (width - board_size) // 2
    board_y = 170
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r:
                restart_game()    

        if event.type == pg.MOUSEBUTTONDOWN and not game_over:

          mouse_x, mouse_y = pg.mouse.get_pos()

          if board_x <= mouse_x <= board_x + board_size and board_y <= mouse_y <= board_y + board_size:

             row = (mouse_y - board_y) // cell
             col = (mouse_x - board_x) // cell
             
             if board[row][col]=="":
                         board[row][col] = current_player

                         winner = check_winner()
                         print(winner)

                         if winner is not None:
                             game_over = True

                         elif check_draw():
                             winner = "DRAW"
                             game_over = True    

                         else:
                             current_player = "O"

                             ai_turn = True     
                             
            
    win.fill((15, 23, 42))

    tic = title_font.render("TIC", True, (255, 255, 255))
    tac = title_font.render("TAC", True, (90, 110, 255))
    toe = title_font.render("TOE", True, (255, 255, 255))
    tic_rect = tic.get_rect()
    tac_rect = tac.get_rect()
    toe_rect = toe.get_rect()

    tic_rect.topleft = (170, 30)
    tac_rect.topleft = (300, 30)
    toe_rect.topleft = (450, 30)

    win.blit(tic, tic_rect)
    win.blit(tac, tac_rect)
    win.blit(toe, toe_rect)

    board_color = (92, 106, 150)
    board_fill = (36, 49, 78)
    
    board_size = 450
    cell = board_size // 3

    board_x = (width - board_size) // 2
    board_y = 170

    pg.draw.rect(win, board_fill, (board_x, board_y, board_size, board_size), border_radius=20)
    pg.draw.rect( win, board_color, (board_x, board_y, board_size, board_size), width=4, border_radius=20)

    pg.draw.line(win, board_color,(board_x + cell, board_y),(board_x + cell, board_y + board_size), 4)
    pg.draw.line(win,board_color,(board_x + cell * 2, board_y),(board_x + cell * 2, board_y + board_size), 4)
    pg.draw.line(win,board_color,(board_x, board_y + cell),(board_x + board_size, board_y + cell),4)
    pg.draw.line(win,board_color,(board_x, board_y + cell * 2),(board_x + board_size, board_y + cell * 2),4)

    for row in range(3):
        for col in range(3):

            center_x = board_x + col * cell + cell // 2
            center_y = board_y + row * cell + cell // 2

            if board[row][col] == "X":

                offset = 40

                pg.draw.line(win, (255,255,255),(center_x-offset, center_y-offset),(center_x+offset, center_y+offset), 6)

                pg.draw.line(win,(255,255,255),(center_x-offset, center_y+offset),(center_x+offset, center_y-offset), 6)

            elif board[row][col] == "O":

                pg.draw.circle(win,(90,110,255),(center_x, center_y),45, 6)
    
    if game_over:
        if winner == "DRAW":
            text = result_font.render("DRAW! Press R to Restart", True, (255,255,255))
        else:
            text = result_font.render(f"{winner} WINS! Press R to Restart", True, (255,255,255))

        text_rect = text.get_rect(center=(width//2, 640))
        win.blit(text, text_rect)

    if ai_turn and not game_over:
        best_move()
        ai_turn = False
    
    pg.display.update()