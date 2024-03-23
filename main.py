import pygame
import draw

if __name__ == "__main__":
    pygame.init()

    while True:
        menu = draw.MainMenu()
        level = menu.run()
        if level is None:
            break

        game = draw.Game(level)
        ret = game.run()
        if ret is None:
            break   

    pygame.quit()     
