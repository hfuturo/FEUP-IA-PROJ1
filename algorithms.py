from __future__ import annotations
from collections import deque
from time import sleep
from copy import deepcopy
from typing import Union
import game_info

class TreeNode:
    """
        Classe que contem informacao um estado utilizada pelos algoritmos.
    """

    def __init__(self, state: list, parent:TreeNode = None) -> None:
        """
            Cria um elemento da classe TreeNode
        """

        self.state = state
        self.parent = parent
        self.children = []
        self.visited = False

    def add_child(self, child:TreeNode ) -> None:
        """
            Adiciona um filho
        """

        self.children.append(child)
        child.parent = self

class Algorithm:
    """
        Classe onde se encontram os algoritmos
    """

    def __init__(self, state: list, goal: list, energy: int, max_height: int) -> None:
        """
            Cria um elemento da class Algorithm
        """

        self.state = state
        self.goal = goal
        self.energy = energy
        self.max_height = max_height

        self.has_compound_colors = self.check_compound_colors()
        self.has_primary_colors = self.check_primary_colors()
        self.goal_board_info = self.get_board_info(self.goal)

    def get_board_info(self, board: list) -> dict:
        """
            Obtém toda a informação relevante do tabuleiro.

            Retorna um dicionário onde as chaves são as cores e os valores uma
            lista com as posições das peças no tabuleiro.
        """

        info = {}

        for i in range(0, len(board)):
            for j in range(0, len(board[i])):
                piece = board[i][j]

                if piece == game_info.GREY:
                    continue

                if piece not in info:
                    info[piece] = [(i,j)]
                else:
                    l = info[piece]
                    info.update({piece: l + [(i,j)]})

        return info

    def check_primary_colors(self) -> bool:
        """
            Verifica se o tabuleiro/estado do objetivo possui alguma cor primária
        """

        for row in self.goal:
            for color in row:
                if color == game_info.RED or color == game_info.GREEN or color == game_info.BLUE:
                    return True
        return False

    def check_compound_colors(self) -> bool:
        """
            Verifica se existe alguma cor composta no tabuleiro/estado atual
        """
        
        for i in range(0, len(self.state)):
            for j in range(0, len(self.state[i])):
                for (_,v) in game_info.COMPUND_COLORS.items():
                    if self.goal[i][j] == v:
                        return True
        return False

    def move(self, coords: tuple[int, int], future_coords: tuple[int, int], board: list) -> list:
        """
            Realiza uma jogada no tabuleiro movimentando as peças
        """
        
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
    
    def valid_move(self, coords: tuple[int, int], future_coords: tuple[int, int], board: list) -> bool:
        """
            Verifica se a jogada pretendida é uma jogada válida
        """
        
        fi,fj = coords
        si, sj = future_coords

        if si >= self.max_height:
            return False
        
        first_circle_color = board[fi][fj]
        second_circle_color = board[si][sj]

        if second_circle_color != game_info.GREY and (first_circle_color, second_circle_color) not in game_info.COMPUND_COLORS:
            return False
        
        return first_circle_color != second_circle_color
        
    def next_states(self, board: list) -> list:
        """
            Obtém todos os estados/tabuleiros possíveis a partir do tabuleiro fornecido.
        """
        
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
    
    def check_win(self, board: list) -> bool:
        """
            Verifica se a condição de vitória foi alcançada
        """
        
        for i in range(0, len(self.goal)):
            for j in range(0, len(self.goal[i])):
                if self.goal[i][j] != board[i][j]:
                    return False
        return True

    def BFS(self) -> Union[TreeNode, None]:
        """
            Executa o algoritmo Breadth-First Search (BFS)
        """

        root = TreeNode(self.state)
        queue = deque([root])
        visited_states = [self.state]

        while queue:
            node = queue.popleft()
            if self.check_win(node.state):
                return node
            
            for state in self.next_states(node.state):
                if state in visited_states:
                    continue

                new_node = TreeNode(state, node)
                node.add_child(new_node)
                queue.append(new_node)
                visited_states.append(new_node.state)

        return None
    
    def DFS(self) -> Union[TreeNode, None]:
        """
            Executa o algoritmo Depth-First Search
        """

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

    def get_colors_by_compound(self, compound_color: tuple[int, int, int], board_info: dict) -> list:
        """
            Retorna uma lista com as cores necessárias que se encontram no tabuleiro para criar uma cor composta.
        """

        # ambas as cores encontram-se no tabuleiro
        for (k,v) in game_info.COMPUND_COLORS.items():
            if compound_color == v:
                if k[0] in board_info and len(board_info[k[0]]) > 0 and k[1] in board_info and len(board_info[k[1]]) > 0:
                    return [k[0], k[1]]
        
        # Edge case: obter branco mas no tabuleiro temos apenas cores primarias.
        # Necessário criar uma cor compound e depois junta-la a uma cor primaria.
        for (k,v) in game_info.COMPUND_COLORS.items():
            if compound_color == v:
                if k[0] in board_info and len(board_info[k[0]]) > 0:
                    l = self.get_colors_by_compound(k[1], deepcopy(board_info))
                    if l != []:
                        return [k[0]] + l
                    
                if k[1] in board_info and len(board_info[k[1]]) > 0:
                    l = self.get_colors_by_compound(k[0], deepcopy(board_info))
                    if l != []:
                        return [k[1]] + l
        return []

    def manhattan(self, piece1: tuple[int, int], piece2: tuple[int, int]) -> int:
        """
            Obtém a distânica de Manhattan entre dois pontos.
        """
        
        x1, y1 = piece1
        x2, y2 = piece2

        return abs(x1-x2) + abs(y1-y2)
    
    def find_best_move(self, c1: tuple[int, int, int], c2: tuple[int, int, int], board_info: dict, goal_info: dict, remove_color_from_goal:bool = True) -> int:
        """
            Encontra a cor que vai percorrer uma menor distância para chegar a outra cor.
        """
        
        min_distance = 10000000000000
        p1_coord = []
        p2_coord = []

        for p1 in board_info[c1]:
            for p2 in goal_info[c2]:
                distance = self.manhattan(p1, p2)
                if distance < min_distance:
                    min_distance = distance
                    p1_coord.clear()
                    p2_coord.clear()
                    p1_coord.append(p1)
                    p2_coord.append(p2)

        l = board_info[c1]
        l.remove(p1_coord.pop())
        board_info.update( {c1: l })

        if remove_color_from_goal:
            l = goal_info[c2]
            l.remove(p2_coord.pop())
            goal_info.update( {c2: l })

        return min_distance

    def heuristic2(self, board: list) -> int:
        """
            Heurística utilizada no algoritmo A*.

            Esta heuristica vai calcular a soma das distâncias das cores atuais à posição da cor no tabuleiro final.
            Esta heuristica não continua a explorar uma node que tenha cores compostas se o estado final não tem cores compostas
            e também não explora uma node que não tem cores primárias se o estado final tiver cores primárias.

            Para evitar criar cores compostas desnecessárias, primeiro calculmos a distância de nodes da mesma cor que se encontram
            na node atual e na node final. De seguida, calculamos a distância para as cores que necessitam de serem juntadas para formar
            uma cor compound (exceto branco). Por último, calculamos a distância para as cores que necessitam de serem juntadas para formar
            branco.
        """

        total = 0
        board_info = self.get_board_info(board)
        goal_info = deepcopy(self.goal_board_info)

        # se goal nao tem compound e board atual tem compound nunca explora esta node
        if not self.has_compound_colors:
            for key in board_info:
                for (_,v) in game_info.COMPUND_COLORS.items():
                    if key == v:
                        return 10000000000000
        

        # se goal tem cor primaria e board atual nao tem cor primaria nunca explora esta node
        found = False
        if self.has_primary_colors:
            for row in board:
                for color in row:
                    if color == game_info.RED or color == game_info.GREEN or color == game_info.BLUE:
                        found = True
                        break
            
            if not found:
                return 10000000000000

        # calcula primeiro a distancia das cores que existem nas duas boards.
        # Se uma cor nao existir numa board, significa que é uma cor compund
        for key in goal_info:
            if key in board_info:
                while len(goal_info[key]):
                    min_distance = self.find_best_move(key, key, board_info, goal_info)
                    total += min_distance
                    

        # compound color
        for key in goal_info:
            if key == game_info.WHITE:
                continue

            while len(goal_info[key]):
                colors = self.get_colors_by_compound(key, deepcopy(board_info))

                min_distance = self.find_best_move(colors[0], key, board_info, goal_info, False)
                total += min_distance
                min_distance = self.find_best_move(colors[1], key, board_info, goal_info)
                total += min_distance


        # white
        for key in goal_info:
            while len(goal_info[key]):
                colors = self.get_colors_by_compound(key, deepcopy(board_info))

                for i in range(0, len(colors)):
                    min_distance = self.find_best_move(colors[i], key, board_info, goal_info, False if i < (len(colors)-1) else True)
                    total += min_distance

        return total

    def heuristic1(self, board: list) -> int:
        """
            Obtém o número de peças fora do sitio em relação ao tabuleiro final e a diferença entre cores compostas
            entre o tabuleiro atual e o tabuleiro final.
        """

        total = 0
        compound_c1 = 0
        compound_c2 = 0

        # peças fora do sitio
        for i in range(0, len(board)):
            for j in range(0, len(board[i])):
                c1 = board[i][j]
                c2 = self.goal[i][j]

                if c1 != game_info.RED and c1 != game_info.GREEN and c1 != game_info.BLUE:
                    compound_c1 += 1

                if c2 != game_info.RED and c2 != game_info.GREEN and c2 != game_info.BLUE:
                    compound_c2 += 1

                if board[i][j] != self.goal[i][j]:
                    total += 1

        total += abs(compound_c2 - compound_c1)

        return total
    
    def get_depth(self, node: TreeNode) -> int:
        """
            Obtém a distância desta node à node do problema inicial.
        """
        
        total = 0

        while node:
            total += 1
            node = node.parent

        return total - 1

    def greedy(self, best_heuristic:bool = True) -> Union[TreeNode, None]:
        """
            Executa o algoritmo greedy com a melhor heuristica por default.
        """
        return self.run_informed_algorithm(self.heuristic2 if best_heuristic else self.heuristic1, lambda _: 0)

    def AStar(self, best_heuristic:bool = True) -> Union[TreeNode, None]:
        """
            Executa o algoritmo A* com a melhor heuristica por default.
        """
        return self.run_informed_algorithm(self.heuristic2 if best_heuristic else self.heuristic1, self.get_depth)
    
    def WeightedAStar(self, best_heuristic:bool = True) -> Union[TreeNode, None]:
        """
            Executa o algoritmo Weighted AStar
        """
        f = lambda x : (self.heuristic2(x) if best_heuristic else self.heuristic1(x)) * 2
        return self.run_informed_algorithm(f, self.get_depth)
    
    def run_informed_algorithm(self, heuristic1: function, heuristic2: function) -> Union[TreeNode, None]:
        """
            Corre a parte "pesada" do algoritmo
        """

        root = TreeNode(self.state)
        nodes_to_visit = [(root, heuristic1(self.state) + heuristic2(root))]
        visited_states = [self.state]

        while nodes_to_visit:

            node, _ = nodes_to_visit.pop()
            if self.check_win(node.state):
                return node
            
            for state in self.next_states(node.state):
                if state not in visited_states:
                    new_state = TreeNode(state, node)
                    node.add_child(new_state)
                    visited_states.append(new_state.state)
                    nodes_to_visit.append((new_state, heuristic1(new_state.state) + heuristic2(new_state)))
            
            nodes_to_visit = sorted(nodes_to_visit, key= lambda x: x[1], reverse=True)