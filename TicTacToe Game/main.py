board = [" " for _ in range(9)]
def display_board():
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---|---|---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---|---|---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")

player_1 = input("Choose Between 'X' or 'O': ").upper()
if player_1 not in ['X', 'O']:
    player_1 = input("Invalid choice. Choose Between 'X' or 'O': ").upper()

if player_1 == 'X':
    player_2 = 'O'
else:
    player_2 = 'X'

def check_winner(player):
    win_combos = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6], 
        [1, 4, 7],  
        [2, 5, 8],  
        [0, 4, 8],  
        [2, 4, 6]
    ]
    for combo in win_combos:
      i1 = combo[0]
      i2 = combo[1]
      i3 = combo[2]

      if board[i1] == player:
        if board[i2] == player:
          if board[i3] == player:
            print(f"{player} won. Congratulations") 
            return True
    return False

def game_start():
  current_player = player_1
  for turn in range (9):
    display_board()
    move = int(input(f"Player {current_player}, enter your move (1-9):"))
    index = move-1
    if move < 1 or move > 9:
      print("Invalid Move try again")
    elif board[index] == " ":
      board[index] = current_player
      
      if check_winner(current_player):
        display_board()
        print(f"🎉 Player {current_player} wins! Congratulations!")
        return

      if current_player  == "X":
        current_player = "O" 
      else: 
        current_player = "X"
    else:
      print("That spot is already taken. Try again.")

  display_board()
  print("😅 It's a draw. No winners this time.")

game_start()
