from Engine.piece import Piece
import numpy as np
# from collections import deque

class Board:
    king = float("inf")
    pawn = 1
    advisor = 2
    elephant = 2
    horse = 4
    cannon = 4.5
    rook = 10
    values = (king, elephant, advisor, cannon, pawn, rook, horse)

    def __init__(self, FEN: str, play_as_red: int, red_moves_first=True) -> None:
        self.moving_side = play_as_red and red_moves_first
        self.opponent_side = 1 - self.moving_side

        # If we don't play as red, the pieces are at the top, 
        self.is_red_up = not play_as_red
        # moving color is 16 if red moves first or 8 when white moves first
        self.moving_color = (1 + red_moves_first) * 8
        self.opponent_color = (2 - red_moves_first) * 8

        # Square-centric board repr
        self.squares = list(np.zeros(90, dtype=np.int8))
        # This keeps track of all game states in history, 
        # so multiple moves can be reversed consecutively, coming in really handy in dfs
        self.game_history = [] # Stack(: previous square, :target square :captured piece)

        # To keep track of the pieces' indices (Piece-centric repr)
        # Piece list at index 0 keeps track of pieces at the top, index 1 for bottom
        self.piece_lists = [[set() for _ in range(7)] for _ in range(2)]
        # DON'T EVER DO THIS IT TOOK ME AN HOUR TO FIX self.piece_list = [[set()] * 7] * 2 
        self.load_board_from_fen(FEN)


    @staticmethod
    def get_board_pos(mouse_pos, unit) -> tuple:
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        rank = int((mouse_y) // unit)
        file = int((mouse_x) // unit)
        rank = min(9, max(rank, 0))
        file = min(8, max(file, 0))
        return file, rank

    def switch_moving_side(self):
        self.opponent_side = self.moving_side
        self.moving_side = 1 - self.moving_side
        _ = self.moving_color
        self.moving_color= self.opponent_color
        self.opponent_color = _
        # if self.moving_side:
        #     print("RED MOVES")
        #     return
        # print("WHITE MOVES")

    def load_board_from_fen(self, FEN: str) -> None:
        """
        Loads a board from Forsyth-Edwards-Notation (FEN)
        Black: upper case
        Red: lower case
        King:K, Advisor:A, Elephant:E, Rook:R, Cannon:C, Horse:H, Pawn:P
        """
        file, rank = 0, 0
        for char in FEN:
            if char == "/":
                rank += 1
                file = 0
            if char.lower() in Piece.letters:
                is_red = char.isupper()
                piece_type = Piece.letters.index(char.lower())
                # If red is playing the top side
                self.piece_lists[is_red - self.is_red_up][piece_type].add(rank * 9 + file)
                self.squares[rank * 9 + file] = (is_red + 1) * 8 + piece_type
                file += 1
            if char.isdigit():
                file += int(char)

    def load_fen_from_board(self) -> str:
        """
        :return: a Forsyth-Edwards-Notation (FEN) string from the current board
        """
        fen = ""
        empty_files_in_rank = 0
        for i, piece in enumerate(self.squares):
            if not piece:
                empty_files_in_rank += 1
            else:
                if empty_files_in_rank:
                    fen += str(empty_files_in_rank)
                    empty_files_in_rank = 0
                is_red = Piece.is_color(piece, Piece.red)
                piece_type = Piece.get_type(piece)
                letter = Piece.letters[is_red * 7 + piece_type]
                fen += letter
            rank = i // 9
            file = i % 9
            if rank < 9 and file == 8 and empty_files_in_rank != 9:
                fen += "/"
                empty_files_in_rank = 0
            elif empty_files_in_rank == 9:
                fen += "9/"
                empty_files_in_rank = 0
        return fen

    @staticmethod
    def get_file_and_rank(square):
        return square % 9, square // 9

    def get_piece_list(self, color_idx, piece_type: int):
        return self.piece_lists[color_idx][piece_type]
    
    def is_capture(self, square):
        return self.squares[square]

    @staticmethod
    def get_horse_block(current_square, target_square):
        d_rank = target_square // 9 - current_square // 9
        d_file = target_square % 9 - current_square % 9

        if abs(d_rank) > abs(d_file):
            return current_square + d_rank // 2 * 9
        return current_square + d_file // 2
   

    def make_move(self, move):
        previous_square, moved_to = move
        moved_piece = self.squares[previous_square]
        piece_type = Piece.get_type(moved_piece)
        # Updating piece lists
        self.piece_lists[self.moving_side][piece_type].remove(previous_square)
        self.piece_lists[self.moving_side][piece_type].add(moved_to)
        
        captured_piece = self.squares[moved_to]
        if captured_piece:
            captured_type = Piece.get_type(captured_piece)
            self.piece_lists[self.opponent_side][captured_type].remove(moved_to)

        # Adding current game state to history
        current_game_state = (previous_square, moved_to, captured_piece)
        self.game_history.append(current_game_state)
        # Updating the board
        self.squares[moved_to] = moved_piece
        self.squares[previous_square] = 0
        self.switch_moving_side()
        # print(self.load_fen_from_board())

        # Used for quiescene search
        return bool(captured_piece)
        
    def reverse_move(self):
        if not len(self.game_history):
            return
        # Accessing the previous game state data
        previous_square, moved_to, captured_piece = self.game_history.pop()

        moved_piece = self.squares[moved_to]
        is_red = Piece.is_color(moved_piece, Piece.red)
        piece_type = Piece.get_type(moved_piece)

        # Reversing the move
        self.piece_lists[is_red][piece_type].remove(moved_to)  
        self.piece_lists[is_red][piece_type].add(previous_square)

        if captured_piece:
            captured_type = captured_piece[1]
            self.piece_lists[1 - is_red][captured_type].add(moved_to)

        self.squares[previous_square] = moved_piece
        self.squares[moved_to] = captured_piece

        # Switch back to previous moving color
        self.switch_moving_side()


    def get_move_notation(self, move):
        former_square, new_square = move
        former_rank, former_file = self.get_file_and_rank(former_square)
        new_rank, new_file = self.get_file_and_rank(new_square)
        piece = self.squares[former_square]
        is_red = Piece.is_color(piece, Piece.red)
        piece_type = Piece.get_type(piece)
        letter = Piece.letters[is_red * 7 + piece_type]
        return (f"{letter}({former_rank}{former_file})-{new_rank}{new_file}")


    def shef(self):
        """
        Standard Heuristic Evaluation Function: \n
        :return: a heuristic evaluation of current material on board relative to moving color.
        positive: good
        negative: bad
        """
        friendly_eval = self.static_material_eval(self.moving_side)
        opponent_eval = self.static_material_eval(self.opponent_color)
        return friendly_eval - opponent_eval
    
    def static_material_eval(self, color):
        material = 0
        for piece_id in range(1, 7):
            material += len(self.piece_lists[color][piece_id]) * self.values[piece_id]
        return material