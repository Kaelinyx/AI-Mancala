#########################################
#
#   ISAT 480 - AI - Final Project
#   ai_player.py
#   Class that implements the ai player with a/b minimax pruning
#
#   Authors:
#       Alex Macauley
#       Mason Scofield
#
#########################################

from mancala_board import MancalaBoard
import math

class AIPlayer:
    """
    Represents an AI agent using Minimax with Alpha-Beta Pruning to choose moves.

    Attributes:
        player_id (int): 1 for Player 1, 2 for Player 2
        max_depth (int): How far ahead the AI searches
    """

    def __init__(self, player_id, max_depth=6):
        self.player_id = player_id                      # AI's own player number
        self.opponent_id = 2 if player_id == 1 else 1   # Determine the opponent's number
        self.max_depth = max_depth                      # Set the search depth for the tree

    def get_best_move(self, board):
        """
        Determines the best legal move using Minimax with Alpha-Beta pruning.

        Args:
            board (MancalaBoard): Current board state

        Returns:
            int: Best pit index for AI to play
        """
        best_score = -math.inf  # Start with worst possible score
        best_move = None

        # Try every possible legal move
        for move in board.get_legal_moves(self.player_id):
            cloned_board = board.clone()        # Simulate the move on a cloned board
            cloned_board.make_move(move)        # Apply the move

            # Recursively evaluate the move using Minimax
            score = self._minimax(
                cloned_board,
                self.max_depth - 1,  # Reduce depth
                False,               
                -math.inf, math.inf  # Start with full range for alpha and beta
            )

            # Keep track of the move that gave the highest score
            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def _minimax(self, board, depth, is_maximizing, alpha, beta):
        """
        Recursive Minimax function with Alpha-Beta pruning.

        Args:
            board (MancalaBoard): Current board state
            depth (int): How many layers deep to search
            is_maximizing (bool): True if it's AI's turn, False for opponent
            alpha (float): Best score the maximizer (AI) can guarantee
            beta (float): Best score the minimizer (opponent) can guarantee

        Returns:
            float: Heuristic score from this game state
        """
        # Base case: reached max depth or game is over
        if depth == 0 or board.is_game_over():
            return self._evaluate_board(board)

        current_player = self.player_id if is_maximizing else self.opponent_id
        legal_moves = board.get_legal_moves(current_player)

        if is_maximizing:
            max_eval = -math.inf
            for move in legal_moves:
                next_board = board.clone()
                extra_turn = next_board.make_move(move)

                # If the move gave another turn, keep the same player
                next_is_max = is_maximizing if extra_turn else False

                eval = self._minimax(next_board, depth - 1, next_is_max, alpha, beta)

                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)

                # Prune if we find a path that is worse than what the opponent would allow
                if beta <= alpha:
                    break

            return max_eval

        else:
            min_eval = math.inf
            for move in legal_moves:
                next_board = board.clone()
                extra_turn = next_board.make_move(move)

                # If opponent gets another turn, still minimizing
                next_is_min = is_maximizing if extra_turn else True

                eval = self._minimax(next_board, depth - 1, next_is_min, alpha, beta)

                min_eval = min(min_eval, eval)
                beta = min(beta, eval)

                # Prune if this branch can't affect the result
                if beta <= alpha:
                    break

            return min_eval

    def _evaluate_board(self, board):
        """
        Heuristic to evaluate the value of the board from AI's perspective.

        Args:
            board (MancalaBoard): Current board state

        Returns:
            int: score = AI's store - opponent's store
        """
        p1_score, p2_score = board.get_score()

        # Score difference depends on which player the AI is
        if self.player_id == 1:
            return p1_score - p2_score
        else:
            return p2_score - p1_score
