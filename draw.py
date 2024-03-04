import pygame
from game_info import RULES_TEXT, LEVEL1
from typing import Union

BLACK = (0, 0, 0)               
LIGHTGREY = (211, 211, 211) 
GREY = (128, 128, 128)
DARKGREY = (169, 169, 169)
RED = (255, 0, 0)               #1
GREEN = (0, 255, 0)             #2
BLUE = (0, 0, 255)              #3
WHITE = (255, 255, 255)         #4    
YELLOW = (255, 255, 0)          #5
PINK = (255, 0, 255)            #6
AQUA = (0, 255, 255)            #7

WIDTH = 800
HEIGHT = 600
TITLE_HEIGHT = 100

class Draw:
    def __init__(self) -> None:
        pygame.init()

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
                        pass

                    if level3.collidepoint(event.pos):
                        pass


class Game(Draw):
    def __init__(self, board: list) -> None:
        super().__init__()
        self.board, self.energy, self.title = self.parse_board(board)
        self.draw_game()

    def parse_board(self, board:list) -> tuple[list, int]:
        l = []
        for i in range(0, len(board)):
            if i == len(board)-2:
                return (l,board[i],board[i+1])
            l.append([self.get_circle_color(cell) for cell in board[i]])

    def draw_game(self) -> None:
            self.draw_text(self.title, WIDTH//2, 50, "titulo")
            self.draw_energy()
            self.draw_lines() # desenha linhas primeiro para circulos tapar o excesso
            self.draw_first_row()
            self.draw_second_row()
            self.draw_third_row()
            self.draw_forth_row()
            self.draw_fifth_row()
            self.update_screen()

    def draw_energy(self) -> None:
        self.draw_text("Energy", 100, TITLE_HEIGHT + 50)
        self.draw_text(str(self.energy), 100, TITLE_HEIGHT + 80, "normal", YELLOW)

    def draw_first_row(self) -> None:
        pygame.draw.circle(self.screen, self.board[0][0], (WIDTH//2 - 130, 150), 20)
        pygame.draw.circle(self.screen, self.board[0][1], (WIDTH//2, 210), 20)
        pygame.draw.circle(self.screen, self.board[0][2], (WIDTH//2 + 130, 150), 20)

    def draw_second_row(self) -> None:
        pygame.draw.circle(self.screen, self.board[1][0], (WIDTH//2 - 130, 270), 20)
        pygame.draw.circle(self.screen, self.board[1][1], (WIDTH//2 - 65, 240), 20)
        pygame.draw.circle(self.screen, self.board[1][2], (WIDTH//2 + 65, 240), 20)
        pygame.draw.circle(self.screen, self.board[1][3], (WIDTH//2 + 130, 270), 20)

    def draw_third_row(self) -> None:
        pygame.draw.circle(self.screen, self.board[2][0], (WIDTH//2 - 260, 330), 20)
        pygame.draw.circle(self.screen, self.board[2][1], (WIDTH//2 - 130, 330), 20)
        pygame.draw.circle(self.screen, self.board[2][2], (WIDTH//2, 330), 20)
        pygame.draw.circle(self.screen, self.board[2][3], (WIDTH//2 + 130, 330), 20)
        pygame.draw.circle(self.screen, self.board[2][4], (WIDTH//2 + 260, 330), 20)

    def draw_forth_row(self) -> None:
        pygame.draw.circle(self.screen, self.board[3][0], (WIDTH//2 - 130, 390), 20)
        pygame.draw.circle(self.screen, self.board[3][1], (WIDTH//2 - 65, 420), 20)
        pygame.draw.circle(self.screen, self.board[3][2], (WIDTH//2 + 65, 420), 20)
        pygame.draw.circle(self.screen, self.board[3][3], (WIDTH//2 + 130, 390), 20)

    def draw_fifth_row(self) -> None:
        pygame.draw.circle(self.screen, self.board[4][0], (WIDTH//2 - 130, 510), 20)
        pygame.draw.circle(self.screen, self.board[4][1], (WIDTH//2, 450), 20)
        pygame.draw.circle(self.screen, self.board[4][2], (WIDTH//2 + 130, 510), 20)

    def draw_lines(self) -> None:
        pygame.draw.line(self.screen, DARKGREY, (WIDTH//2 - 130, 150), (WIDTH//2 - 130, 510), 5) #[0][0] -> [4][0]
        pygame.draw.line(self.screen, DARKGREY, (WIDTH//2 - 130, 150), (WIDTH//2 + 130, 510), 5) #[0][0] -> [4][2] 
        pygame.draw.line(self.screen, DARKGREY, (WIDTH//2 - 130, 150), (WIDTH//2 + 260, 330), 5) #[0][0] -> [2][4]
        pygame.draw.line(self.screen, DARKGREY, (WIDTH//2 + 130, 150), (WIDTH//2 - 130, 510), 5) #[0][2] -> [4][0]
        pygame.draw.line(self.screen, DARKGREY, (WIDTH//2 + 130, 150), (WIDTH//2 + 130, 510), 5) #[0][2] -> [4][2]
        pygame.draw.line(self.screen, DARKGREY, (WIDTH//2 - 260, 330), (WIDTH//2 + 130, 150), 5) #[2][0] -> [0][2]
        pygame.draw.line(self.screen, DARKGREY, (WIDTH//2 - 260, 330), (WIDTH//2 + 260, 330), 5) #[2][0] -> [2][4]
        pygame.draw.line(self.screen, DARKGREY, (WIDTH//2 - 260, 330), (WIDTH//2 + 130, 510), 5) #[2][0] -> [4][2]
        pygame.draw.line(self.screen, DARKGREY, (WIDTH//2 + 260, 330), (WIDTH//2 - 130, 510), 5) #[2][4] -> [4][0]
        
    def get_circle_color(self, color:tuple[int, int, int]) -> tuple[int, int, int]:
        colors = [GREY, RED, GREEN, BLUE, WHITE, YELLOW, PINK, AQUA]
        return colors[color]
    
    def run(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None                    

