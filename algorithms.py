from collections import deque
from copy import deepcopy
from time import sleep

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

class TreeNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visited = False

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

class Algorithm:
    def __init__(self, state: list, goal: list, energy: int, max_height: int):
        self.state = state
        self.goal = goal
        self.energy = energy
        self.max_height = max_height

    def move(self, coords, future_coords, board):
        fi,fj = coords
        si, sj = future_coords
        first_circle_color = board[fi][fj]
        second_circle_color = board[si][sj]

        new_board = board

        if second_circle_color == GREY:
            new_board[si][sj] = first_circle_color
        else:
            new_board[si][sj] = COMPUND_COLORS[(first_circle_color, second_circle_color)]

        new_board[fi][fj] = GREY

        return new_board
    
    def valid_move(self, coords, future_coords, board):
        fi,fj = coords
        si, sj = future_coords

        if si >= self.max_height:
            return False
        
        first_circle_color = board[fi][fj]
        second_circle_color = board[si][sj]

        if second_circle_color != GREY and (first_circle_color, second_circle_color) not in COMPUND_COLORS:
            return False
        
        return first_circle_color != second_circle_color
        
    def next_states(self, board):
        circle_coords = []
        states = []

        for i in range(0, len(board)):
            for j in range(0, len(board[i])):
                if board[i][j] != GREY:
                    circle_coords.append((i,j))

        for circle in circle_coords:
            for possible_move in POSSIBLE_MOVES[circle]:
                if self.valid_move(circle, possible_move, board) == False:
                    continue

                child_state = self.move(circle, possible_move, deepcopy(board))
                states.append(child_state)

        return states
    
    def check_win(self, board):
        for i in range(0, len(self.goal)):
            for j in range(0, len(self.goal[i])):
                if self.goal[i][j] != board[i][j]:
                    return False
        return True

    def BFS(self):
        root = TreeNode(self.state)
        queue = deque([root])
        visited_states = [self.state]

        while queue:
            node = queue.popleft()
            if self.check_win(node.state):
                return node
            
            for state in self.next_states(node.state):
                if state in visited_states:
                    print("entra")
                    continue

                new_node = TreeNode(state, node)
                node.add_child(new_node)
                queue.append(new_node)
                visited_states.append(new_node.state)

        return None
    
    def DFS(self):
        root = TreeNode(self.state)
        stack = deque([root])
        visited_states = [self.state]

        while stack:
            node = stack.pop()

            if self.check_win(node.state):
                return node
        
            for state in self.next_states(node.state):
                if state in visited_states:
                    continue
                
                new_state = TreeNode(state, node)
                node.add_child(new_state)
                stack.append(new_state)
                visited_states.append(state)
        
        return None
    
    def DLS(self):
        root = TreeNode(self.state)
        stack = deque([(root, 0)])
        visited_states = [self.state]

        while stack:
            node, depth = stack.pop()

            if self.check_win(node.state):
                return node

            if depth <= self.energy: 
                for state in self.next_states(node.state):
                    if state not in visited_states:
                        new_state = TreeNode(state, node)
                        node.add_child(new_state)
                        stack.append((new_state, depth+1))

        return None
