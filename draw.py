import pygame
import algorithms
import drop_of_light as dol
import game_info
from typing import Union
from copy import deepcopy
from time import sleep, time

WIDTH: int = 800
HEIGHT: int = 600
TITLE_HEIGHT: int = 100

class Draw:
    """
        Classe que possui funções comuns a todas as funções que desenham.
    """

    def __init__(self) -> None:
        """
            Cria um elemento da classe Draw
        """

        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])

        self.title_font = pygame.font.SysFont("Arial", 45)
        self.normal_font = pygame.font.SysFont("Arial", 30)

        pygame.display.set_caption("Drop of Light")

    def draw_text(self, text: str, width: int, height: int, font:str = "normal", color:tuple[int, int, int] = game_info.WHITE) -> pygame.Rect:
        """
            Desenha texto no ecrã
        """

        if font == "normal":
            f = self.normal_font
        else:
            f = self.title_font

        text_surface = f.render(text, True, color)
        text_rect = text_surface.get_rect(center=(width,height))
        self.screen.blit(text_surface, text_rect)

        return text_rect

    def update_screen(self) -> None:
        """
            Dá update ao ecrã
        """
        pygame.display.flip()

        
class MainMenu(Draw):
    """
        Classe que possui funções e lógica do menu principal.
    """

    def __init__(self) -> None:
        """
            Cria um elemento da classe MainMenu.
        """
        
        super().__init__()

        self.draw_main_menu()

        self.update_screen()

    def draw_main_menu(self) -> None:
        """
            Desenha o menu principal.
        """
        
        self.screen.fill(game_info.BLACK)

        self.draw_text("Drop of Light", WIDTH//2, TITLE_HEIGHT, "titulo")

        self.new_game = self.draw_text("New game", WIDTH//2, HEIGHT//2 - 60)
        self.rules =  self.draw_text("Rules", WIDTH//2, HEIGHT//2 - 10)
        self.quit = self.draw_text("Quit", WIDTH//2, HEIGHT//2 + 40)
    
    def run(self) -> Union[list, None]:
        """
            Gere a lógica do menu principal.
        """
        
        while True:
            for event in pygame.event.get():
                if self.leave(event):
                    pygame.quit()
                    return None

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.rules.collidepoint(event.pos):
                        self.draw_rules()
                        self.draw_main_menu()
                        self.update_screen()

                    if self.new_game.collidepoint(event.pos):
                        level = self.draw_level_menu()
                        if type(level) == list and len(level) == 0:
                            self.draw_main_menu()
                            self.update_screen()
                            break
                        return level
                    

    def leave(self, event: pygame.event) -> bool:
        """
            Verifica se user quer sair da aplicação.
        """

        return event.type == pygame.QUIT or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.quit.collidepoint(event.pos))
    
    def draw_rules(self) -> None:
        """
            Desenha as regras e dá "handle" à lógica.
        """

        i = 0

        while i < len(game_info.RULES_TEXT):
            previous_rule = next_rule = None  
            self.screen.fill(game_info.BLACK)
            self.draw_text("Rules", WIDTH//2, TITLE_HEIGHT, "titulo")

            for (rule, index) in zip(game_info.RULES_TEXT[i], range(0, len(game_info.RULES_TEXT[i]))):
                self.draw_text(rule, WIDTH//2, HEIGHT//2 - 120 + (50 * index))

            if i == 2:
                self.draw_rule_example()

            if i != 0:
                previous_rule = self.draw_text("Previous rule", WIDTH//5, HEIGHT - 50)
            main_menu = self.draw_text("Main Menu", WIDTH//2, HEIGHT - 50)
            if i != len(game_info.RULES_TEXT)-1:
                next_rule = self.draw_text("Next rule", WIDTH - (WIDTH//5) , HEIGHT - 50)

            self.update_screen()

            run = True
            while run:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        run = False
                        return

                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if previous_rule is not None and previous_rule.collidepoint(event.pos):
                            i -= 2
                            run = False
                            break
                        if next_rule is not None and next_rule.collidepoint(event.pos):
                            run = False
                            break
                        if main_menu.collidepoint(event.pos):
                            return
            i = max(0, i+1)

    def draw_rule_example(self) -> None:
        """
            Desenha o exemplo das cores compostas que se encontra nas regras
        """
        
        self.draw_rule_line(game_info.RED, game_info.GREEN, game_info.YELLOW, 0)
        self.draw_rule_line(game_info.RED, game_info.BLUE, game_info.PINK, 50)
        self.draw_rule_line(game_info.GREEN, game_info.BLUE, game_info.AQUA, 100)
        self.draw_rule_line(game_info.RED, game_info.GREEN, game_info.WHITE, 150, 47.5)

    def draw_rule_line(self, color1: tuple[int, int, int], color2: tuple[int, int, int], color3: tuple[int, int, int], paddingY: int, paddingX: int = 0) -> None:
        """
            Desenha uma linha do exemplo das cores compostas que se encontra nas regras
        """
        
        pygame.draw.circle(self.screen, color1, (WIDTH // 2 - 95 - paddingX, HEIGHT // 2 + 40 + paddingY), 20) # 1º circulo
        pygame.draw.line(self.screen, game_info.LIGHTGREY, (WIDTH // 2 - 60 - paddingX, HEIGHT // 2 + 40 + paddingY), (WIDTH // 2 - 35 - paddingX, HEIGHT // 2 + 40 + paddingY), 5) # -
        pygame.draw.line(self.screen, game_info.LIGHTGREY, (WIDTH // 2 - 47.5 - paddingX, HEIGHT // 2 + 52.5 + paddingY), (WIDTH // 2 - 47.5 - paddingX, HEIGHT // 2 + 27.5 + paddingY), 5) # |
        pygame.draw.circle(self.screen, color2, (WIDTH // 2 - paddingX, HEIGHT // 2 + 40 + paddingY), 20) # 2º circulo
        if paddingX != 0:
            pygame.draw.line(self.screen, game_info.LIGHTGREY, (WIDTH // 2 - 60 + paddingX, HEIGHT // 2 + 40 + paddingY), (WIDTH // 2 - 35 + paddingX, HEIGHT // 2 + 40 + paddingY), 5) # -
            pygame.draw.line(self.screen, game_info.LIGHTGREY, (WIDTH // 2 - 47.5 + paddingX, HEIGHT // 2 + 52.5 + paddingY), (WIDTH // 2 - 47.5 + paddingX, HEIGHT // 2 + 27.5 + paddingY), 5) # |
            pygame.draw.circle(self.screen, game_info.BLUE, (WIDTH // 2 + paddingX, HEIGHT // 2 + 40 + paddingY), 20) # 3º circulo
        pygame.draw.line(self.screen, game_info.LIGHTGREY, (WIDTH // 2 + 35 + paddingX, HEIGHT // 2 + 35 + paddingY), (WIDTH // 2 + 60 + paddingX, HEIGHT // 2 + 35 + paddingY), 5) # resultado linha de cima
        pygame.draw.line(self.screen, game_info.LIGHTGREY, (WIDTH // 2 + 35 + paddingX, HEIGHT // 2 + 45 + paddingY), (WIDTH // 2 + 60 + paddingX, HEIGHT // 2 + 45 + paddingY), 5) # resultado linha de baixo
        pygame.draw.circle(self.screen, color3, (WIDTH // 2 + 95 + paddingX, HEIGHT // 2 + 40 + paddingY), 20) # ultimo circulo 

    def draw_level_menu(self) -> Union[list, None]:
        """
            Desenha o menu de seleção dos níveis e dá "handle" à lógica.
        """
        
        self.screen.fill(game_info.BLACK)

        self.draw_text("Choose a level", WIDTH//2, TITLE_HEIGHT, "titulo")
        level1 = self.draw_text("Level 1", WIDTH//2, HEIGHT//2 - 60)
        level2 = self.draw_text("Level 2", WIDTH//2, HEIGHT//2 - 10)
        level3 = self.draw_text("Level 3", WIDTH//2, HEIGHT//2 + 40)
        level4 = self.draw_text("Level 4", WIDTH//2, HEIGHT//2 + 90)
        main_menu = self.draw_text("Main Menu", WIDTH//2, HEIGHT - 50)

        self.update_screen()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if main_menu.collidepoint(event.pos):
                        return []

                    if level1.collidepoint(event.pos):
                        ret = self.select_game_mode()
                        if ret == -1:
                            return self.draw_level_menu()
                        return None if ret is None else [game_info.LEVEL1, ret]

                    if level2.collidepoint(event.pos):
                        ret = self.select_game_mode()
                        if ret == -1: 
                            return self.draw_level_menu()
                        return None if ret is None else [game_info.LEVEL2, ret]

                    if level3.collidepoint(event.pos):
                        ret = self.select_game_mode()
                        if ret == -1:
                            return self.draw_level_menu()
                        return None if ret is None else [game_info.LEVEL3, ret]
                    
                    if level4.collidepoint(event.pos):
                        ret = self.select_game_mode()
                        if ret == -1:
                            return self.draw_level_menu()
                        return None if ret is None else [game_info.LEVEL4, ret]
                    
    def select_game_mode(self) -> Union[int, None]:
        """
            Desenha os game modes e dá "handle" à lógica.
        """
        
        self.screen.fill(game_info.BLACK)

        self.draw_text("Select game mode", WIDTH//2, TITLE_HEIGHT, "titulo")

        mode = []
        mode.append(self.draw_text("Manually", WIDTH//4, HEIGHT//2 - 130))
        mode.append(self.draw_text("BFS", WIDTH//2, HEIGHT//2 - 130))
        mode.append(self.draw_text("DFS", WIDTH//2, HEIGHT//2 - 80))
        mode.append(self.draw_text("Greedy (bad h)", WIDTH//2 + WIDTH//4, HEIGHT//2 - 130))
        mode.append(self.draw_text("Greedy (good h)", WIDTH//2 + WIDTH//4, HEIGHT//2 - 80))
        mode.append(self.draw_text("A* (bad h)", WIDTH//2 + WIDTH//4, HEIGHT//2 - 30))
        mode.append(self.draw_text("A* (good h)", WIDTH//2 + WIDTH//4, HEIGHT//2 + 20))
        mode.append(self.draw_text("Weighted A* (bad h)", WIDTH//2 + WIDTH//4, HEIGHT//2 + 70))
        mode.append(self.draw_text("Weighted A* (good h)", WIDTH//2 + WIDTH//4, HEIGHT//2 + 120))

        go_back = self.draw_text("Go back", WIDTH//2, HEIGHT - 50)

        self.update_screen()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if go_back.collidepoint(event.pos):
                        return -1

                    for i in range(0, len(mode)):
                        if mode[i].collidepoint(event.pos):
                            return i


class FinalMenu(Draw):
    """
        Classe que possui funções e lógica do menu final.
    """

    def __init__(self, title:str) -> None:
        """
            Cria um elemento da classe FinalMenu.
        """
        
        super().__init__()

        self.play_again, self.main_menu = self.draw_menu(title)

    def draw_menu(self, title:str) -> tuple[pygame.Rect, pygame.Rect]:
        """
            Desenha o menu final.
        """
        
        self.screen.fill(game_info.BLACK)
        self.draw_text(title, WIDTH//2, TITLE_HEIGHT, "titulo")
        play_again = self.draw_text("Play Again", WIDTH//2, HEIGHT//2 - 60)
        main_menu = self.draw_text("Main Menu", WIDTH//2, HEIGHT//2 - 10)
        self.update_screen()

        return play_again, main_menu

    def run(self) -> Union[None, int]:
        """
            "handle" lógica do menu final.
        """
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.play_again.collidepoint(event.pos):
                        return 0
                    if self.main_menu.collidepoint(event.pos):
                        return 1

class Game(Draw):
    """
        Classe responsável por desenhar e dar "handle" à lógica do jogo.
    """
    
    def __init__(self, board: list, game_mode: int) -> None:
        """
            Cria um elemento da classe Game.
        """
        
        super().__init__()
        self.game_mode = game_mode
        self.level_info = board
        self.board, self.energy, image_path, self.title, self.goal, self.max_height = self.parse_level(board)
        self.image = pygame.transform.scale(pygame.image.load(image_path), (200, 150))
        self.prev_board = None
        self.rects, self.reset, self.undo_button, self.main_menu, self.hint_button = self.draw_game()

    def parse_level(self, level:list) -> tuple[list, int, str, str, list]:
        """
            Dá parse à variável que contém toda a informação sobre o nível.
        """
        
        board = []
        goal = []
        for row in level[0]:
            board.append([self.get_circle_color(cell) for cell in row])
        for row in level[4]:
            goal.append([self.get_circle_color(cell) for cell in row])
        
        return board, level[1], level[2], level[3], goal, level[5]
                
    def draw_game(self) -> tuple[list, pygame.Rect]:
            """
                Desenha o jogo.
            """
            
            self.draw_text(self.title, WIDTH//2, 50, "titulo")

            self.draw_energy()

            hint = None
            if self.game_mode == 0:
                hint = self.draw_hint_button()

            reset = self.draw_reset()
            main_menu = self.draw_main_menu_button()

            undo = None
            if self.prev_board is not None:
                undo = self.draw_undo()

            self.draw_goal()
            self.draw_lines()   # desenha linhas primeiro para circulos tapar o excesso

            l = []
            l.append(self.draw_first_row())
            l.append(self.draw_second_row())
            l.append(self.draw_third_row())
            if (self.max_height > 3):
                l.append(self.draw_forth_row())
                l.append(self.draw_fifth_row())

            self.update_screen()
            
            return l, reset, undo, main_menu, hint
    
    def draw_hint_button(self) -> pygame.Rect :
        """
            Desenha o botão "Hint".
        """
        return self.draw_text("Hint", WIDTH//2 + 295, HEIGHT//2 + 170)

    def draw_main_menu_button(self) -> pygame.Rect :
        """
            Desenha o botão "Main Menu".
        """
        return self.draw_text("Main Menu", 100, HEIGHT//2 + 230)

    def draw_undo(self) -> pygame.Rect:
        """
            Desenha o botão "Undo".
        """
        return self.draw_text("Undo", 100, HEIGHT//2 + 170)
    
    def draw_goal(self) -> None:
        """
            Desenha a borda final.
        """

        self.draw_text("Goal:", WIDTH//2 + 295, TITLE_HEIGHT + 15)
        self.screen.blit(self.image, (WIDTH//2 + 200, 130))

    def draw_energy(self) -> None:
        """
            Desenha a energia.
        """

        self.draw_text("Energy", 100, TITLE_HEIGHT + 15)
        self.draw_text(str(self.energy), 100, TITLE_HEIGHT + 45, "normal", game_info.YELLOW)

    def draw_reset(self) -> pygame.Rect:
        """
            Desenha o botão "reset".
        """
        return self.draw_text("Reset level", 100, HEIGHT//2 + 200)

    def draw_first_row(self) -> list:
        """
            Desenha a primeira linha do jogo.
        """

        l = []
        l.append(pygame.draw.circle(self.screen, self.board[0][0], (WIDTH//2 - 130, 150), 20))
        l.append(pygame.draw.circle(self.screen, self.board[0][1], (WIDTH//2, 210), 20))
        l.append(pygame.draw.circle(self.screen, self.board[0][2], (WIDTH//2 + 130, 150), 20))
        return l

    def draw_second_row(self) -> list:
        """
            Desenha a segunda linha do jogo.
        """
        
        l = []
        l.append(pygame.draw.circle(self.screen, self.board[1][0], (WIDTH//2 - 130, 270), 20))
        l.append(pygame.draw.circle(self.screen, self.board[1][1], (WIDTH//2 - 65, 240), 20))
        l.append(pygame.draw.circle(self.screen, self.board[1][2], (WIDTH//2 + 65, 240), 20))
        l.append(pygame.draw.circle(self.screen, self.board[1][3], (WIDTH//2 + 130, 270), 20))
        return l

    def draw_third_row(self) -> list:
        """
            Desenha a terceira linha do jogo.
        """
        
        l = []
        l.append(pygame.draw.circle(self.screen, self.board[2][0], (WIDTH//2 - 260, 330), 20))
        l.append(pygame.draw.circle(self.screen, self.board[2][1], (WIDTH//2 - 130, 330), 20))
        l.append(pygame.draw.circle(self.screen, self.board[2][2], (WIDTH//2, 330), 20))
        l.append(pygame.draw.circle(self.screen, self.board[2][3], (WIDTH//2 + 130, 330), 20))
        l.append(pygame.draw.circle(self.screen, self.board[2][4], (WIDTH//2 + 260, 330), 20))
        return l

    def draw_forth_row(self) -> list:
        """
            Desenha a quarta linha do jogo.
        """
        
        l = []
        l.append(pygame.draw.circle(self.screen, self.board[3][0], (WIDTH//2 - 130, 390), 20))
        l.append(pygame.draw.circle(self.screen, self.board[3][1], (WIDTH//2 - 65, 420), 20))
        l.append(pygame.draw.circle(self.screen, self.board[3][2], (WIDTH//2 + 65, 420), 20))
        l.append(pygame.draw.circle(self.screen, self.board[3][3], (WIDTH//2 + 130, 390), 20))
        return l

    def draw_fifth_row(self) -> list:
        """
            Desenha a quinta linha do jogo.
        """
        
        l = []
        l.append(pygame.draw.circle(self.screen, self.board[4][0], (WIDTH//2 - 130, 510), 20))
        l.append(pygame.draw.circle(self.screen, self.board[4][1], (WIDTH//2, 450), 20))
        l.append(pygame.draw.circle(self.screen, self.board[4][2], (WIDTH//2 + 130, 510), 20))
        return l

    def draw_lines(self) -> None:
        """
            Desenha as linhas que conectam os circulos.
        """

        pygame.draw.line(self.screen, game_info.DARKGREY, (WIDTH//2 - 130, 150), (WIDTH//2 - 130, 510 if self.max_height > 3 else 330), 5) #[0][0] -> [4][0]
        pygame.draw.line(self.screen, game_info.DARKGREY, (WIDTH//2 - 130, 150), (WIDTH//2 + 130, 510) if self.max_height > 3 else (WIDTH//2, 330), 5) #[0][0] -> [4][2] 
        pygame.draw.line(self.screen, game_info.DARKGREY, (WIDTH//2 - 130, 150), (WIDTH//2 + 260, 330), 5) #[0][0] -> [2][4]
        pygame.draw.line(self.screen, game_info.DARKGREY, (WIDTH//2 + 130, 150), (WIDTH//2 - 130, 510) if self.max_height > 3 else (WIDTH//2, 330), 5) #[0][2] -> [4][0]
        pygame.draw.line(self.screen, game_info.DARKGREY, (WIDTH//2 + 130, 150), (WIDTH//2 + 130, 510 if self.max_height > 3 else 330), 5) #[0][2] -> [4][2]
        pygame.draw.line(self.screen, game_info.DARKGREY, (WIDTH//2 - 260, 330), (WIDTH//2 + 130, 150), 5) #[2][0] -> [0][2]
        pygame.draw.line(self.screen, game_info.DARKGREY, (WIDTH//2 - 260, 330), (WIDTH//2 + 260, 330), 5) #[2][0] -> [2][4]
        if self.max_height > 3:
            pygame.draw.line(self.screen, game_info.DARKGREY, (WIDTH//2 - 260, 330), (WIDTH//2 + 130, 510), 5) #[2][0] -> [4][2]
            pygame.draw.line(self.screen, game_info.DARKGREY, (WIDTH//2 + 260, 330), (WIDTH//2 - 130, 510), 5) #[2][4] -> [4][0]
        
    def get_circle_color(self, color: int) -> tuple[int, int, int]:
        """
            Obtém a cor de um círculo a partir da informção "raw" do nível.
        """
        
        colors = [game_info.GREY, game_info.RED, game_info.GREEN, game_info.BLUE, game_info.WHITE, game_info.YELLOW, game_info.PINK, game_info.AQUA]
        return colors[color]
    
    def reset_level(self, game:dol) -> None:
        """
            Dá reset ao tabuleiro.
        """
        
        self.board, self.energy, _, self.title, self.goal, _ = self.parse_level(self.level_info)
        game.reset(deepcopy(self.board), self.energy)
        self.screen.fill(game_info.BLACK)
        self.rects, self.reset, self.undo_button, self.main_menu, self.hint_button = self.draw_game()

    def undo(self, game:dol) -> None:
        """
            Volta uma jogada atrás.
        """

        self.screen.fill(game_info.BLACK)
        self.board = deepcopy(self.prev_board)
        self.prev_board = None
        self.energy += 1
        game.reset(deepcopy(self.board), self.energy)
        self.rects, self.reset, self.undo_button, self.main_menu, self.hint_button = self.draw_game();
        self.update_screen()

    def highlight_selected(self, highlight:bool, center:tuple[int, int], coords_circle:tuple[int, int]) -> tuple[int, int]:
        """
            "handle" a lógica de quando se clica num circulo.

            Se não tiver nenhum círculo selecionado dá "highlight" ao círculo. 
            Se tiver um círculo selecionado tira o "highlight".
        """
        
        i,j = coords_circle

        if highlight is False and self.board[i][j] != game_info.GREY:
            highlight = True
            center = (i,j)
            pygame.draw.circle(self.screen, game_info.ORANGE, self.rects[i][j].center, 23)
            pygame.draw.circle(self.screen, self.board[i][j], self.rects[i][j].center, 20)
            self.update_screen()
        elif highlight is True and (i,j) == center:
            highlight = False
            center = None
            self.screen.fill(game_info.BLACK)
            self.rects, self.reset, self.undo_button, self.main_menu, self.hint_button = self.draw_game()

        return highlight, center
    
    def show_algorithm_moves(self, node, time: int) -> None:
        """
            Mostra as jogadas do algoritmo.
        """
        
        moves = []

        while node:
            moves.append(node.state)
            node = node.parent

        moves.reverse()
        for move in moves:
            self.board = move
            self.screen.fill(game_info.BLACK)
            self.draw_game()
            self.draw_text("Time: " + str(time) + "s", 100, TITLE_HEIGHT + 105) # display do tempo no ecra
            self.draw_text("Total Moves: " + str(len(moves)-1), 110, TITLE_HEIGHT + 155) # display do numero total de jogadas
            self.update_screen()
            sleep(1)

    def get_first_algorithm_move(self, node) -> tuple[tuple[int, int], tuple[int, int]]:
        """
            Obtém a primeria jogada do algorítmo.
        """
        
        moves = []

        while node:
            moves.append(node.state)
            node = node.parent

        move = moves[-2]
        pos = []
        for i in range(0, len(self.board)):
            for j in range(0, len(self.board[i])):
                if self.board[i][j] != move[i][j]:
                    pos.append((i,j))
                    
        return pos[0], pos[1]

    def run(self) -> Union[None, int]:
        """
            "handle" a lógica do jogo.
        """
        
        game = dol.DropOfLight(deepcopy(self.board), self.goal, self.energy, self.max_height)

        highlight = False
        center = None
        finished_algo = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.main_menu.collidepoint(event.pos):
                        return -1

                    if self.reset.collidepoint(event.pos):
                        self.reset_level(game)
                        finished_algo = False
                        continue

                # manually
                if self.game_mode == 0:

                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.hint_button.collidepoint(event.pos):
                            algorithm = algorithms.Algorithm(self.board, self.goal, self.energy, self.max_height)
                            moves = algorithm.AStar()
                            (x1,y1), (x2,y2) = self.get_first_algorithm_move(moves)

                            # highlight hint
                            pygame.draw.circle(self.screen, game_info.PURPLE, self.rects[x1][y1].center, 23)
                            pygame.draw.circle(self.screen, self.board[x1][y1], self.rects[x1][y1].center, 20)
                            pygame.draw.circle(self.screen, game_info.PURPLE, self.rects[x2][y2].center, 23)
                            pygame.draw.circle(self.screen, self.board[x2][y2], self.rects[x2][y2].center, 20)  

                            self.update_screen()                      

                        if self.undo_button is not None and self.undo_button.collidepoint(event.pos):
                            self.undo(game)
                            continue

                        for i in range(0, len(self.rects)):
                            for j in range(0, len(self.rects[i])):
                                if self.rects[i][j].collidepoint(event.pos):

                                    #highlight a circulo que user clique
                                    highlight, center = self.highlight_selected(highlight, center, (i,j))

                                    ret = game.handle_piece_selected((i,j))
                                    if ret is None:
                                        break
                                    
                                    center = None
                                    highlight = False
                                    self.prev_board = deepcopy(self.board)
                                    self.board, self.energy = ret
                                    self.screen.fill(game_info.BLACK)

                                    # win
                                    if self.board == []:
                                        win_menu = FinalMenu("You Won")
                                        ret = win_menu.run()
                                        if ret != 0:
                                            return ret
                                        self.prev_board = None
                                        self.reset_level(game)
                                        
                                    # lose
                                    if self.energy == 0:
                                        lose_menu = FinalMenu("You Lost")
                                        ret = lose_menu.run()
                                        if ret != 0:
                                            return ret
                                        self.prev_board = None
                                        self.reset_level(game)

                                    self.rects, self.reset, self.undo_button, self.main_menu, self.hint_button = self.draw_game()
                
                # algorithms
                else:
                    if finished_algo:
                        continue

                    algorithm = algorithms.Algorithm(self.board, self.goal, self.energy, self.max_height)

                    begin = time()
                    if self.game_mode == 1:
                        moves = algorithm.BFS()
                    elif self.game_mode == 2:
                        moves = algorithm.DFS()
                    elif self.game_mode == 3: # greedy bad heuristic
                        moves = algorithm.greedy(False)
                    elif self.game_mode == 4: # greedy good heuristic
                        moves = algorithm.greedy()
                    elif self.game_mode == 5: # A* bad heuristic
                        moves = algorithm.AStar(False)
                    elif self.game_mode == 6: # A* good heuristic
                        moves = algorithm.AStar()
                    elif self.game_mode == 7: # WA* bad heuristic
                        moves = algorithm.WeightedAStar(False)
                    elif self.game_mode == 8: # WA* good heuristic
                        moves = algorithm.WeightedAStar()

                    end = time()

                    elapsed_time = end - begin
                    self.show_algorithm_moves(moves, round(elapsed_time, 2 if elapsed_time > 0.01 else 3))
                    finished_algo = True
