import pygame
import algorithms
import drop_of_light as dol
from game_info import RULES_TEXT, LEVEL1, LEVEL2
from typing import Union
from copy import deepcopy
from time import sleep

BLACK: tuple[int, int, int] = (0, 0, 0)               
DARKGREY: tuple[int, int, int] = (169, 169, 169)      # para as linhas
LIGHTGREY: tuple[int, int, int] = (211, 211, 211)     # para exemplos das regras
GREY: tuple[int, int, int] = (128, 128, 128)          #0
RED: tuple[int, int, int] = (255, 0, 0)               #1
GREEN: tuple[int, int, int] = (0, 255, 0)             #2
BLUE: tuple[int, int, int] = (0, 0, 255)              #3
WHITE: tuple[int, int, int] = (255, 255, 255)         #4    
YELLOW: tuple[int, int, int] = (255, 255, 0)          #5
PINK: tuple[int, int, int] = (255, 0, 255)            #6
AQUA: tuple[int, int, int] = (0, 255, 255)            #7
ORANGE: tuple[int, int, int] = (255, 165, 0)         # highlight

WIDTH: int = 800
HEIGHT: int = 600
TITLE_HEIGHT: int = 100

class Draw:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])

        self.title_font = pygame.font.SysFont("Arial", 45)
        self.normal_font = pygame.font.SysFont("Arial", 30)

        pygame.display.set_caption("Drop of Light")

    def draw_text(self, text: str, width: int, height: int, font:str = "normal", color:tuple[int, int, int] = WHITE) -> pygame.Rect:
        if font == "normal":
            f = self.normal_font
        else:
            f = self.title_font

        text_surface = f.render(text, True, color)
        text_rect = text_surface.get_rect(center=(width,height))
        self.screen.blit(text_surface, text_rect)

        return text_rect

    def update_screen(self) -> None:
        pygame.display.flip()

        
class MainMenu(Draw):
    def __init__(self) -> None:
        super().__init__()

        self.draw_main_menu()

        self.update_screen()

    def draw_main_menu(self) -> None:
        self.screen.fill(BLACK)

        self.draw_text("Drop of Light", WIDTH//2, TITLE_HEIGHT, "titulo")

        self.new_game = self.draw_text("New game", WIDTH//2, HEIGHT//2 - 60)
        self.rules =  self.draw_text("Rules", WIDTH//2, HEIGHT//2 - 10)
        self.quit = self.draw_text("Quit", WIDTH//2, HEIGHT//2 + 40)
    
    def run(self) -> Union[list, None]:
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
        return event.type == pygame.QUIT or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.quit.collidepoint(event.pos))
    
    def draw_rules(self) -> None:
        i = 0

        while i < len(RULES_TEXT):
            previous_rule = next_rule = None  
            self.screen.fill(BLACK)
            self.draw_text("Rules", WIDTH//2, TITLE_HEIGHT, "titulo")

            for (rule, index) in zip(RULES_TEXT[i], range(0, len(RULES_TEXT[i]))):
                self.draw_text(rule, WIDTH//2, HEIGHT//2 - 120 + (50 * index))

            if i == 2:
                self.draw_rule_example()

            if i != 0:
                previous_rule = self.draw_text("Previous rule", WIDTH//5, HEIGHT - 50)
            main_menu = self.draw_text("Main Menu", WIDTH//2, HEIGHT - 50)
            if i != len(RULES_TEXT)-1:
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
        self.draw_rule_line(RED, GREEN, YELLOW, 0)
        self.draw_rule_line(RED, BLUE, PINK, 50)
        self.draw_rule_line(GREEN, BLUE, AQUA, 100)
        self.draw_rule_line(RED, GREEN, WHITE, 150, 47.5)

    def draw_rule_line(self, color1, color2, color3, paddingY, paddingX = 0) -> None:
        pygame.draw.circle(self.screen, color1, (WIDTH // 2 - 95 - paddingX, HEIGHT // 2 + 40 + paddingY), 20) # 1º circulo
        pygame.draw.line(self.screen, LIGHTGREY, (WIDTH // 2 - 60 - paddingX, HEIGHT // 2 + 40 + paddingY), (WIDTH // 2 - 35 - paddingX, HEIGHT // 2 + 40 + paddingY), 5) # -
        pygame.draw.line(self.screen, LIGHTGREY, (WIDTH // 2 - 47.5 - paddingX, HEIGHT // 2 + 52.5 + paddingY), (WIDTH // 2 - 47.5 - paddingX, HEIGHT // 2 + 27.5 + paddingY), 5) # |
        pygame.draw.circle(self.screen, color2, (WIDTH // 2 - paddingX, HEIGHT // 2 + 40 + paddingY), 20) # 2º circulo
        if paddingX != 0:
            pygame.draw.line(self.screen, LIGHTGREY, (WIDTH // 2 - 60 + paddingX, HEIGHT // 2 + 40 + paddingY), (WIDTH // 2 - 35 + paddingX, HEIGHT // 2 + 40 + paddingY), 5) # -
            pygame.draw.line(self.screen, LIGHTGREY, (WIDTH // 2 - 47.5 + paddingX, HEIGHT // 2 + 52.5 + paddingY), (WIDTH // 2 - 47.5 + paddingX, HEIGHT // 2 + 27.5 + paddingY), 5) # |
            pygame.draw.circle(self.screen, BLUE, (WIDTH // 2 + paddingX, HEIGHT // 2 + 40 + paddingY), 20) # 3º circulo
        pygame.draw.line(self.screen, LIGHTGREY, (WIDTH // 2 + 35 + paddingX, HEIGHT // 2 + 35 + paddingY), (WIDTH // 2 + 60 + paddingX, HEIGHT // 2 + 35 + paddingY), 5) # resultado linha de cima
        pygame.draw.line(self.screen, LIGHTGREY, (WIDTH // 2 + 35 + paddingX, HEIGHT // 2 + 45 + paddingY), (WIDTH // 2 + 60 + paddingX, HEIGHT // 2 + 45 + paddingY), 5) # resultado linha de baixo
        pygame.draw.circle(self.screen, color3, (WIDTH // 2 + 95 + paddingX, HEIGHT // 2 + 40 + paddingY), 20) # ultimo circulo 

    def draw_level_menu(self) -> Union[list, None]:
        self.screen.fill(BLACK)

        self.draw_text("Choose a level", WIDTH//2, TITLE_HEIGHT, "titulo")
        level1 = self.draw_text("Level 1", WIDTH//2, HEIGHT//2 - 60)
        level2 = self.draw_text("Level 2", WIDTH//2, HEIGHT//2 - 10)
        level3 = self.draw_text("Level 3", WIDTH//2, HEIGHT//2 + 40)
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
                        return LEVEL1

                    if level2.collidepoint(event.pos):
                        return LEVEL2

                    if level3.collidepoint(event.pos):
                        pass


class FinalMenu(Draw):
    def __init__(self, title:str) -> None:
        super().__init__()

        self.play_again, self.main_menu = self.draw_menu(title)

    def draw_menu(self, title:str) -> tuple[pygame.Rect, pygame.Rect]:
        self.screen.fill(BLACK)
        self.draw_text(title, WIDTH//2, TITLE_HEIGHT, "titulo")
        play_again = self.draw_text("Play Again", WIDTH//2, HEIGHT//2 - 60)
        main_menu = self.draw_text("Main Menu", WIDTH//2, HEIGHT//2 - 10)
        self.update_screen()

        return play_again, main_menu

    def run(self) -> Union[None, int]:
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
    def __init__(self, board: list) -> None:
        super().__init__()
        self.level_info = board
        self.board, self.energy, image_path, self.title, self.goal, self.max_height = self.parse_level(board)
        self.image = pygame.transform.scale(pygame.image.load(image_path), (200, 150))
        self.prev_board = None
        self.rects, self.reset, self.undo_button = self.draw_game()

    def parse_level(self, level:list) -> tuple[list, int, str, str, list]:
        board = []
        goal = []
        for row in level[0]:
            board.append([self.get_circle_color(cell) for cell in row])
        for row in level[4]:
            goal.append([self.get_circle_color(cell) for cell in row])
        
        return board, level[1], level[2], level[3], goal, level[5]
                
    def draw_game(self) -> tuple[list, pygame.Rect]:
            self.draw_text(self.title, WIDTH//2, 50, "titulo")
            l = []
            self.draw_energy()
            reset = self.draw_reset()
            undo = None
            if self.prev_board is not None:
                undo = self.draw_undo()
            self.draw_goal()
            self.draw_lines() # desenha linhas primeiro para circulos tapar o excesso
            l.append(self.draw_first_row())
            l.append(self.draw_second_row())
            l.append(self.draw_third_row())
            if (self.max_height > 3):
                l.append(self.draw_forth_row())
                l.append(self.draw_fifth_row())
            self.update_screen()

            return l, reset, undo
    
    def draw_undo(self):
        return self.draw_text("Undo", 100, HEIGHT//2 + 170)
    
    def draw_goal(self) -> None:
        self.draw_text("Goal:", WIDTH//2 + 295, TITLE_HEIGHT + 15)
        self.screen.blit(self.image, (WIDTH//2 + 200, 130))

    def draw_energy(self) -> None:
        self.draw_text("Energy", 100, TITLE_HEIGHT + 15)
        self.draw_text(str(self.energy), 100, TITLE_HEIGHT + 45, "normal", YELLOW)

    def draw_reset(self) -> pygame.Rect:
        return self.draw_text("Reset level", 100, HEIGHT//2 + 200)

    def draw_first_row(self) -> list:
        l = []
        l.append(pygame.draw.circle(self.screen, self.board[0][0], (WIDTH//2 - 130, 150), 20))
        l.append(pygame.draw.circle(self.screen, self.board[0][1], (WIDTH//2, 210), 20))
        l.append(pygame.draw.circle(self.screen, self.board[0][2], (WIDTH//2 + 130, 150), 20))
        return l

    def draw_second_row(self) -> list:
        l = []
        l.append(pygame.draw.circle(self.screen, self.board[1][0], (WIDTH//2 - 130, 270), 20))
        l.append(pygame.draw.circle(self.screen, self.board[1][1], (WIDTH//2 - 65, 240), 20))
        l.append(pygame.draw.circle(self.screen, self.board[1][2], (WIDTH//2 + 65, 240), 20))
        l.append(pygame.draw.circle(self.screen, self.board[1][3], (WIDTH//2 + 130, 270), 20))
        return l

    def draw_third_row(self) -> list:
        l = []
        l.append(pygame.draw.circle(self.screen, self.board[2][0], (WIDTH//2 - 260, 330), 20))
        l.append(pygame.draw.circle(self.screen, self.board[2][1], (WIDTH//2 - 130, 330), 20))
        l.append(pygame.draw.circle(self.screen, self.board[2][2], (WIDTH//2, 330), 20))
        l.append(pygame.draw.circle(self.screen, self.board[2][3], (WIDTH//2 + 130, 330), 20))
        l.append(pygame.draw.circle(self.screen, self.board[2][4], (WIDTH//2 + 260, 330), 20))
        return l

    def draw_forth_row(self) -> list:
        l = []
        l.append(pygame.draw.circle(self.screen, self.board[3][0], (WIDTH//2 - 130, 390), 20))
        l.append(pygame.draw.circle(self.screen, self.board[3][1], (WIDTH//2 - 65, 420), 20))
        l.append(pygame.draw.circle(self.screen, self.board[3][2], (WIDTH//2 + 65, 420), 20))
        l.append(pygame.draw.circle(self.screen, self.board[3][3], (WIDTH//2 + 130, 390), 20))
        return l

    def draw_fifth_row(self) -> list:
        l = []
        l.append(pygame.draw.circle(self.screen, self.board[4][0], (WIDTH//2 - 130, 510), 20))
        l.append(pygame.draw.circle(self.screen, self.board[4][1], (WIDTH//2, 450), 20))
        l.append(pygame.draw.circle(self.screen, self.board[4][2], (WIDTH//2 + 130, 510), 20))
        return l

    def draw_lines(self) -> None:
        pygame.draw.line(self.screen, DARKGREY, (WIDTH//2 - 130, 150), (WIDTH//2 - 130, 510 if self.max_height > 3 else 330), 5) #[0][0] -> [4][0]
        pygame.draw.line(self.screen, DARKGREY, (WIDTH//2 - 130, 150), (WIDTH//2 + 130, 510) if self.max_height > 3 else (WIDTH//2, 330), 5) #[0][0] -> [4][2] 
        pygame.draw.line(self.screen, DARKGREY, (WIDTH//2 - 130, 150), (WIDTH//2 + 260, 330), 5) #[0][0] -> [2][4]
        pygame.draw.line(self.screen, DARKGREY, (WIDTH//2 + 130, 150), (WIDTH//2 - 130, 510) if self.max_height > 3 else (WIDTH//2, 330), 5) #[0][2] -> [4][0]
        pygame.draw.line(self.screen, DARKGREY, (WIDTH//2 + 130, 150), (WIDTH//2 + 130, 510 if self.max_height > 3 else 330), 5) #[0][2] -> [4][2]
        pygame.draw.line(self.screen, DARKGREY, (WIDTH//2 - 260, 330), (WIDTH//2 + 130, 150), 5) #[2][0] -> [0][2]
        pygame.draw.line(self.screen, DARKGREY, (WIDTH//2 - 260, 330), (WIDTH//2 + 260, 330), 5) #[2][0] -> [2][4]
        if self.max_height > 3:
            pygame.draw.line(self.screen, DARKGREY, (WIDTH//2 - 260, 330), (WIDTH//2 + 130, 510), 5) #[2][0] -> [4][2]
            pygame.draw.line(self.screen, DARKGREY, (WIDTH//2 + 260, 330), (WIDTH//2 - 130, 510), 5) #[2][4] -> [4][0]
        
    def get_circle_color(self, color:tuple[int, int, int]) -> tuple[int, int, int]:
        colors = [GREY, RED, GREEN, BLUE, WHITE, YELLOW, PINK, AQUA]
        return colors[color]
    
    def reset_level(self, game:dol) -> None:
        self.board, self.energy, _, self.title, self.goal, _ = self.parse_level(self.level_info)
        game.reset(deepcopy(self.board), self.energy)
        self.screen.fill(BLACK)
        self.rects, self.reset, self.undo_button = self.draw_game()

    def undo(self, game:dol) -> None:
        self.screen.fill(BLACK)
        self.board = deepcopy(self.prev_board)
        self.prev_board = None
        self.energy += 1
        game.reset(deepcopy(self.board), self.energy)
        self.rects, self.reset, self.undo_button = self.draw_game();
        self.update_screen()

    def highlight_selected(self, highlight:bool, center:tuple[int, int], coords_circle:tuple[int, int]) -> tuple[int, int]:
        i,j = coords_circle

        if highlight is False and self.board[i][j] != GREY:
            highlight = True
            center = (i,j)
            pygame.draw.circle(self.screen, ORANGE, self.rects[i][j].center, 23)
            pygame.draw.circle(self.screen, self.board[i][j], self.rects[i][j].center, 20)
            self.update_screen()
        elif highlight is True and (i,j) == center:
            highlight = False
            center = None
            self.screen.fill(BLACK)
            self.rects, self.reset, self.undo_button = self.draw_game()

        return highlight, center

    def run(self) -> Union[None, int]:
        game = dol.DropOfLight(deepcopy(self.board), self.goal, self.energy, self.max_height)

        highlight = False
        center = None

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.reset.collidepoint(event.pos):
                        self.reset_level(game)
                        continue

                    if self.undo_button is not None and self.undo_button.collidepoint(event.pos):
                        self.undo(game)
                        continue

                    bfs = algorithms.Algorithm(self.board, self.goal, self.energy, self.max_height)

                    ret = bfs.BFS()

                    if ret is not None:
                        print("not")
                    else:
                        print("None")

                    l = []
                    while ret:
                        l.append(ret.state)
                        ret = ret.parent

                    l.reverse()
                    for i in l:
                        self.board = i
                        self.draw_game()
                        self.update_screen()
                        print("Updated")
                        sleep(1)

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
                                self.screen.fill(BLACK)

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

                                self.rects, self.reset, self.undo_button = self.draw_game()



