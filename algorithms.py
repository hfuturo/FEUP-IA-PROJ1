from collections import deque
from copy import deepcopy
import game_info

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

        if second_circle_color == game_info.GREY:
            new_board[si][sj] = first_circle_color
        else:
            new_board[si][sj] = game_info.COMPUND_COLORS[(first_circle_color, second_circle_color)]

        new_board[fi][fj] = game_info.GREY

        return new_board
    
    def valid_move(self, coords, future_coords, board):
        fi,fj = coords
        si, sj = future_coords

        if si >= self.max_height:
            return False
        
        first_circle_color = board[fi][fj]
        second_circle_color = board[si][sj]

        if second_circle_color != game_info.GREY and (first_circle_color, second_circle_color) not in game_info.COMPUND_COLORS:
            return False
        
        return first_circle_color != second_circle_color
        
    def next_states(self, board):
        circle_coords = []
        states = []

        for i in range(0, len(board)):
            for j in range(0, len(board[i])):
                if board[i][j] != game_info.GREY:
                    circle_coords.append((i,j))

        for circle in circle_coords:
            for possible_move in game_info.POSSIBLE_MOVES[circle]:
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
