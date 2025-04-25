#########################################
#
#   ISAT 480 - AI - Final Project
#   mancala_board.py
#   Creates class for the state of the board and possible moves
#
#   Authors:
#       Alex Macauley
#       Mason Scofield
#
#########################################

class MancalaBoard:
    """
    Represents the board and logic for the Mancala (Kalah) game.
    
    Attributes:
        board (list): A list of 14 integers representing the game state.
                      Index 0-5: Player 1 pits
                      Index 6:   Player 1's store
                      Index 7-12: Player 2 pits
                      Index 13:  Player 2's store
        current_player (int): The active player (1 or 2)
    """

    def __init__(self):
        """
        Initializes the board with 4 stones in each pit and empty stores.
        Player 1 always starts.
        """
        self.board = [4] * 6 + [0] + [4] * 6 + [0]  # 14 pits total
        self.current_player = 1

    def clone(self):
        """
        Returns a deep copy of the board for use in AI simulations.

        Useful so the AI can simulate moves without affecting the real game.
        """
        new_board = MancalaBoard()
        new_board.board = self.board[:]  # Make a shallow copy of the board list
        new_board.current_player = self.current_player
        return new_board

    def get_legal_moves(self, player):
        """
        Returns a list of pit indices that the player can legally select.

        Args:
            player (int): 1 for Player 1, 2 for Player 2

        Returns:
            list[int]: indices of pits that have stones
        """
        offset = 0 if player == 1 else 7  # Determine where the player's pits begin
        return [i for i in range(offset, offset + 6) if self.board[i] > 0]

    def make_move(self, pit_index):
        """
        Executes a move from the selected pit and applies all game rules.

        Args:
            pit_index (int): index of the pit selected by the current player

        Returns:
            bool: True if move is valid and completed, False if move is invalid
        """
        stones = self.board[pit_index]
        if stones == 0:
            return False  # Can't move from an empty pit

        self.board[pit_index] = 0  # Pick up all stones
        index = pit_index

        # Define which index is the current player's store and which to skip
        player_store = 6 if self.current_player == 1 else 13
        opponent_store = 13 if self.current_player == 1 else 6

        # Distribute stones counter-clockwise
        while stones > 0:
            index = (index + 1) % 14  # Wrap around the board circularly
            if index == opponent_store:
                continue  # Skip the opponent’s store
            self.board[index] += 1
            stones -= 1

        # Check for a capture:
        # If last stone landed in an empty pit on your side
        if self._is_own_pit(index) and self.board[index] == 1:
            opposite = 12 - index  # Pit directly across from index
            if self.board[opposite] > 0:
                # Capture both the last stone and stones from opposite pit
                self.board[player_store] += self.board[opposite] + self.board[index]
                self.board[opposite] = 0
                self.board[index] = 0

        # If last stone was not placed in your store, switch turns
        if index != player_store:
            self.current_player = 2 if self.current_player == 1 else 1

        return True

    def _is_own_pit(self, index):
        """
        Helper to check if a pit belongs to the current player.

        Args:
            index (int): pit index

        Returns:
            bool: True if index is on current player's side
        """
        return (self.current_player == 1 and 0 <= index <= 5) or \
               (self.current_player == 2 and 7 <= index <= 12)

    def is_game_over(self):
        """
        Checks if one side of the board has no stones.

        Returns:
            bool: True if the game is over (one side is empty)
        """
        return all(stone == 0 for stone in self.board[0:6]) or \
               all(stone == 0 for stone in self.board[7:13])

    def collect_remaining(self):
        """
        Moves remaining stones to the respective stores at game end.
        This is called only once after the game ends.
        """
        p1_remaining = sum(self.board[0:6])
        p2_remaining = sum(self.board[7:13])
        self.board[6] += p1_remaining
        self.board[13] += p2_remaining

        # Clear all remaining pits
        for i in range(0, 6):
            self.board[i] = 0
        for i in range(7, 13):
            self.board[i] = 0

    def print_board(self):
        """
        Nicely prints the board in terminal layout.
        Player 2's pits are shown reversed to reflect board layout.
        """
        print(f"P1 side: {self.board[0:6]}      P1 Store: {self.board[6]}")
        print(f"P2 side: {self.board[12:6:-1]}      P2 Store: {self.board[13]}")

    def get_score(self):
        """
        Returns the final score of both players.

        Returns:
            tuple: (player1_score, player2_score)
        """
        return self.board[6], self.board[13]
