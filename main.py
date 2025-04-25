#########################################
#
#   ISAT 480 - AI - Final Project
#   main.py
#   Main script that simulates a game and performs moves
#
#   Authors:
#       Alex Macauley
#       Mason Scofield
#
#########################################

from mancala_board import MancalaBoard
from ai_player import AIPlayer

def main():
    """
    Entry point for the Mancala game. Prompts user to choose between
    AI vs Player and AI vs AI modes, then starts the appropriate game.
    """

    print("Welcome to Mancala!")
    print("Select game mode:")
    print("1 - Play against AI (You are Player 1)")
    print("2 - Watch AI vs AI")

    mode = input("Enter 1 or 2: ").strip()
    while mode not in ["1", "2"]:
        mode = input("Invalid input. Enter 1 or 2: ").strip()

    game = MancalaBoard()

    # Create AI agents
    ai1 = AIPlayer(player_id=1, max_depth=6)
    ai2 = AIPlayer(player_id=2, max_depth=6)

    # Game loop starts here
    while not game.is_game_over():
        game.print_board()

        if mode == "1":
            # PLAYER vs AI Mode
            if game.current_player == 1:
                # Human move
                print("\nYour turn (Player 1)")
                legal_moves = game.get_legal_moves(1)
                print("Legal moves:", legal_moves)

                move = -1
                while move not in legal_moves:
                    try:
                        move = int(input("Choose a pit index to move from (0–5): "))
                    except ValueError:
                        continue
            else:
                # AI move
                print("\nAI's turn (Player 2)...")
                move = ai2.get_best_move(game)
                print(f"AI chose pit: {move}")

        else:
            # AI vs AI Mode
            print(f"\nAI Player {game.current_player}'s turn...")
            current_ai = ai1 if game.current_player == 1 else ai2
            move = current_ai.get_best_move(game)
            print(f"AI {game.current_player} chose pit: {move}")

        # Apply the chosen move
        game.make_move(move)

    # Game has ended
    print("\nGame over!")
    game.collect_remaining()
    game.print_board()

    p1_score, p2_score = game.get_score()
    print(f"\nFinal Score — Player 1: {p1_score} | Player 2: {p2_score}")

    if p1_score > p2_score:
        print("Player 1 wins!")
    elif p2_score > p1_score:
        print("Player 2 wins!")
    else:
        print("It's a tie!")

if __name__ == "__main__":
    main()
