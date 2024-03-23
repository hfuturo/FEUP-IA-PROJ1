from typing import Union
from copy import deepcopy
import game_info
        
class DropOfLight:
    def __init__(self, board: list, goal: list, energy: int, max_height: int) -> None:
        self.board = deepcopy(board)
        self.goal = goal
        self.energy = energy
        self.max_height = max_height

        self.first_piece = None
        self.second_piece = None

    def reset(self, board:list, energy:int) -> None:
        self.board = deepcopy(board)
        self.energy = energy
        self.first_piece = None
        self.second_piece = None

    def handle_piece_selected(self, coords: tuple[int, int]) -> Union[tuple[list, int], None]:
        i,j = coords
        if self.first_piece is None and self.board[i][j] == game_info.GREY:
            return None

        if self.first_piece is None:
            self.first_piece = coords
            return None
        
        if self.first_piece == coords:
            self.first_piece = None
            return None
        
        if self.second_piece is None:
            fi, fj = self.first_piece
            if self.board[fi][fj] == self.board[i][j]:
                return None
            self.second_piece = coords
        
        if not self.check_move():
            self.second_piece = None
            return None

        self.move()
        
        if self.check_win():
            return [], self.energy
        if self.energy == 0:
            return deepcopy(self.board), 0
        
        return deepcopy(self.board), self.energy
        

    def check_move(self) -> bool:
        fi, fj = self.first_piece
        si, sj = self.second_piece
        first_piece_color = self.board[fi][fj]
        second_piece_color = self.board[si][sj]

        if second_piece_color != game_info.GREY and (first_piece_color, second_piece_color) not in game_info.COMPUND_COLORS:
            return False

        return self.second_piece in game_info.POSSIBLE_MOVES.get(self.first_piece) and self.board[fi][fj] != self.board[si][sj]
    
    def move(self) -> None:
        fi, fj = self.first_piece
        si, sj = self.second_piece
        first_piece_color = self.board[fi][fj]
        second_piece_color = self.board[si][sj]

        if second_piece_color == game_info.GREY:
            self.board[si][sj] = self.board[fi][fj]
        else:
            self.board[si][sj] = game_info.COMPUND_COLORS.get((first_piece_color, second_piece_color))
            
        self.board[fi][fj] = game_info.GREY
        self.first_piece = None
        self.second_piece = None
        self.energy -= 1

    def check_win(self) -> bool:
        for i in range(0, len(self.board)):
            for j in range(0, len(self.board[i])):
                if self.board[i][j] != self.goal[i][j]:
                    return False
        return True
        



