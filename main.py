import pygame
import draw

if __name__ == "__main__":
    pygame.init()

    while True:
        menu = draw.MainMenu()
        level = menu.run()
        if level is None:
            break

        game_mode = level[1]
        level = level[0]

        game = draw.Game(level, game_mode)
        ret = game.run()
        if ret is None:
            break   

    pygame.quit()     
