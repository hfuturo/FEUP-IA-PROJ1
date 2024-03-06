from typing import Union
from copy import deepcopy
        
GREY: tuple[int, int, int] = (128, 128, 128)          #0
RED: tuple[int, int, int] = (255, 0, 0)               #1
GREEN: tuple[int, int, int] = (0, 255, 0)             #2
BLUE: tuple[int, int, int] = (0, 0, 255)              #3
WHITE: tuple[int, int, int] = (255, 255, 255)         #4    
YELLOW: tuple[int, int, int] = (255, 255, 0)          #5
PINK: tuple[int, int, int] = (255, 0, 255)            #6
AQUA: tuple[int, int, int] = (0, 255, 255)            #7

POSSIBLE_MOVES: dict[tuple[int, int], list[tuple[int, int]]] = {
    (0,0): [(0,1), (1,0), (1,1)],
    (0,1): [(0,0), (0,2), (1,1), (1,2)],
    (0,2): [(0,1), (1,2), (1,3)],
    (1,0): [(0,0), (1,1), (2,0), (2,1)],
    (1,1): [(0,0), (0,1), (1,0), (2,2)],
    (1,2): [(0,1), (0,2), (1,3), (2,2)],
    (1,3): [(0,2), (1,2), (2,3), (2,4)],
    (2,0): [(1,0), (2,1), (3,0)],
    (2,1): [(1,0), (2,0), (2,2), (3,0)],
    (2,2): [(1,1), (1,2), (2,1), (2,3), (3,1), (3,2)],
    (2,3): [(1,3), (2,2), (2,4), (3,3)],
    (2,4): [(1,3), (2,3), (3,3)],
    (3,0): [(2,0), (2,1), (3,1), (4,0)],
    (3,1): [(2,2), (3,0), (4,0), (4,1)],
    (3,2): [(2,2), (3,3), (4,1), (4,2)],
    (3,3): [(2,3), (2,4), (3,2), (4,2)],
    (4,0): [(3,0), (3,1), (4,1)],
    (4,1): [(3,1), (3,2), (4,0), (4,2)],
    (4,2): [(3,2), (3,3), (4,1)]
}

COMPUND_COLORS: dict[tuple[tuple[int, int, int], tuple[int, int, int]], tuple[int, int, int]] = {
    (RED, GREEN): YELLOW,
    (GREEN, RED): YELLOW,
    (RED, BLUE): PINK,
    (BLUE, RED): PINK,
    (GREEN, BLUE): AQUA,
    (BLUE, GREEN): AQUA,
    (RED, AQUA): WHITE,
    (AQUA, RED): WHITE,
    (GREEN, PINK): WHITE,
    (PINK, GREEN): WHITE,
    (BLUE, YELLOW): WHITE,
    (YELLOW, BLUE): WHITE
}

class DropOfLight:
    def __init__(self, board: list, goal: list, energy: int) -> None:
        self.board = deepcopy(board)
        self.goal = goal
        self.energy = energy

        self.first_piece = None
        self.second_piece = None

    def reset(self, board:list, energy:int) -> None:
        self.board = deepcopy(board)
        self.energy = energy
        self.first_piece = None
        self.second_piece = None

    def handle_piece_selected(self, coords: tuple[int, int]) -> Union[tuple[list, int], None]:
        i,j = coords
        if self.first_piece is None and self.board[i][j] == GREY:
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

        if second_piece_color != GREY and (first_piece_color, second_piece_color) not in COMPUND_COLORS:
            return False

        return self.second_piece in POSSIBLE_MOVES.get(self.first_piece) and self.board[fi][fj] != self.board[si][sj]
    
    def move(self) -> None:
        fi, fj = self.first_piece
        si, sj = self.second_piece
        first_piece_color = self.board[fi][fj]
        second_piece_color = self.board[si][sj]

        if second_piece_color == GREY:
            self.board[si][sj] = self.board[fi][fj]
        else:
            self.board[si][sj] = COMPUND_COLORS.get((first_piece_color, second_piece_color))
            
        self.board[fi][fj] = GREY
        self.first_piece = None
        self.second_piece = None
        self.energy -= 1

    def check_win(self) -> bool:
        for i in range(0, len(self.board)):
            for j in range(0, len(self.board[i])):
                if self.board[i][j] != self.goal[i][j]:
                    return False
        return True
        



